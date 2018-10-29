import cv2 as cv
import numpy as np
import math


class LaneLineDetection:
    def __init__(self):
        print("instace it")
        self.left_line = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0}
        self.right_line = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0}

    def process(self, frame, method=0):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        binary = cv.Canny(gray, 150, 300)
        h, w = gray.shape
        binary[0:np.int(h/2+40),0:w] = 0
        out_binary, contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        out_image = np.zeros((h, w), frame.dtype)
        for cnt in range(len(contours)):
            # 计算面积与周长
            p = cv.arcLength(contours[cnt], True)
            area = cv.contourArea(contours[cnt])
            x, y, rw, rh = cv.boundingRect(contours[cnt])
            if p < 5 or area < 10:
                continue
            if y > (h - 50):
                continue
            (x, y), (a, b), angle = cv.minAreaRect(contours[cnt]);
            angle = abs(angle)
            if angle < 20 or angle > 160 or angle == 90.0:
                continue
            if len(contours[cnt]) > 5:
                (x, y), (a, b), degree = cv.fitEllipse(contours[cnt])
                if degree< 5 or degree>160 or 80<degree<100:
                    continue
            cv.drawContours(out_image, contours, cnt, (255), 2, 8)
        result = self.fitLines(out_image)
        cv.imshow("contours", out_image)
        dst = cv.addWeighted(frame, 0.8, result, 0.5, 0)
        cv.imshow("lane-lines", dst)

    def fitLines(self, image):
        h, w = image.shape
        h1 = np.int(h / 2 + 40)
        out = np.zeros((h, w, 3), dtype=np.uint8)
        cx = w // 2
        cy = h // 2
        left_pts = []
        right_pts = []
        for col in range(100, cx, 1):
            for row in range(cy, h, 1):
                pv = image[row, col]
                if pv == 255:
                    left_pts.append((col, row))
        for col in range(cx, w-20, 1):
            for row in range(cy, h, 1):
                pv = image[row, col]
                if pv == 255:
                    right_pts.append((col, row))

        if len(left_pts) >= 2:
            [vx, vy, x, y] = cv.fitLine(np.array(left_pts), cv.DIST_L1, 0, 0.01, 0.01)
            y1 = int((-x * vy / vx) + y)
            y2 = int(((w - x) * vy / vx) + y)
            dy = y2 - y1
            dx = w - 1
            k = dy/dx
            c = y1

            w1 = (h1 -c)/k
            w2 = (h - c) / k
            cv.line(out, (np.int(w1), np.int(h1)), (np.int(w2), np.int(h)), (0, 0, 255), 8, 8, 0)
            self.left_line['x1'] = np.int(w1)
            self.left_line['y1'] = np.int(h1)
            self.left_line['x2'] = np.int(w2)
            self.left_line['y2'] = np.int(h)
        else:
            x1 = self.left_line['x1']
            y1 = self.left_line['y1']
            x2 = self.left_line['x2']
            y2 = self.left_line['y2']
            cv.line(out, (x1, y1), (x2, y2), (0, 0, 255), 8, 8, 0)

        if len(right_pts) >= 2:
            x1, y1 = right_pts[0]
            x2, y2 = right_pts[len(right_pts) - 1]
            dy = y2 - y1
            dx = x2 - x1
            k = dy / dx
            c = y1 - k * x1
            w1 = (h1 - c) / k
            w2 = (h - c)/k
            cv.line(out, (np.int(w1), np.int(h1)), (np.int(w2), np.int(h)), (0, 0, 255), 8, 8, 0)
            self.right_line['x1'] = np.int(w1)
            self.right_line['y1'] = np.int(h1)
            self.right_line['x2'] = np.int(w2)
            self.right_line['y2'] = np.int(h)
        else:
            x1 = self.right_line['x1']
            y1 = self.right_line['y1']
            x2 = self.right_line['x2']
            y2 = self.right_line['y2']
            cv.line(out, (x1, y1), (x2, y2), (0, 0, 255), 8, 8, 0)
        return out


def video_run():
    capture = cv.VideoCapture("D:/javaopencv/road_line.mp4")
    height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
    width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    count = capture.get(cv.CAP_PROP_FRAME_COUNT)
    fps = capture.get(cv.CAP_PROP_FPS)
    print(height, width, count, fps)
    detector = LaneLineDetection()
    while (True):
        ret, frame = capture.read()
        if ret is True:
            cv.imshow("video-input", frame)
            detector.process(frame, 0)
            c = cv.waitKey(1)
            if c == 27:
                break
        else:
            break


if __name__ == "__main__":
    video_run()
    cv.waitKey(0)
    cv.destroyAllWindows()


