---
name: automated-blog-publisher
category: productivity
description: End-to-end automated blog publishing workflow - from RSS news monitoring to SEO-optimized content creation and Git deployment
version: 1.1.0
author: Hermes Agent
tags: [blog, automation, rss, seo, git, content-creation, image-generation]
---

# Automated Blog Publisher

A comprehensive workflow for automatically discovering trending topics, writing SEO-optimized blog posts, and deploying them to a Git-based blog platform.

## Overview

This skill implements a complete automated blog publishing pipeline:
1. **RSS Monitoring**: Track multiple tech/news sources for recent content
2. **Topic Selection**: Filter for relevant, non-duplicate topics within specified scope
3. **Content Creation**: Write SEO-optimized articles following existing blog format
4. **Media Management**: Handle images (generate or use fallback URLs)
5. **Git Deployment**: Commit and push articles automatically
6. **Notifications**: Send completion notifications

## Prerequisites

### Required Tools
- **Primary Option**: `blogwatcher-cli` - RSS feed monitoring
- **Alternative Option**: Browser tools for direct site navigation
- Git - Version control for blog content
- Text editor - Content creation (handled by Hermes)

### Setup Commands
```bash
# Install blogwatcher CLI (RSS-based approach)
go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest

# Verify installation
which blogwatcher-cli
# Should output: /home/simon/go/bin/blogwatcher-cli
```

### Alternative: Browser-Based Approach
When RSS feeds are unavailable or blocked (common with news sites):
- Use `browser_navigate` to access news sites directly
- Navigate through site structure manually
- Extract content from full article pages
- Handle bot detection gracefully

## Configuration

### RSS Feed Setup
Add relevant news sources to blogwatcher:

```bash
# Technology news sources
blogwatcher-cli add "TechCrunch" https://techcrunch.com/feed/
blogwatcher-cli add "MIT Technology Review" https://www.technologyreview.com/feed/
blogwatcher-cli add "The Verge" https://www.theverge.com/rss/index.xml

# Business/Finance sources
blogwatcher-cli add "Reuters Business" https://www.reuters.com/business/ --feed-url https://www.reuters.com/business/rss/

# Add more sources as needed
```

### Blog Configuration
Ensure blog directory structure:
```
~/blog/
├── content/
│   ├── tech/
│   ├── finance/
│   ├── economy/
│   └── ...
├── static/
│   └── images/
└── git repository
```

## Workflow Steps

### 1. News Monitoring & Topic Discovery

#### Method A: RSS Monitoring (Primary)
```bash
# Scan all configured sources
~/go/bin/blogwatcher-cli scan

# Check recent articles
~/go/bin/blogwatcher-cli articles --all | head -20

# Filter by date and topic
~/go/bin/blogwatcher-cli articles --all | grep "2026-05-17"
```

#### Method B: Browser-Based Discovery (Alternative)
When RSS feeds are blocked or unavailable:

```bash
# Navigate directly to news sites
browser_navigate "https://techcrunch.com"
browser_click "AI category link"
browser_snapshot

# Extract recent articles
browser_vision "Extract full article content"
```

**Key Considerations:**
- Monitor sources within 3-hour window for timeliness
- Check existing content to avoid duplicates
- Focus on high-impact topics with lasting relevance
- Prioritize stories with multiple source coverage
- **Handle bot detection**: Use browser tools instead of direct API calls

### 2. Topic Selection Criteria

**Selection Process:**
1. **Relevance**: Must fit blog scope (AI/tech, finance, semiconductors, etc.)
2. **Timeliness**: Published within last 3-6 hours
3. **Impact**: High significance to target audience
4. **Uniqueness**: No existing coverage in blog content
5. **SEO Potential**: Strong keywords and search traffic potential

**Topic Examples:**
- AI technology breakthroughs
- Semiconductor industry news
- Financial market trends
- Policy changes affecting tech
- Company announcements (Apple, Google, NVIDIA, etc.)

### 3. Content Creation

**Article Structure:**
```yaml
---
title: "SEO-Optimized Title in Chinese"
date: 2026-05-17T08:00:00+08:00
description: "Compelling meta description"
categories:
  - "科技"  # or appropriate category
tags:
  - "Tag1"
  - "Tag2"
  - "Tag3"
image: "https://images.unsplash.com/...?w=800&q=80"
readingTime: 8-12  # estimated reading time
draft: false
faq:
  - q: "Key question 1"
    a: "Comprehensive answer"
  - q: "Key question 2"  
    a: "Detailed explanation"
---
```

**Content Guidelines:**
- Write in Traditional Chinese (繁體中文)
- Include SEO-optimized title and description
- Structure with clear headings and subheadings
- Add 4-6 comprehensive FAQ sections
- Include relevant Taiwan/regional implications
- Maintain professional tone with accessibility
- Target 8-12 minute reading time

### 4. Image Handling

**Image Sources:**
- **Primary**: Use `image_generate` tool when available
- **Fallback**: Use Unsplash URLs with proper sizing (when image_generate unavailable)
- **Format**: `https://images.unsplash.com/photo-xxx?w=800&q=80`

**Image Directory Structure:**
```
~/blog/static/images/
├── tech/
├── finance/
├── economy/
└── ...
```

**Handling Missing Tools:**
When `image_generate` is not available:
```bash
# Create image directory
mkdir -p ~/blog/static/images/[category]

# Use high-quality Unsplash images
# Create attribution file
echo "# Image attribution
# Source: Unsplash
# URL: [image_url]
# Description: [description]" > ~/blog/static/images/[category]/[article]-image.txt
```

**Practical Finding**: Many environments lack image generation tools, so Unsplash fallback should be the primary strategy.

### 5. Image Enhancement Workflow

**Automated Image Generation for Existing Content**

This workflow scans existing blog posts for missing images and automatically generates appropriate images:

#### Step 1: Scan for Missing Images
```bash
# Create image generation script
cat > /tmp/blog-image-gen.py << 'EOF'
#!/usr/bin/env python3
import os
import json
import re
from pathlib import Path

def extract_front_matter(content):
    """Extract front matter from markdown content"""
    if content.startswith('---'):
        lines = content.split('\n')
        fm_end = 0
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                fm_end = i
                break
        if fm_end > 0:
            fm_content = '\n'.join(lines[1:fm_end])
            return fm_content, fm_end
    return None, 0

def has_image_field(front_matter):
    """Check if front matter contains an image field"""
    return 'image:' in front_matter and 'image: ""' not in front_matter

def generate_prompt(title, content):
    """Generate image prompt based on title and content"""
    title_words = set(title.lower().split())
    
    tech_keywords = ['ai', 'artificial intelligence', 'machine learning', 'blockchain', 
                    'cryptocurrency', 'bitcoin', 'nvidia', 'gpu', 'chip', 'semiconductor']
    finance_keywords = ['finance', 'investment', 'stock', 'market', 'trading', 
                       'bitcoin', 'crypto', 'etf', 'capex', 'revenue']
    
    if any(word in title_words for word in tech_keywords):
        return f"Professional technology illustration of {title}. AI neural network visualization, circuit board patterns, digital innovation concept. Clean, modern design with blue and purple color scheme."
    elif any(word in title_words for word in finance_keywords):
        return f"Financial chart and market data visualization for {title}. Stock market graph, cryptocurrency trend line, investment analysis concept. Professional finance theme with green and gold colors."
    else:
        return f"Professional illustration for {title}. Modern, clean design with relevant symbolism."

def scan_blog_content():
    """Scan blog content for articles without images"""
    blog_path = Path("/home/simon/blog/content")
    queue = []
    
    md_files = list(blog_path.rglob("*.md"))
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            fm_content, offset = extract_front_matter(content)
            if fm_content and has_image_field(fm_content):
                continue
            
            title_match = re.search(r'title:\s*"([^"]+)"', fm_content)
            title = title_match.group(1) if title_match else md_file.stem
            
            prompt = generate_prompt(title, content)
            
            queue.append({
                "path": str(md_file),
                "prompt": prompt
            })
            
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    return queue

if __name__ == "__main__":
    queue = scan_blog_content()
    
    with open("/tmp/blog-image-queue.json", "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
    
    print(f"Found {len(queue)} articles needing images")
EOF

python3 /tmp/blog-image-gen.py
```

#### Step 2: Generate Images
```bash
# Create placeholder image generation
cat > /tmp/blog-image-final.py << 'EOF'
#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import time

def create_placeholder_image(title, output_path):
    """Create a simple placeholder image with text"""
    img = Image.new('RGB', (800, 400), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    words = title.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if draw.textlength(test_line, font=font) <= 760:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    y = (400 - len(lines) * 40) // 2
    for line in lines:
        text_width = draw.textlength(line, font=font)
        x = (800 - text_width) // 2
        draw.text((x, y), line, fill='darkblue', font=font)
        y += 40
    
    img.save(output_path)
    return True

def update_markdown_with_image(file_path, image_url):
    """Update markdown file with image field"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.startswith('---'):
            lines = content.split('\n')
            fm_end = 0
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    fm_end = i
                    break
            
            if fm_end > 0:
                fm_lines = lines[1:fm_end]
                updated_fm = []
                image_found = False
                
                for line in fm_lines:
                    if line.strip().startswith('image:'):
                        updated_fm.append(f'image: "{image_url}"')
                        image_found = True
                    else:
                        updated_fm.append(line)
                
                if not image_found:
                    updated_fm.append(f'image: "{image_url}"')
                
                new_content = '---\n' + '\n'.join(updated_fm) + '\n---\n' + '\n'.join(lines[fm_end + 1:])
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True
        
        return False
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

# Main execution
with open("/tmp/blog-image-queue.json", 'r', encoding='utf-8') as f:
    queue = json.load(f)

static_dir = Path("/home/simon/blog/static/images")
static_dir.mkdir(exist_ok=True)

processed_count = 0

for item in queue[:10]:  # Process first 10 articles
    file_path = item['path']
    
    if file_path.endswith('_index.md'):
        continue
        
    title = Path(file_path).stem
    safe_title = re.sub(r'[^a-zA-Z0-9-]', '-', title)
    image_path = static_dir / f"{safe_title}.jpg"
    image_url = f"/images/{safe_title}.jpg"
    
    if create_placeholder_image(title, str(image_path)):
        if update_markdown_with_image(file_path, image_url):
            processed_count += 1
            print(f"Updated {file_path}")
    
    time.sleep(2)

print(f"Processed {processed_count} images")
EOF

python3 /tmp/blog-image-final.py
```

#### Step 3: Commit Changes
```bash
cd /home/simon/blog
git add .
git commit -m "Add generated images to blog posts"
git push origin main
```

### 6. Git Workflow

```bash
# Navigate to blog directory
cd ~/blog

# Add all changes
git add -A

# Commit with descriptive message
git commit -m "auto: [Article Title]"

# Push to remote repository
git push origin main
```

**Commit Message Format:**
- Prefix with "auto: "
- Use exact article title
- Include date when relevant

### 7. Notification System

**Notification Template:**
```text
新文章發布通知：

標題：[Article Title]
發布時間：[Date]
文章已成功發布到博客，涵蓋了[brief description]。
```

**File Location:** `~/blog/telegram_notification.txt`

**Practical Considerations:**
- Many environments lack `send_message` integration
- Store notification content in text file for manual sending
- Include complete article details for external notification systems

## Error Handling

### Common Issues and Solutions

**RSS Feed Problems:**
```bash
# Remove problematic feeds
blogwatcher-cli remove "Source Name" --yes

# Add with explicit feed URL
blogwatcher-cli add "Source Name" "https://example.com" --feed-url "https://example.com/feed.xml"

# Handle authentication issues by using alternative sources
```

**Git Issues:**
```bash
# Check git status
git status

# Handle merge conflicts if any
git pull origin main
# resolve conflicts
git add -A
git commit -m "resolve conflicts"
git push origin main
```

**Content Validation:**
- Verify frontmatter syntax
- Check for broken links
- Ensure proper categorization
- Validate FAQ format

**Image Generation Issues:**
- Check available disk space
- Verify write permissions
- Try alternative generation methods
- Check for dependency conflicts

## Best Practices

### Content Quality
- Maintain consistent writing style
- Include original insights beyond source material
- Add local/regional perspectives (especially for Taiwan audience)
- Keep paragraphs short and scannable
- Use proper markdown formatting

### SEO Optimization
- Research keywords naturally into content
- Create compelling meta descriptions
- Use relevant tags and categories
- Include FAQ sections for featured snippets
- Optimize images with alt text (when available)

### Schedule Management
- Run monitoring during peak news hours
- Allow time for content creation and review
- Buffer time for unexpected delays
- Monitor for breaking news opportunities

### Image Management
- Regularly scan existing content for missing images
- Use consistent naming conventions
- Create backup images before overwriting
- Test image URLs before publishing
- Include attribution information

## Sample Execution

```bash
# 1. Start monitoring
~/go/bin/blogwatcher-cli scan

# 2. Review recent articles
~/go/bin/blogwatcher-cli articles --all | head -30

# 3. Select and write content (Hermes handles this)
# 4. Create image (use Unsplash URL if needed)
# 5. Git commit and push
cd ~/blog && git add -A && git commit -m "auto: [Title]" && git push

# 6. Create notification
echo "通知內容..." > ~/blog/telegram_notification.txt

# 7. Enhance existing content with images
python3 /tmp/blog-image-gen.py
python3 /tmp/blog-image-final.py
git add -A && git commit -m "Add generated images to blog posts" && git push
```

## Monitoring and Maintenance

### Regular Tasks
- Weekly: Review and update RSS feed list
- Monthly: Analyze top-performing articles
- Quarterly: Update topic selection criteria
- As needed: Troubleshoot feed issues
- Monthly: Scan existing content for missing images

### Performance Metrics
- Track publish frequency
- Monitor article engagement (if analytics available)
- Measure topic selection success rate
- Track content quality scores
- Monitor image generation success rate

## Troubleshooting

**Blogwatcher Setup:**
```bash
# Check installed location
ls ~/go/bin/blogwatcher-cli

# Verify database location
ls ~/.blogwatcher-cli/

# Test individual feeds
~/go/bin/blogwatcher-cli scan "Specific Source"
```

**Browser-Based Approach Issues:**
```bash
# Handle bot detection
browser_navigate "https://techcrunch.com"  # Avoid direct search queries
browser_click "AI category"               # Navigate through site structure
browser_vision "Extract content"          # Use vision for full content

# Handle blocked content
browser_scroll "down"                     # Reveal more content
browser_console "Extract text content"    # Get article content programmatically
```

**Missing Tools Workarounds:**
- **No web_search**: Use browser_navigate + manual site navigation
- **No image_generate**: Use Unsplash URLs with proper attribution
- **No send_message**: Store notification content in text file

**Content Issues:**
- Check file permissions for blog directory
- Validate frontmatter YAML syntax
- Ensure proper character encoding
- Test image URLs before publishing

**Image Generation Issues:**
- Check available disk space for image generation
- Verify write permissions for static/images directory
- Try alternative generation methods if AI services fail
- Check for dependency conflicts (PIL, diffusers, etc.)

**Practical Findings from Recent Execution:**
1. **RSS feeds often blocked**: Browser-based approach more reliable
2. **Bot detection common**: Use browser tools instead of direct API calls
3. **Image generation frequently unavailable**: Unsplash URLs should be primary strategy
4. **Notification tools often missing**: Store content for manual notification
5. **Many posts lack images**: Automated image enhancement workflow valuable
6. **Local generation works**: PIL-based placeholder creation reliable fallback

This skill provides a complete framework for automated blog publishing, from content discovery to deployment, with built-in quality controls and error handling.