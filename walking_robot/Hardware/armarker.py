from Time import Time
import cv2
import numpy as np
from os import environ
from sys import argv
from readchar import readkey
import json
import socketserver
from http.server import BaseHTTPRequestHandler
from ar_markers import detect_markers
PORT = 8000


httpd = None
DISPLAY = 'DISPLAY' in environ



    # 이미지 통신 코드
    def do_POST(self):
        print(self.headers['X-Client2Server'])
        self.send_response(200)
        self.send_header('X-Server2Client', '123')
        self.end_headers()

        # 라즈베리파이에서 보낸 이미지(byte)를 읽는 코드.
        data = self.rfile.read(int(self.headers['Content-Length']))
        if DISPLAY:
            # 바이트를 array로 만들고
            data = np.asarray(bytearray(data), dtype="uint8")
            img = cv2.imdecode(data, cv2.IMREAD_ANYCOLOR)  # 이미지 형식을 바꿔주고
            # AR_Marker
            markers = detect_markers(img)   #배열을 리턴
            for marker in markers :
                print('detected',marker,id)
                marker.highlite_marker(img)
            cv2.imshow('image', img)  # 이미지를 보여준다
            cv2.waitKey(1)

        else:
            with open('uploaded.jpg', 'wb') as File:
                File.write(data)
                print('Written to file')

        self.wfile.write(
            bytes(json.dumps({"foo": "bar"}), encoding='utf8'))


with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as _httpd:
    httpd = _httpd
    print("HTTPServer Serving at port", PORT)
    httpd.serve_forever()