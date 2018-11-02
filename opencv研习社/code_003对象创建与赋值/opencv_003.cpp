#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main(int artc, char** argv) {
	Mat src = imread("D:/vcprojects/images/test.png");
	if (src.empty()) {
		printf("could not load image...\n");
		return -1;
	}
	namedWindow("input", CV_WINDOW_AUTOSIZE);
	imshow("input", src);

    // 创建方法 - 克隆
	Mat m1 = src.clone();

	// 复制
	Mat m2;
	src.copyTo(m2);

	// 赋值法
	Mat m3 = src;

	// 创建空白图像
	Mat m4 = Mat::zeros(src.size(), src.type());//创建一个数据大小类型都一样的
	Mat m5 = Mat::zeros(Size(512, 512), CV_8UC3);//创建空白图像，宽512，高512，CV_8UC3是3通道的字节类型
	Mat m6 = Mat::ones(Size(512, 512), CV_8UC3);

	Mat kernel = (Mat_<char>(3, 3) << 0, -1, 0,//char类型的3*3数组
		-1, 5, -1,
		0, -1, 0);

	waitKey(0);
	return 0;
}
