#积分图像是Crow在1984年首次提出，是为了在多尺度透视投影中提高渲染速度，是一种快速计算图像区域和与平方和的算法。其核心思想是对每个图像建立自己的积分图查找表，
#在图像积分处理计算阶段根据预先建立的积分图查找表，直接查找从而实现对均值卷积线性时间计算，
#做到了卷积执行的时间与半径窗口大小的无关联。图像积分图在图像特征提取HAAR/SURF、二值图像分析、图像相似相关性NCC计算、图像卷积快速计算等方面均有应用
#图像积分图建立与查找
#在积分图像(Integral Image - ii)上任意位置(x, y)处的ii(x, y)表示该点左上角所有像素之和， 其中(x,y)是图像像素点坐标。
#图一的语音解释

#OpenCV中的相关API如下：
#integral(
#InputArray src, // 输入图像
#OutputArray sum, // 和表
#OutputArray sqsum, // 平方和表
#OutputArray tilted, // 瓦块和表--倾斜的45度的表
#int sdepth = -1, // 和表数据深度常见CV_32S
#int sqdepth = -1 // 平方和表数据深度 常见 CV_32F
#)

import cv2 as cv
import numpy as np


def get_block_sum(ii, x1, y1, x2, y2, index):
    tl = ii[y1, x1][index]
    tr = ii[y2, x1][index]
    bl = ii[y1, x2][index]
    br = ii[y2, x2][index]
    s = (br - bl - tr + tl)
    return s


def blur_demo(image, ii):
    h, w, dims = image.shape
    result = np.zeros(image.shape, image.dtype)
    ksize = 15
    radius = ksize // 2
    for row in range(0, h + radius, 1):
        y2 = h if (row + 1)> h else (row + 1)
        y1 = 0 if (row - ksize) < 0 else (row - ksize)
        for col in range(0, w + radius, 1):
            x2 = w if (col + 1)>w else (col + 1)
            x1 = 0 if (col - ksize) < 0 else (col - ksize)
            cx = 0 if (col - radius) < 0 else (col - radius)
            cy = 0 if (row - radius) < 0 else (row - radius)
            num = (x2 - x1)*(y2 - y1)
            for i in range(0, 3, 1):
                s = get_block_sum(ii, x1, y1, x2, y2, i)
                result[cy, cx][i] = s // num

    cv.imshow("integral fast blur", result)
    cv.imwrite("D:/result.png", result)


src = cv.imread("D:/images/test1.png")
cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
cv.imshow("input", src)
sum_table = cv.integral(src, sdepth=cv.CV_32S)
blur_demo(src, sum_table)

cv.waitKey(0)
cv.destroyAllWindows()

