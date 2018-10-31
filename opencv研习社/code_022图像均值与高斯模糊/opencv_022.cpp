////图像均值与高斯模糊
//
//均值模糊 是卷积核的系数完全一致，
//高斯模糊考虑了中心像素距离的影响，对距离中心像素使用高斯分布公式生成不同的权重系数给卷积核，然后用此卷积核完成图像卷积得到输出结果就是图像高斯模糊之后的输出。
//
//OpenCV高斯模糊 API函数
//void GaussianBlur(
//	InputArray src,
//	OutputArray dst,
//	Size ksize, // Ksize为高斯滤波器窗口大小
//	double sigmaX, // X方向滤波系数
//	double sigmaY = 0, // Y方向滤波系数
//	int borderType = BORDER_DEFAULT // 默认边缘插值方法
//)
//当Size(0, 0)就会从sigmax开始计算生成高斯卷积核系数，当时size不为零是优先从size开始计算高斯卷积核系数
// 图像模糊的本质, 从数字信号处理的角度看，图像模糊就要压制高频信号保留低频信号，
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

	Mat dst1, dst2;
	blur(src, dst1, Size(5, 5), Point(-1, -1), 4);
	GaussianBlur(src, dst2, Size(5, 5), 15, 0, 4);


	imshow("blur", dst1);
	imshow("gaussian blur", dst2);

	waitKey(0);
	return 0;
}



