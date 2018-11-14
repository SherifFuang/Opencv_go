import cv2 as cv
import numpy as np

src = cv.imread("C:\\Users\\admin\\Documents\\Visual Studio 2015\\Projects\\Testphoto\\example.png")
cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
cv.imshow("input", src)

h, w = src.shape[:2]#2的意思是获得高496，宽353.  如果写成[：1]那就是只获得高，
dst = cv.edgePreservingFilter(src, sigma_s=100, sigma_r=0.4, flags=cv.RECURS_FILTER)
cv.imshow("dst", dst)
result = np.zeros([h, w*2, 3], dtype=src.dtype)
result[0:h,0:w,:] = src
result[0:h,w:2*w,:] = dst#把dst图像放在result的右侧，（0，w）点与（h,2*w）点
cv.imshow("result", result)
cv.imwrite("D:/result.png", result)


cv.waitKey(0)
cv.destroyAllWindows()
