from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        d = {}
        d['server'] = os.environ['HOSTNAME']
        d['method'] = 'GET'
        d['FDENV0'] = os.environ['FDENV0']
        for name, value in sorted(self.headers.items()):
            d[name] = value.rstrip()
        json_data = json.dumps(d)
        self.send_response(200,json_data)
        self.end_headers()
        self.wfile.write(json.dumps(json_data,ensure_ascii=False).encode('gbk'))

    def do_POST(self):
        length = int(self.headers.get('content-length'))
        payload_string = self.rfile.read(length).decode('utf-8')
        payload = json.loads(payload_string)
        payload['server'] = os.environ['HOSTNAME']
        payload['method'] = 'POST'
        payload['FDENV0'] = os.environ['FDENV0']
        for name, value in sorted(self.headers.items()):
            payload[name] = value.rstrip()
        json_data = json.dumps(payload)
        self.send_response(200,json_data)
        self.end_headers()
        self.wfile.write(json.dumps(json_data,ensure_ascii=False).encode('gbk'))

httpd = HTTPServer((os.environ['HOSTNAME'], 80), SimpleHTTPRequestHandler)
httpd.serve_forever()
