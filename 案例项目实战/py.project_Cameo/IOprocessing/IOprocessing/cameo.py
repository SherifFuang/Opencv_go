import cv2 
import filters
from managers import WindowManager, CaptureManager  #from import : 从车里把矿泉水拿出来，给我.而import : 把车给我。 在这则是从manager项目中读取win... Cap..两个类

class Cameo(object):
    def __init__(self):
        # 创建一个窗口，并将键盘的回调函数传入
        self._windowManager = WindowManager('Cameo', self.onKeypress)
        # 告诉程序数据来自视频文件， 还镜面翻转效果
        video_path = "C:\\Users\\admin\\Documents\\Visual Studio 2015\\Projects\\Testphoto\\FaceVideo.mp4"
        self._captureManager = CaptureManager(capture=cv2.VideoCapture(video_path), previewWindowManager=self._windowManager, shouldMirrorPreview=True)
        self._curveFilter = filters.BGRPortraCurveFilter()

    def run(self):
        """Run the main loop."""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            # 这里的enterFrame就是告诉程序从视频中读取数据
            self._captureManager.enterFrame()
            # 下面的这个frame是原始帧数据，这里没有做任何修改，后面的教程会对这个帧数据进行修改
            frame = self._captureManager._frame
            if frame is not None:
                
                # TODO: Track faces (Chapter 3).
                
                filters.strokeEdges(frame, frame)
                self._curveFilter.apply(frame, frame)

            self._captureManager.exitFrame()
            self._windowManager.processEvents()
    
            # exitFrame看起来是像是退出的意思，其实主要功能都是在这里方法里实现的，截屏、录像都是在这里
            self._captureManager.exitFrame()
            # 回调函数
            self._windowManager.processEvents()
    # 定义键盘的回调函数，用于self._windowManager.processEvents()的调用
    def onKeypress(self, keycode):
        '''
        快捷键设置：
        当按下“空格”键的时候，会进行抓屏。
        当按下‘tab’键的时候，就开始或者停止录像。
        当然相应的目录也会生成图片或者视频文件
        '''
        if keycode == 32:#space
            # 截屏保存的文件名字
            self._captureManager.writeImage('screenshot.png')
        elif keycode == 9:#tab
            if not self._captureManager.isWritingVideo:
                # 告诉程序，录像保存的文件名字
                self._captureManager.startWritingVideo('screen_record.avi')
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27: #escape
            self._windowManager.destroyWindow()

if __name__=="__main__":
    Cameo().run()