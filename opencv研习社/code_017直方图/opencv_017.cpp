//直方图的使用

#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

const int bins = 256;
Mat src;
const char* winTitle = "input image";//定义一个指向字符常数的指针
void showHistogram();
int main(int argc, char** argv) {// char **为二级指针
	src = imread("D:/vcprojects/images/flower.png");
	if (src.empty()) {
		printf("could not load image...\n");
		return 0;
	}
	namedWindow(winTitle, WINDOW_AUTOSIZE);
	imshow(winTitle, src);
	showHistogram();
	waitKey(0);
	return 0;
}


void showHistogram() {
	// 三通道分离
	vector<Mat> bgr_plane;//vector是向量数据结构，相当于一个动态数组，在这是等于设置了一个Mat数组
	split(src, bgr_plane);//split是通道分离函数，bgr_plane是Mat数组的首地址
	// 定义参数变量
	const int channels[1] = { 0 };
	const int bins[1] = { 256 };//直接bins={256}就行了，为啥还要加个[1] ，bins是竖条的个数
	float hranges[2] = { 0,255 };//这里为什么要用[2]
	const float* ranges[1] = { hranges };//啥意思？
	Mat b_hist;
	Mat g_hist;
	Mat r_hist;
	// 计算Blue, Green, Red通道的直方图
	calcHist(&bgr_plane[0], 1, 0, Mat(), b_hist, 1, bins, ranges);//&bgr_plane[0]为输入图像的指针，[0]中0对应蓝色通道，后面1对应绿色，2对应红色，
	calcHist(&bgr_plane[1], 1, 0, Mat(), g_hist, 1, bins, ranges);
	calcHist(&bgr_plane[2], 1, 0, Mat(), r_hist, 1, bins, ranges);
	// 显示直方图
	int hist_w = 512;
	int hist_h = 400;
	int bin_w = cvRound((double)hist_w / bins[0]);//cvRound浮点数取整
	Mat histImage = Mat::zeros(hist_h, hist_w, CV_8UC3);
	// 归一化直方图数据-----------------归一化就是要把需要处理的数据经过处理后（通过某种算法）限制在你需要的一定范围内
	normalize(b_hist, b_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat());
	normalize(g_hist, g_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat());
	normalize(r_hist, r_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat());
	// 绘制直方图曲线
	for (int i = 1; i < bins[0]; i++) {
		line(histImage, Point(bin_w*(i - 1), hist_h - cvRound(b_hist.at<float>(i - 1))),
			Point(bin_w*(i), hist_h - cvRound(b_hist.at<float>(i))), Scalar(255, 0, 0), 2, 8, 0);
		line(histImage, Point(bin_w*(i - 1), hist_h - cvRound(g_hist.at<float>(i - 1))),
			Point(bin_w*(i), hist_h - cvRound(g_hist.at<float>(i))), Scalar(0, 255, 0), 2, 8, 0);
		line(histImage, Point(bin_w*(i - 1), hist_h - cvRound(r_hist.at<float>(i - 1))),
			Point(bin_w*(i), hist_h - cvRound(r_hist.at<float>(i))), Scalar(0, 0, 255), 2, 8, 0);
	}
	// 显示直方图
	namedWindow("Histogram Demo", WINDOW_AUTOSIZE);
	imshow("Histogram Demo", histImage);
}

