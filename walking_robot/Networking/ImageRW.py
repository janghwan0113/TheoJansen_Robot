# https://www.mixedcontentexamples.com
import cv2
import numpy as np
from http.client import HTTPConnection
file = 'steveholt.jpg'
host = '192.168.0.69:8000'

# 라즈베리파이(client)에서 노트북(server)로 보내기


def Upload(body, headers={}):
    conn = HTTPConnection(host)
    # body를 보낸다, 경로를 임의로 설정한다('/').노트북으로 요청이 넘어감
    conn.request('POST', '/', body=body, headers=headers)
    res = conn.getresponse()  # 노트북에서 요청에대한 응답을 보내는데,
    print(res.getheaders())  # 응답 중 헤더부분만가져와서 프린드
    # X-server2CLient 라는 key의 value를 가져오는데 없으면 fallvback을 내보내라.
    print(res.getheader('X-Server2Client', 'Fallback'))
    print(res.read())  # 서버가 보낸 응답의 body부분을 프린트
    print('Uploaded to', host, 'with status', res.status)

# 이미지 다운로드받기


def Download():
    with open(file, 'wb') as File:
        conn = HTTPConnection('www.mixedcontentexamples.com')
        conn.request("GET", "/Content/Test/steveholt.jpg")
        res = conn.getresponse()
        File.write(res.read())
        print('Downloaded to', file)

# 위에서 다운받은 이미지 업로드하기(서버로). Download 함수 실행 후 Upload 함수실행


def DownloadAndUpload():
    Download()
    with open(file, 'rb') as File:
        Upload(File.read())


def UploadNumpy():
    img = 255 * np.random.random((100, 100, 3))  # 코드설명위한 랜덤이미지
    print('shape', img.shape)
    result, img = cv2.imencode(
        '.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])  # image 형식을 jpg로 바꾸는데 quality'90' 설정. img가 배열로 저장됨
    if not result:
        raise Exception('Image encode error')

    Upload(img.tobytes(), {
        "X-Client2Server": "123"
    })  # 이미지를 byte로전달


if __name__ == '__main__':
    # Download()
    # DownloadAndUpload()
    UploadNumpy()
