import MapleImage
import os
import cv2
from tkinter import *

CAPTURE_PATH = "./CapturedData/"
CAPTURE_NAME = "miniGame_%d_%d.bmp"
CAPTURE_LOG = "NumCapture.txt"

class Front:
    save_path = CAPTURE_PATH
    def __init__(self):
        # UI initialization
        self.root= Tk()
        self.frame = Frame(self.root, width=300, height=300)
        self.frame.bind("<Button-3>", self.right)
        self.frame.bind("<Button-2>", self.middle)
        self.frame.bind("<Button-1>", self.left)
        self.frame.pack()

        # Object for screenshot
        self.map = MapleImage.MapleCapture()
        
        # Screenshot number
        self.numCapture = 0

        # Give data set number
        self.setNum = 0
        try:
            log_file = open(CAPTURE_PATH + CAPTURE_LOG,'r')
            line = log_file.readline()
            if not line:
                self.setNum = 0
                print("Something went wrong with the log file! setNum set to 0")
            else:
                line.replace("\n","")
                self.setNum = int(line) + 1
                print("Progress read! Data set number: %d" % self.setNum)
            log_file.close()
        except FileNotFoundError:
            self.setNum = 0
            print("No existing progress. Data set number set to 0")

        # Save data set number
        log_write = open(Front.save_path + "NumCapture.txt",'w')
        log_write.write("%d" % self.setNum)
        log_write.close()


    def left(self,event):
        """
        Handles left click. Captures the screen.
        Returns the label of the capture just captured.
        """
        img = self.map.capture_all()
        cv2.imwrite(CAPTURE_PATH + CAPTURE_NAME % (self.setNum, self.numCapture), img)
        print("Saved!: number %d" % self.numCapture)
        self.numCapture += 1
        return self.numCapture

    def right(self,event):
        """
        Handles right click. Undo last capture.
        Returns the label of the capture deleted.
        """
        if self.numCapture <= 1:
            print("No files to delete")
            return None
        os.remove(CAPTURE_PATH + CAPTURE_NAME % (self.setNum, self.numCapture-1))
        self.numCapture -= 1
        print("Deleted")
        return self.numCapture

    def middle(self,event):
        """
        Handles scroll button. Adjusts the position of the window.
        """
        pos = self.map.set_window_pos()
        if pos == None:
            print("Cannot find window.")
        else:
            print("Adjustment factor set to",pos)