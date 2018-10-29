import cv2 as cv

image = cv.imread("D:/vcprojects/images/three.png")
h, w = image.shape[:2]
detector = cv.CascadeClassifier(cv.data.haarcascades +
                                "haarcascade_frontalface_default.xml")
faces = detector.detectMultiScale(image, scaleFactor=1.1,
                                  minNeighbors=3, minSize=(30, 30), maxSize=(w//2, h//2))
for x, y, w, h in faces:
    cv.rectangle(image, (x,y), (x+w, y+h), (0, 0, 255), 2, 8, 0)

cv.imshow("result", image)
cv.waitKey(0)
cv.destroyAllWindows()


