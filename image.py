import cv2
url='http://172.32.0.238:8080/video'

cap = cv2.VideoCapture(url)

while True:
    ret, frame=cap.read()
    if frame is not None:
        cv2.imshow('frame', frame)
    q=cv2.waitKey(1)
    if q == ord('q'):
        break

cv2.destroyAllWindows()