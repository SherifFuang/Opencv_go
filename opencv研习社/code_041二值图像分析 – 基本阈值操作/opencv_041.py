import cv2 as cv
import numpy as np
#
# THRESH_BINARY = 0
# THRESH_BINARY_INV = 1
# THRESH_TRUNC = 2
# THRESH_TOZERO = 3
# THRESH_TOZERO_INV = 4
#
src = cv.imread("C:\\Users\\admin\\Documents\\Visual Studio 2015\\Projects\\Testphoto\\cat_test.png")
cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
cv.imshow("input", src)

T = 100

# 转换为灰度图像
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
for i in range(5):
    ret, binary = cv.threshold(gray, T, 255, i)#看参数提醒，它会返回两个值，一个是retval，一个是dst
    

cv.waitKey(0)
cv.destroyAllWindows()


