from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
os.chdir(Path(__file__).parent)
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw): super().__init__(*a,directory=os.getcwd(),**kw)
if __name__=="__main__":
    print("PIMCO demo running at http://127.0.0.1:8000")
    ThreadingHTTPServer(("0.0.0.0",8000),Handler).serve_forever()
