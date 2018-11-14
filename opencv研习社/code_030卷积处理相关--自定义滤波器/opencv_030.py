#dst=cv.filter2D(src, ddepth, kernel[, dst[, anchor[, delta[, borderType]]]]	)
#
#int ddepth, // 默认-1，表示输入与输出图像类型一致，但是当涉及浮点数计算时候，需要设置为CV_32F。滤波完成之后需要使用convertScaleAbs函数将结果转换为字节类型。

import cv2 as cv
import numpy as np

src = cv.imread("D:/images/test.png")
cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
cv.imshow("input", src)

blur_op = np.ones([5, 5], dtype=np.float32)/25.#自定义模糊的卷积核
shape_op = np.array([[0, -1, 0],#自定义锐化的卷积核
                   [-1, 5, -1],
                   [0, -1, 0]], np.float32)
grad_op = np.array([[1, 0],[0, -1]], dtype=np.float32)#自定义梯度的卷积核

dst1 = cv.filter2D(src, -1, blur_op)
dst2 = cv.filter2D(src, -1, shape_op)
dst3 = cv.filter2D(src, cv.CV_32F, grad_op)
dst3 = cv.convertScaleAbs(dst3)

cv.imshow("blur=5x5", dst1);
cv.imshow("shape=3x3", dst2);
cv.imshow("gradient=2x2", dst3);

cv.waitKey(0)
cv.destroyAllWindows()

