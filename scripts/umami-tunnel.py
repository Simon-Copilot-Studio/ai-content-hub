"""Umami Cloudflare Tunnel Manager - starts tunnel and captures URL."""
import subprocess, time, re, os, sys

HUGO_TOML = "/home/simon/.openclaw/workspace/projects/ai-content-hub/hugo.toml"
DATA_DIR = "/home/simon/.openclaw/workspace/projects/ai-content-hub/data"
PIDFILE = "/tmp/umami-tunnel.pid"

def start():
    os.makedirs(DATA_DIR, exist_ok=True)
    proc = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", "http://localhost:3100", "--no-autoupdate"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    with open(PIDFILE, "w") as f:
        f.write(str(proc.pid))

    url = None
    for _ in range(30):
        line = proc.stdout.readline()
        if not line:
            time.sleep(1)
            continue
        m = re.search(r'(https://[a-z0-9-]+\.trycloudflare\.com)', line)
        if m:
            url = m.group(1)
            break

    if url:
        with open(f"{DATA_DIR}/tunnel_url.txt", "w") as f:
            f.write(url)
        # Update hugo.toml
        with open(HUGO_TOML, "r") as f:
            content = f.read()
        content = re.sub(r"scriptUrl = '.*?'", f"scriptUrl = '{url}/script.js'", content)
        with open(HUGO_TOML, "w") as f:
            f.write(content)
        print(f"✅ Tunnel: {url}")
        print(f"✅ Hugo config updated with {url}/script.js")
    else:
        print("❌ Failed to get tunnel URL")
    return url

def stop():
    if os.path.exists(PIDFILE):
        with open(PIDFILE) as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, 15)
            print("Tunnel stopped")
        except ProcessLookupError:
            pass
        os.remove(PIDFILE)

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "start"
    if action == "start":
        start()
    elif action == "stop":
        stop()
    elif action == "restart":
        stop()
        time.sleep(2)
        start()
