#!/usr/bin/env python3
"""Tiny local preview server:  python3 serve.py  ->  http://localhost:8765/"""
import os, sys, http.server, socketserver
root = os.path.dirname(os.path.abspath(__file__))
os.chdir(root)
port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", "8765"))
class H(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".webp": "image/webp"}
    def log_message(self, *a): pass
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", port), H) as s:
    print("serving", root, "on", port, flush=True); s.serve_forever()
