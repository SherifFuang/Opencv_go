import numpy 
import cv2 
import time 
#使用managers.CaptureManager提取视频流
# 增加要导入的包、构造函数和属性值
class CaptureManager(object): 
# 类变量前加 _ 代表将变量设置保护变量，只有类对象和子类才能访问
# 类变量前加 __ 代表将变量设置私有变量，只有类对象才能访问
    def __init__(self, capture, previewWindowManager = None, shouldMirrorPreview = False):#高级的I/O流接口，可以获取帧并分配输出，shouldMirrorPreview是否镜像，previewWindowManager退出frame之前是否要在窗口中显示帧属性
       #CaptureManager类被定义了三个参数，分别为输入视频流，输出的窗口以及镜像参数。
        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview  =  shouldMirrorPreview
        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFilename = None
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None
        self._startTime = None
        self._framesElapsed = int(0)
        self._fpsEstimate = None
       
    # 设置窗口只读属性
    @property
    def channel(self):#获取通道属性
        return self._channel
    # 设置可写属性
    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None
            
    # 设置帧只读属性
    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve()
        return self._frame
    
    # 设置只读属性
    @property
    def isWritingImage(self):
        return self._imageFilename is not None
    @property
    def isWritingVideo(self):
        return self._videoFilename is not None


 # 启动摄像头录制功能
    def enterFrame(self):#进入帧，只能同步获取一帧
        #capture the next frame if any，but first check whether that any previous frame was exited
        # 第一步，检查是否有之前帧存在
        assert not self._enteredFrame, 'previous enterFrame() had no matching exitFram()'
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

# 程序里最复杂的就是这方法了，担负了视频显示、视频录制、截屏保存的功能。
    def exitFrame(self):#退出帧
        """draw to the window write to files , Release the frame"""   
        #check whether any grabbed frame is retrievable. the getter may retrieve and cache frame 
        # 检查是否有捕获的帧是可获取的
        # getter可能获取并缓存帧
        if self.frame is None:
            self._enteredFrame = False
            return
         # 更新帧估计和相关变量
        if self._framesElapsed == 0:
            self._startTime = time.time()#time.time()是python 中专门用来估测帧速率的
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1
        if self.previewWindowManager is not None: #通过窗口管理器（如果有）显示图像
            if self.shouldMirrorPreview:
                mirroredFrame = numpy.fliplr(self._frame).copy()
                self.previewWindowManager.show(mirroredFrame)
            else:
                self.previewWindowManager.show(self._frame)
        #write to the image file ,if any 写入图像到文件
        if self.isWritingImage:
            cv2.imwrite(self._imageFilename, self._frame)
            self._imageFilename = None
        #write to the video file, if any 录像生成
        self._writerVideoFrame()
        #release the frame 
        self._frame = None
        self._enteredFrame = False
 

        # 设置图片文件名
    def writeImage(self, filename):
        self._imageFilename = filename
        # 开始录制
    def startWritingVideo(self, filename, encoding = cv2.VideoWriter_fourcc('I', '4', '2', '0')):
        
        self._videoFilename = filename
        self._videoEncoding = encoding
        # 开始录制
    def stopWritingVideo(self):
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None
        
    # 录制视频
    def _writerVideoFrame(self):
        if not self.isWritingVideo:
            return
        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps == 0.0:
                if self._framesElapsed < 20:
                    return
                else:
                    fps = self._fpsEstimate
            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv2.VideoWriter(self._videoFilename, self._videoEncoding,fps,size)
            self._videoWriter.write(self._frame)
          
# 使用managers.WindowManager抽象窗口和键盘
# 创建界面管理类
class WindowManager(object):
    # 实现支持键盘事件
    def __init__(self, windowName, keypressCallback = None):
        self.keypressCallback = keypressCallback
        self._windowName = windowName   
        self._isWindowCreated = False
    # 设置只读属性
    @property
    def isWindowCreated(self):
        return self._isWindowCreated
    # 创建窗口
    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True
    # 显示窗口
    def show(self, frame):
        cv2.imshow(self._windowName, frame)
    # 注销窗口
    def destoryWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False
     # 执行键盘操作的回调函数
    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            keycode &= 0xFF
            self.keypressCallback(keycode)