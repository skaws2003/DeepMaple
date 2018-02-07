import cv2
import glob
import ArrowClassifier

ARROW_PATH = ArrowClassifier.ARROW_PATH
EDGE_PATH = './EdgeArrow/'

class ArrowEdger:
    def __init__(self):
        self.addrs = glob.glob(path+"*.bmp")
        self.cnt = 0
    def Edge(self):
        for addr in self.addrs:
            img = cv2.imread(addr)
            edge = cv2.Canny(img,80,200)
            cv2.imwrite(EDGE_PATH+addr[len(ARROW_PATH):],edge)
            self.cnt += 1
            if self.cnt%0 == 0:
                print('Edge detection:(',self.cnt,'/',len(self.addrs),')')
