////图像噪声
//
//图像噪声产生的原因很复杂，有的可能是数字信号在传输过程中发生了丢失或者受到干扰，有的是成像设备或者环境本身导致成像质量不稳定，反应到图像上就是图像的亮度与颜色呈现某种程度的不一致性。从噪声的类型上，常见的图像噪声可以分为如下几种：
//
//- 椒盐噪声，
//是一种随机在图像中出现的稀疏分布的黑白像素点， 对椒盐噪声一种有效的去噪手段就是图像中值滤波
//
//- 高斯噪声 / 符合高斯分布
//一般会在数码相机的图像采集(acquisition)阶段发生, 这个时候它的物理 / 电 / 光等各种信号都可能导致产生高斯分布噪声。
//
//- 均匀分布噪声
//均匀 / 规则噪声一般都是因为某些规律性的错误导致的
//
//代码演示
//- 图像椒盐噪声生成
//- 图像高斯噪声生成

#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

void add_salt_pepper_noise(Mat &image);
void gaussian_noise(Mat &image);
int main(int artc, char** argv) {
	Mat src = imread("D:/vcprojects/images/cos.jpg");
	if (src.empty()) {
		printf("could not load image...\n");
		return -1;
	}
	namedWindow("input", CV_WINDOW_AUTOSIZE);
	imshow("input", src);
	gaussian_noise(src);

	waitKey(0);
	return 0;
}

void add_salt_pepper_noise(Mat &image) {
	RNG rng(12345);
	int h = image.rows;
	int w = image.cols;
	int nums = 10000;
	for (int i = 0; i < nums; i++) {
		int x = rng.uniform(0, w);
		int y = rng.uniform(0, h);
		if (i % 2 == 1) {
			image.at<Vec3b>(y, x) = Vec3b(255, 255, 255);
		}
		else {
			image.at<Vec3b>(y, x) = Vec3b(0, 0, 0);
		}
	}
	imshow("salt pepper", image);
}

void gaussian_noise(Mat &image) {
	Mat noise = Mat::zeros(image.size(), image.type());
	randn(noise, (15, 15, 15), (30, 30, 30));
	Mat dst;
	add(image, noise, dst);
	imshow("gaussian noise", dst);
}
