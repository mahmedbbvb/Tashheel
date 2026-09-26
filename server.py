import http.server
import socketserver
import json
import os
import urllib.parse
from datetime import datetime

PORT = int(os.environ.get('PORT', 3000))
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(ROOT_DIR, 'results.json')

if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)

class TashheelHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/results':
            try:
                with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/save-result':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                item = json.loads(body)
                if 'name' not in item or 'score' not in item:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Name and score required'}).encode('utf-8'))
                    return

                item['id'] = item.get('id', f"res_{int(datetime.now().timestamp()*1000)}")
                item['timestamp'] = item.get('timestamp', int(datetime.now().timestamp()*1000))
                item['date'] = item.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                try:
                    with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if not isinstance(data, list):
                            data = []
                except Exception:
                    data = []

                data.append(item)

                with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'total': len(data), 'data': item}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/results':
            with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'message': 'تم مسح النتائج'}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), TashheelHandler) as httpd:
        print(f"\n======================================================")
        print(f"🚀 خادم بايثون لمنصة تسهيل يعمل بنجاح على المنفذ {PORT}!")
        print(f"🌐 رابط المنصة:   http://localhost:{PORT}/")
        print(f"📝 امتحان الفسيولوجي: http://localhost:{PORT}/physiology_lecture_1_quiz.html")
        print(f"📊 نتائج الامتحانات:  http://localhost:{PORT}/results.html")
        print(f"======================================================\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
