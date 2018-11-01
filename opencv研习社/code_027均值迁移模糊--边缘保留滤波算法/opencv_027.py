import cv2 as cv
import numpy as np

src = cv.imread("D:/images/example.png")
cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
cv.imshow("input", src)

h, w = src.shape[:2]
dst = cv.pyrMeanShiftFiltering(src, 15, 30, termcrit=(cv.TERM_CRITERIA_MAX_ITER+cv.TERM_CRITERIA_EPS, 5, 1))
result = np.zeros([h, w*2, 3], dtype=src.dtype)
result[0:h,0:w,:] = src
result[0:h,w:2*w,:] = dst
cv.imshow("result", result)
cv.imwrite("D:/result.png", result)


cv.waitKey(0)
cv.destroyAllWindows()
