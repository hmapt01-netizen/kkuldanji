import os
import sys
import threading
import socket
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

web_dir = os.path.abspath(r"d:\작업\꿀단지\kkuldanji_web")

class HoneyjarHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=web_dir, **kwargs)

    def log_message(self, format, *args):
        # 무소음 또는 안전 로그
        pass

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

class IPv6Server(ThreadingHTTPServer):
    address_family = socket.AF_INET6

def serve_ipv4(port):
    try:
        httpd4 = ThreadingHTTPServer(('127.0.0.1', port), HoneyjarHandler)
        httpd4.serve_forever()
    except Exception as e:
        pass

def serve_ipv6(port):
    try:
        httpd6 = IPv6Server(('::1', port), HoneyjarHandler)
        httpd6.serve_forever()
    except Exception as e:
        pass

def main():
    port = 8080
    t4 = threading.Thread(target=serve_ipv4, args=(port,), daemon=True)
    t6 = threading.Thread(target=serve_ipv6, args=(port,), daemon=True)
    t4.start()
    t6.start()
    print(f"Dual Honeyjar Server running on 127.0.0.1:{port} and [::1]:{port} (localhost)", flush=True)
    # 메인 스레드 유지
    t4.join()
    t6.join()

if __name__ == '__main__':
    main()
