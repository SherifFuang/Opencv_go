//查找表参考解释：https://blog.csdn.net/jameshater/article/details/50759650
//按我的理解就是：通过查找表，简单理解为映射函数，就是一种对应关系，对着这个表来变。 比如原图中灰度为0-100的都会变为新图中灰度0， 100-200变成1，200以上变成2.  这样新图只有三个灰度级，
//也可以这么说，查找表是简单的查询操作替换运行时计算的数组，在图像处理中，查找表经常称为LUT，它们将索引号与输出值建立联系。颜色表作为一种普通的 LUT 是用来确定特定图像所要显示的颜色和强度。
#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;
void customColorMap(Mat &image);
int main(int argc, const char *argv[])
{
	Mat src = imread("C:\\Users\\admin\\Documents\\Visual Studio 2015\\Projects\\Testphoto\\daopian.png");
	if (src.empty())
	{
		printf("could not load image...\n");
		return -1;
	}
	Mat gray, dst;
	// 使用LUT
	applyColorMap(src, dst, COLORMAP_SUMMER);
	// 显示结果
	imshow("colorMap", dst);

	cvtColor(src, gray, COLOR_BGR2GRAY);
	imshow("gray", gray);
	customColorMap(gray);

	waitKey(0);
	return 0;
}

void customColorMap(Mat &image) {
	int lut[256];
	for (int i = 0; i < 256; i++) {
		if (i < 127)
			lut[i] = 0;
		else
			lut[i] = 255;
	}

	int h = image.rows;
	int w = image.cols;
	for (int row = 0; row < h; row++) {
		for (int col = 0; col < w; col++) {
			int pv = image.at<uchar>(row, col);
			image.at<uchar>(row, col) = lut[pv];
		}
	}
	imshow("lut demo", image);
}

