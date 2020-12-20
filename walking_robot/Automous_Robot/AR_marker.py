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