import os
import sys
import subprocess
import time
import socket
import webview

def find_free_port():
    """Finds an available free localhost port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def main():
    port = find_free_port()
    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.py"))
    
    # Launch Streamlit server in background
    cmd = [
        sys.executable, "-m", "streamlit", "run", app_path,
        "--server.port", str(port),
        "--server.headless", "true",
        "--global.developmentMode", "false"
    ]
    
    proc = subprocess.Popen(cmd)
    
    # Wait for server startup
    time.sleep(3)

    # Launch Native OS Window
    try:
        webview.create_window(
            "AI Data Analyst",
            f"http://127.0.0.1:{port}",
            width=1280,
            height=850,
            resizable=True
        )
        webview.start()
    finally:
        proc.terminate()

if __name__ == "__main__":
    main()
