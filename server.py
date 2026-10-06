from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit
import json

ROOT = Path(__file__).parent
REDIRECTS = json.loads((ROOT / 'url-mapping.json').read_text())['redirects']

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / 'dist'), **kwargs)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path in REDIRECTS:
            self.send_response(301)
            self.send_header('Location', REDIRECTS[path])
            self.end_headers()
            return
        super().do_GET()

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            body = (ROOT / 'dist/404.html').read_bytes()
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().send_error(code, message, explain)

print('Local preview: http://127.0.0.1:4173/', flush=True)
ThreadingHTTPServer(('127.0.0.1', 4173), Handler).serve_forever()
