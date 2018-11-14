import cv2 as cv

src = cv.imread("D:/vcprojects/images/cat.jpg")
cv.namedWindow("rgb", cv.WINDOW_AUTOSIZE)
cv.imshow("rgb", src)

# RGB to HSV
hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
cv.imshow("hsv", hsv)

# RGB to YUV
yuv = cv.cvtColor(src, cv.COLOR_BGR2YUV)
cv.imshow("yuv", yuv)

# RGB to YCrCb
ycrcb = cv.cvtColor(src, cv.COLOR_BGR2YCrCb)
cv.imshow("ycrcb", ycrcb)

src2 = cv.imread("D:/javaopencv/tinygreen.png");
cv.imshow("src2", src2)
hsv = cv.cvtColor(src2, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv, (35, 43, 46), (99, 255, 255))#色彩范围，(35, 43, 46)下边界， (99, 255, 255)上边界，有那个范围表  ，不在范围内都像素点都变为0，范围内的变为255
cv.imshow("mask", mask)

cv.waitKey(0)
cv.destroyAllWindows()

#RGB与设备无关的色彩空间
#HSV用于直方图相关时好用，
#YUV 早期欧洲电视的标准， 安卓的摄像头也是用YUV
#YCrCb用于皮肤检测，对有色人种比较好




