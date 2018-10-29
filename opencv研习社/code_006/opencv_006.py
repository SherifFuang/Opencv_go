import cv2 as cv

src = cv.imread("D:/vcprojects/images/test.png")
cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
cv.imshow("input", src)
dst = cv.applyColorMap(src, cv.COLORMAP_COOL)
cv.imshow("output", dst)

# 伪色彩
image = cv.imread("D:/gloomyfish/canjian.jpg")
color_image = cv.applyColorMap(image, cv.COLORMAP_JET)
cv.imshow("image", image)
cv.imshow("color_image", color_image)
cv.waitKey(0)
cv.destroyAllWindows()


