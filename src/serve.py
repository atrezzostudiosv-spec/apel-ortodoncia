from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
DIST=Path(__file__).resolve().parents[1]/'dist'
class Preview(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(DIST),**kwargs)
 def send_error(self,code,message=None,explain=None):
  if code==404:
   lang=self.path.split('/')[1]; f=DIST/(lang if lang in ('en','de') else '.')/'404.html'; data=f.read_bytes(); self.send_response(404);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
  else:super().send_error(code,message,explain)
 def end_headers(self):
  self.send_header('X-Robots-Tag','noindex, nofollow');super().end_headers()
if __name__=='__main__':
 print('APEL local: http://127.0.0.1:8000',flush=True);ThreadingHTTPServer(('127.0.0.1',8000),Preview).serve_forever()
