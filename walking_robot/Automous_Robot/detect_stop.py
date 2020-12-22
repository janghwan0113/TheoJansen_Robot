import cv2


def detect_stop(img_array):
    face_cascade = cv2.CascadeClassifier('./cascade3.xml')
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    objs = face_cascade.detectMultiScale(gray, 1.3, 5)

    if (len(objs)):
        length = objs[0][3]
        for (x, y, w, h) in objs:
            cv2.rectangle(img_array, (x, y), (x+w, y+h), (255, 0, 0), 2)
    else:
        length = 0
    cv2.imshow('Stop', img_array)
    # print(length)

    return length
