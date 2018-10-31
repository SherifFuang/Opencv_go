
//图像直方图均衡化
//图像增强、对输入图像进行直方图均衡化处理，提升后续对象检测的准确率
//在OpenCV人脸检测的代码演示中已经很常见。此外对医学影像图像与卫星遥感图像也经常通过直方图均衡化来提升图像质量。
//API：equalizeHist

#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main(int artc, char** argv) {
	Mat src = imread("C:/Users/admin/Documents/Visual Studio 2015/Projects/Testphoto/flower.png");

	if (src.empty()) {
		printf("could not load image...\n");
		return -1;
	}
	namedWindow("input", CV_WINDOW_AUTOSIZE);
	Mat gray, dst;
	cvtColor(src, gray, COLOR_BGR2GRAY);
	imshow("input", gray);
	equalizeHist(gray, dst);
	imshow("eq", dst);

	waitKey(0);
	return 0;
}



