from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import os
p=Path(__file__).resolve().parents[1]/"frontend";os.chdir(p);print("Open http://127.0.0.1:5500");ThreadingHTTPServer(("127.0.0.1",5500),SimpleHTTPRequestHandler).serve_forever()
