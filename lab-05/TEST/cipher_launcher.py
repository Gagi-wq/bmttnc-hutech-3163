import http.server
import socketserver
import subprocess
import sys
import os
import logging

PORT = 5001

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CipherHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        cipher = self.path[1:]  # Lấy tên cipher từ URL (ví dụ: /playfair)
        # Bản đồ tên cipher thành tên tệp PyQt5
        cipher_map = {
            "caesar": "caesar",
            "vigenere": "Vigenere",
            "railfence": "RailFence",
            "playfair": "PlayFair"  # Sửa lại thành PlayFair để khớp với tệp
        }
        if cipher in cipher_map:
            script_name = cipher_map[cipher]
            script_path = os.path.join(os.path.dirname(__file__), "ui", f"{script_name}.py")
            logger.info(f"Attempting to run {script_path}")
            if os.path.exists(script_path):
                try:
                    subprocess.Popen([sys.executable, script_path])
                    logger.info(f"Successfully launched {script_name}.py")
                    self.wfile.write(b"Success")
                except Exception as e:
                    logger.error(f"Error launching {script_name}.py: {str(e)}")
                    self.wfile.write(f"Error: {str(e)}".encode())
            else:
                logger.error(f"File {script_path} not found")
                self.wfile.write(b"File not found")
        else:
            logger.error(f"Invalid cipher: {cipher}")
            self.wfile.write(b"Invalid cipher")

with socketserver.TCPServer(("", PORT), CipherHandler) as httpd:
    print(f"Serving at port {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped by user")
        httpd.server_close()