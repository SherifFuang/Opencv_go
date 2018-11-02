import cv2 as cv
import numpy as np

src = cv.imread("C:\\Users\\admin\\Documents\\Visual Studio 2015\\Projects\\Testphoto\\test.png")
cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
cv.imshow("input", src)

# 克隆图像
m1 = np.copy(src)

# 赋值
x = np.empty([3,2],dtype = int) #numpy.empty 方法用来创建一个指定形状（shape）、数据类型（dtype）且未初始化的数组：
print(x)#[3,2]是三行二列？

m2 = src
src[100:200,200:300,:] = 255 #。部分窗口可以改颜色，起点从100-200，宽度200至300
cv.imshow("m2",m2)

m3 = np.zeros(src.shape, src.dtype)#numpy.zeros,创建指定大小的数组，数组元素以 0 来填充：
cv.imshow("m3", m3)

m4 = np.zeros([512,512], np.uint8)
m4[0:128,128:256] =127 # try to give gray value 127
cv.imshow("m4", m4)

m5 = np.ones(shape=[256,512,3], dtype=np.uint8)#numpy.ones创建指定形状的数组，数组元素以 1 来填充：256*512高宽大小 3通道[256,512,3]
m5[:,:,1] = 255 #其中0表示r通道， 且赋值255值。   前面两个:,:,感觉就是对前面的512,512不改动
cv.imshow("m5", m5)

cv.waitKey(0)
cv.destroyAllWindows()

