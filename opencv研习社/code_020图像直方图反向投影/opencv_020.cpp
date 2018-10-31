//图像直方图反向投影是通过构建指定模板图像的二维直方图空间与目标的二维直方图空间，进行直方图数据归一化之后， 进行比率操作
//对所有得到非零数值，生成查找表对原图像进行像素映射之后，再进行图像模糊输出的结果。
//直方图反向投影流程：
//- 计算直方图
//- 计算比率r
//- lut查找表
//- 卷积模糊
//- 归一化输出
//
//相关api
//- calcbackproject
//用在什么地方呢？模式匹配、对象识别、视频跟踪  怎么用？实现图像分割，背景与对象分离，对已知对象位置进行定位
//OpenCV中经典算法之一CAMeanShift就是基于反向投影实现对已知对象的位置查找与标记、从而达到连续跟踪
//内容链接：https://blog.csdn.net/jia20003/article/details/73136986
//https://blog.csdn.net/keith_bb/article/details/70154219

#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

const int bins = 256;
Mat src;
const char* winTitle = "input image";
void backProjection_demo(Mat &image, Mat &model);
int main(int argc, char** argv) {
	Mat src = imread("C:/Users/admin/Documents/Visual Studio 2015/Projects/Testphoto/target.png");
	Mat model = imread("C:/Users/admin/Documents/Visual Studio 2015/Projects/Testphoto/sample.png");
	//判断图像是否加载成功
	if (src.empty() || model.empty()) {
		printf("could not load image...\n");
		return 0;
	}
	namedWindow(winTitle, WINDOW_AUTOSIZE);
	imshow(winTitle, src);
	imshow("model", model);

	backProjection_demo(src, model);
	waitKey(0);
	return 0;
}

void backProjection_demo(Mat &image, Mat &model) {
	//把图像转为HSV图像
	Mat model_hsv, image_hsv;
	cvtColor(model, model_hsv, COLOR_BGR2HSV);
	cvtColor(image, image_hsv, COLOR_BGR2HSV);

	// 定义直方图参数与属性
	int h_bins = 32; int s_bins = 32;
	int histSize[] = { h_bins, s_bins };
	// hue varies from 0 to 179, saturation from 0 to 255
	float h_ranges[] = { 0, 180 };//初始化数组，表明有两个数组元素
	float s_ranges[] = { 0, 256 };
	const float* ranges[] = { h_ranges, s_ranges };//直方图中每个维度bin的取值范围 
	int channels[] = { 0, 1 };
	Mat roiHist;
	//计算图像直方图并归一化处理
	calcHist(&model_hsv, 1, channels, Mat(), roiHist, 2, histSize, ranges, true, false);
	normalize(roiHist, roiHist, 0, 255, NORM_MINMAX, -1, Mat());
	
	//获取反向投影
	MatND backproj;
	calcBackProject(&image_hsv, 1, channels, roiHist, backproj, ranges, 1.0);
	//输出反向投影
	imshow("BackProj", backproj);
	
	////绘制图像直方图
	//int w = 400;
	//int h = 400;
	//int bin_w = cvRound((double)w/histSize[1]);
	//Mat histImage = Mat::zeros(w, h, CV_8UC3);
	//for (int i = 0; i < 30; i++)
	//{
	//	rectangle(histImage, Point(i*bin_w, h), Point((i + 1)*bin_w, h - cvRound(roiHist.at<float>(i)*h / 255.0)), Scalar(0, 0, 255), -1);
	//}
	//imshow("HistImage", histImage);

}