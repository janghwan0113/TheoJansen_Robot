from glob import glob
import cv2 
from ar_markers import detect_markers

def AR_marker(img_array):
    markers = detect_markers(img_array)  # 배열을 리턴
    length, id_num = (0, 0)
    for marker in markers:
        crdt_x, crdt_y = ([], [])
        for i in range(4):
            crdt_x.append(marker.contours[i][0][0])
            crdt_y.append(marker.contours[i][0][1])
        marker.highlite_marker(img_array)
        length = max(crdt_x)-min(crdt_x)
        id_num = marker.id
    #print(length, id_num)
    cv2.imshow('img', img_array)
    return length, id_num

class AR_test:
  def __iter__(self):
    self.streaming_obj = iter(sorted(glob('streaming/*.jpg',recursive=True)))
    return self

  def __next__(self):
    path = next(self.streaming_obj)
    print(path)
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    return img

for img in AR_test():
    AR_marker(img)
    #cv2.imshow("Raw", img)
    key = cv2.waitKey(200) & 0xFF  # 에러 방지
    
    
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