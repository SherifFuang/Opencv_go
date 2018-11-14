#图像梯度 – Sobel算子

#卷积的作用除了实现图像模糊或者去噪，还可以寻找一张图像上所有梯度信息，这些梯度信息是图像的最原始特征数据，进一步处理之后就可以生成一些比较高级的特征用来表示一张图像实现基于图像特征的匹配，
#图像分类等应用。Sobel算子是一种很经典的图像梯度提取算子，其本质是基于图像空间域卷积，背后的思想是图像一阶导数算子的理论支持。OpenCV实现了基于Sobel算子提取图像梯度的API，
#dst = cv.Sobel(src, ddepth, dx, dy[, dst[, ksize[, scale[, delta[, borderType]]]]])
import cv2 as cv
import numpy as np

src = cv.imread("D:/images/grad.png")
cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
cv.imshow("input", src)

h, w = src.shape[:2]
x_grad = cv.Sobel(src, cv.CV_32F, 1, 0)
y_grad = cv.Sobel(src, cv.CV_32F, 0, 1)

x_grad = cv.convertScaleAbs(x_grad)#convertScaleAbs是图像增强的函数
y_grad = cv.convertScaleAbs(y_grad)
# cv.imshow("x_grad", x_grad)
# cv.imshow("y_grad", y_grad)

dst = cv.add(x_grad, y_grad, dtype=cv.CV_16S)
dst = cv.convertScaleAbs(dst)
cv.imshow("gradient", dst)

result = np.zeros([h, w*2, 3], dtype=src.dtype)
result[0:h,0:w,:] = src
result[0:h,w:2*w,:] = dst
cv.imshow("result", result)
cv.imwrite("D:/result.png", dst)

cv.waitKey(0)
cv.destroyAllWindows()
