//中值模糊
//
//中值滤波本质上是统计排序滤波器的一种，中值滤波对图像特定噪声类型（椒盐噪声）会取得比较好的去噪效果，也是常见的图像去噪声与增强的方法之一。中值滤波也是窗口在图像上移动，其覆盖的对应ROI区域下，所有像素值排序，取中值作为中心像素点的输出值
//
//OpenCV中值滤波API函数如下：
//medianBlur(
//	InputArray 	src,
//	OutputArray 	dst,
//	int 	ksize // 必须是奇数，而且必须大于1
//)
//
//Python:
//dst = cv.medianBlur(src, ksize[, dst])

#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main(int artc, char** argv) {
	Mat src = imread("D:/sp_noise.png");
	if (src.empty()) {
		printf("could not load image...\n");
		return -1;
	}
	namedWindow("input", CV_WINDOW_AUTOSIZE);
	imshow("input", src);

	Mat dst;
	medianBlur(src, dst, 5);
	imshow("medianblur ksize=5", dst);

	waitKey(0);
	return 0;
}



