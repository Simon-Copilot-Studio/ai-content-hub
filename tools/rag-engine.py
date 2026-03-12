#!/usr/bin/env python3
"""
RAG Engine for OpenClaw Conversation Memory
============================================
三層記憶系統的 Layer 3 實作：
- 將對話 log / MD 檔案切分成 chunks
- 用 sentence-transformers 嵌入向量
- 存入 ChromaDB 本地向量 DB
- 支援語意搜尋

Usage:
  # 索引一個檔案
  python3 rag-engine.py index <file_path> [--source <label>]
  
  # 索引 archive 目錄下所有檔案
  python3 rag-engine.py index-all [--dir <path>]
  
  # 搜尋
  python3 rag-engine.py search "你的查詢" [--top-k 5]
  
  # 統計
  python3 rag-engine.py stats
"""

import sys
import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
RAG_DB_DIR = SCRIPT_DIR / "rag-db"
ARCHIVE_DIR = SCRIPT_DIR.parent / "memory" / "archive"
VENV_SITE = SCRIPT_DIR / "rag-env" / "lib"

# Add venv to path
for p in VENV_SITE.glob("python*/site-packages"):
    sys.path.insert(0, str(p))

import chromadb
from sentence_transformers import SentenceTransformer

# Config
CHUNK_SIZE = 500       # characters per chunk
CHUNK_OVERLAP = 100    # overlap between chunks
COLLECTION_NAME = "conversation_memory"
EMBED_MODEL = "all-MiniLM-L6-v2"  # 快速、輕量、多語言支援尚可

# Lazy globals
_client = None
_collection = None
_model = None


def get_db():
    """Get or create ChromaDB client and collection."""
    global _client, _collection
    if _client is None:
        _client = chromadb.PersistentClient(path=str(RAG_DB_DIR))
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
    return _collection


def get_model():
    """Load sentence transformer model (cached)."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks, respecting paragraph boundaries."""
    # Split by paragraphs first
    paragraphs = re.split(r'\n\n+', text.strip())
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        if len(current_chunk) + len(para) + 2 <= chunk_size:
            current_chunk += ("\n\n" + para if current_chunk else para)
        else:
            if current_chunk:
                chunks.append(current_chunk)
            # If single paragraph is too long, split by sentences
            if len(para) > chunk_size:
                sentences = re.split(r'(?<=[。！？.!?\n])\s*', para)
                current_chunk = ""
                for sent in sentences:
                    if len(current_chunk) + len(sent) + 1 <= chunk_size:
                        current_chunk += (" " + sent if current_chunk else sent)
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = sent
            else:
                current_chunk = para
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return [c for c in chunks if len(c.strip()) > 20]  # Skip tiny chunks


def file_hash(filepath: str) -> str:
    """Generate hash for deduplication."""
    return hashlib.md5(Path(filepath).read_bytes()).hexdigest()


def index_file(filepath: str, source_label: str = None):
    """Index a file into the vector DB."""
    path = Path(filepath)
    if not path.exists():
        print(f"❌ File not found: {filepath}")
        return
    
    collection = get_db()
    model = get_model()
    
    text = path.read_text(encoding="utf-8", errors="ignore")
    fhash = file_hash(filepath)
    
    # Check if already indexed (by hash)
    existing = collection.get(where={"file_hash": fhash})
    if existing and existing["ids"]:
        print(f"⏭️  Already indexed: {path.name} ({len(existing['ids'])} chunks)")
        return
    
    # Source label
    if not source_label:
        source_label = path.stem
    
    # Extract date from filename if possible
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', path.name)
    doc_date = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")
    
    # Chunk
    chunks = chunk_text(text)
    if not chunks:
        print(f"⏭️  No content to index: {path.name}")
        return
    
    # Embed
    embeddings = model.encode(chunks, show_progress_bar=False).tolist()
    
    # Store
    ids = [f"{fhash}_{i}" for i in range(len(chunks))]
    metadatas = [{
        "source": source_label,
        "file": str(path.name),
        "file_hash": fhash,
        "date": doc_date,
        "chunk_index": i,
        "total_chunks": len(chunks),
    } for i in range(len(chunks))]
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )
    
    print(f"✅ Indexed: {path.name} → {len(chunks)} chunks ({len(text)} chars)")


def index_directory(dir_path: str = None):
    """Index all markdown files in a directory."""
    target = Path(dir_path) if dir_path else ARCHIVE_DIR
    if not target.exists():
        print(f"❌ Directory not found: {target}")
        return
    
    files = sorted(target.glob("*.md"))
    if not files:
        print(f"⏭️  No .md files in {target}")
        return
    
    print(f"📁 Indexing {len(files)} files from {target}")
    for f in files:
        index_file(str(f))
    print(f"✅ Done!")


def search(query: str, top_k: int = 5):
    """Search the vector DB."""
    collection = get_db()
    model = get_model()
    
    if collection.count() == 0:
        print("⚠️  Database is empty. Index some files first.")
        return []
    
    embedding = model.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=embedding,
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )
    
    output = []
    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        similarity = 1 - dist  # cosine distance → similarity
        entry = {
            "rank": i + 1,
            "similarity": round(similarity, 3),
            "source": meta.get("source", "?"),
            "date": meta.get("date", "?"),
            "file": meta.get("file", "?"),
            "content": doc,
        }
        output.append(entry)
        print(f"\n--- Result {i+1} (similarity: {similarity:.3f}) ---")
        print(f"Source: {meta.get('source')} | Date: {meta.get('date')} | File: {meta.get('file')}")
        print(doc[:300] + ("..." if len(doc) > 300 else ""))
    
    return output


def stats():
    """Show database statistics."""
    collection = get_db()
    count = collection.count()
    print(f"📊 RAG Database Stats")
    print(f"   Collection: {COLLECTION_NAME}")
    print(f"   Total chunks: {count}")
    print(f"   DB path: {RAG_DB_DIR}")
    print(f"   Embed model: {EMBED_MODEL}")
    
    if count > 0:
        all_data = collection.get(include=["metadatas"])
        sources = set()
        dates = set()
        for m in all_data["metadatas"]:
            sources.add(m.get("source", "?"))
            dates.add(m.get("date", "?"))
        print(f"   Sources: {len(sources)}")
        print(f"   Date range: {min(dates)} → {max(dates)}")
        print(f"   Sources list: {', '.join(sorted(sources))}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "index" and len(sys.argv) >= 3:
        source = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--source" else None
        index_file(sys.argv[2], source)
    
    elif cmd == "index-all":
        dir_path = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--dir" else None
        index_directory(dir_path)
    
    elif cmd == "search" and len(sys.argv) >= 3:
        top_k = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[3] == "--top-k" else 5
        search(sys.argv[2], top_k)
    
    elif cmd == "stats":
        stats()
    
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
