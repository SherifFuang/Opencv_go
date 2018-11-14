#使用managers.CaptureManager提取视频流
import numpy as np
import cv2 as cv
import time 

# 增加要导入的包、构造函数和属性值
class CaptureManager(object): 
    def __init__(self, capture, previewWindowManager = None, shouldMirrorPreview = False):#这个怎么会有这么多属性值，哪里来的
        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview
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
       
    @property
    def channel(self):
        return self._channel
    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None
    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve()
        return self._frame
    @property
    def isWritingImage(self):
        return self._imageFilename is not None
    @property
    def isWritingVideo(self):
        return self._videoFilename is not None
 
    def enterFrame(self):
        assert not self._enteredFrame, 'previous enterFrame() had no matching exitFram()'
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()
    def exitFrame(self):
        if self.frame is None:
            self._enteredFrame = False
            return
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirroredFrame = numpy.fliplr(self._frame).copy()
                self.previewWindowManager.show(mirroredFrame)
            else:
                self.previewWindowManager.show(self._frame)
        if self.isWritingImage:
            cv2.imwrite(self._imageFilename, self._frame)
            self._imageFilename = None
        self._writerVideoFrame()
        self._frame = None
        self._enteredFrame = False
 
    def writeImage(self, filename):
        self._imageFilename = filename
    def startWritingVideo(self, filename, encoding = cv2.VideoWriter_fourcc('I', '4', '2', '0')):
        self._videoFilename = filename
        self._videoEncoding = encoding
    def stopWritingVideo(self):
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None
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
          

