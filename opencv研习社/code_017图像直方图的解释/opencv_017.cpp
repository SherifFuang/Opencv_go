////图像直方图--
//讲的就是其统计学特征， 
//Bins是指直方图的大小范围， 对于像素值取值在0～255之间的，最少有256个bin，此外还可以有16、32、48、128等，256除以bin的大小应该是整数倍----- 说白了直方图横坐标就是bins。
//优点：图像平移、旋转、缩放时保持不变性，
//用在哪呢：灰度图像的阈值分割、基于颜色的图像检索以及图像分类、反向投影跟踪
//OpenCV中相关API
//calcHist(&bgr_plane[0], 1, 0, Mat(), b_hist, 1, bins, ranges);
//cv.calcHist([image], [i], None, [256], [0, 256])
//
//&rgbPlanes[0]: 输入数组(或数组集)
//1 : 输入数组的个数(这里我们使用了一个单通道图像，我们也可以输入数组集)
//0 : 需要统计的通道(dim)索引 ，这里我们只是统计了灰度(且每个数组都是单通道)所以只要写 0 就行了。
//Mat() : 掩码(0 表示忽略该像素)， 如果未定义，则不使用掩码
//redHist : 储存直方图的矩阵
//	1 : 直方图维数
//	histSize : 每个维度的bin数目
//	histRange : 每个维度的取值范围
//	uniform 和 accumulate : bin大小相同，清楚直方图痕迹

#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

const int bins = 256;
Mat src;
const char* winTitle = "input image";//定义一个指向字符常数的指针
void showHistogram();
int main(int argc, char** argv) {// char **为二级指针
	src = imread("C:/Users/admin/Documents/Visual Studio 2015/Projects/Testphoto/flower.png");
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
	const int channels[1] = { 0 };//好像没用上
	const int bins[1] = { 256 };//直接bins={256}就行了，为啥还要加个[1] ，bins是竖条的个数
	float hranges[2] = { 0,255 };//有两个元素的数组
	const float* ranges[1] = { hranges };//弄数组的数组出来，  const float*p。其实是指针的声明，意思是：p是浮点型的指针（还是常量的）
	Mat b_hist;
	Mat g_hist;
	Mat r_hist;
	// 计算Blue, Green, Red通道的直方图
	calcHist(&bgr_plane[0], 1, 0, Mat(), b_hist, 1, bins, ranges);//&bgr_plane[0]为输入图像的指针，[0]中0对应蓝色通道，后面1对应绿色，2对应红色，
	calcHist(&bgr_plane[1], 1, 0, Mat(), g_hist, 1, bins, ranges);//参数ranges：指出bin的范围的数组的数组，因为后面的uniform标志为true，也就是均匀直方图，所以每一维由一个两个元素的数组指出上下限；
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
	for (int i = 1; i < bins[0]; i++) {//不知道它这个起点终点怎么确定的
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

