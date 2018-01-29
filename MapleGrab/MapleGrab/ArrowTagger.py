import PIL.Image, PIL.ImageTk
from tkinter import *
import cv2
import numpy as np
import os
import ParseArrow

PARSE_PATH = ParseArrow.PARSE_PATH
PARSE_NAME = ParseArrow.PARSE_NAME
PARSE_LOG = ParseArrow.PARSE_LOG
TAG_PATH = "./TaggedArrow/"
TAG_LOG = "00TagProgress.txt"


class ArrowTagger:
    def __init__(self):
        print("Let's start tagging...")
        self.root = Tk()
        #self.frame = Frame(self.root,width=300,height=300)
        self.root.bind("<Left>",self.LeftKey)
        self.root.bind("<Right>",self.RightKey)
        self.root.bind("<Up>",self.UpKey)
        self.root.bind("<Down>",self.DownKey)
        self.root.bind("<Button-3>",self.UndoTag)
        self.root.bind("<Button-2>",self.putoff)

        # Variables
        self.left = 0       # Number of each type of images
        self.right = 0
        self.down = 0
        self.up = 0
        self.toTag = 0      # Tag progress
        self.ReadProgress()
        self.log = []       # Working log

        # Open file
        self.workingFile = PARSE_PATH + PARSE_NAME % self.toTag
        self.img = cv2.imread(self.workingFile)
        cv2.namedWindow("Arrow")
        cv2.imshow("Arrow",self.img)


    def UndoTag(self,event):
        print("\tUndo")
        self.toTag -= 1
        last_job = self.log.pop()

        if last_job is 'left':
            self.left -= 1
            os.rename(TAG_PATH+'left_%d.bmp' % self.left, PARSE_PATH + PARSE_NAME % self.toTag)
            self.workingFile = PARSE_PATH + PARSE_NAME % self.toTag
            self.img = cv2.imread(self.workingFile)
            cv2.imshow("Arrow",self.img)
            self.saveProgress()
        elif last_job is 'right':
            self.right -= 1
            os.rename(TAG_PATH+'right_%d.bmp' % self.right, PARSE_PATH + PARSE_NAME % self.toTag)
            self.workingFile = PARSE_PATH + PARSE_NAME % self.toTag
            self.img = cv2.imread(self.workingFile)
            cv2.imshow("Arrow",self.img)
            self.saveProgress()
        elif last_job is 'up':
            self.up -= 1
            os.rename(TAG_PATH+'up_%d.bmp' % self.up, PARSE_PATH + PARSE_NAME % self.toTag)
            self.workingFile = PARSE_PATH + PARSE_NAME % self.toTag
            self.img = cv2.imread(self.workingFile)
            cv2.imshow("Arrow",self.img)
            self.saveProgress()
        elif last_job is 'down':
            self.down -= 1
            os.rename(TAG_PATH+'down_%d.bmp' % self.down, PARSE_PATH + PARSE_NAME % self.toTag)
            self.workingFile = PARSE_PATH + PARSE_NAME % self.toTag
            self.img = cv2.imread(self.workingFile)
            cv2.imshow("Arrow",self.img)
            self.saveProgress()
        print("Now working on: %d" % self.toTag)

    def putoff(self,event):
        print("\t141")
        self.toTag += 1
        self.workingFile = PARSE_PATH + PARSE_NAME % self.toTag
        self.img = cv2.imread(self.workingFile)
        cv2.imshow("Arrow",self.img)
        self.saveProgress()
        print("Now working on: %d" % self.toTag)

    def LeftKey(self,event):
        print("\tLeft Key pressed.")
        os.rename(self.workingFile,TAG_PATH + 'left_%d.bmp' % self.left)
        self.log.append('left')
        self.left += 1
        self.toTag += 1
        self.saveProgress()
        self.workingFile = PARSE_PATH + PARSE_NAME % self.toTag
        self.img = cv2.imread(self.workingFile)
        cv2.imshow("Arrow",self.img)
        print("Now working on: %d" % self.toTag)

    def RightKey(self,event):
        print("\tRight Key pressed.")
        os.rename(self.workingFile,TAG_PATH + 'right_%d.bmp' % self.right)
        self.log.append('right')
        self.right += 1
        self.toTag += 1
        self.saveProgress()
        self.workingFile = PARSE_PATH + PARSE_NAME % self.toTag
        self.img = cv2.imread(self.workingFile)
        cv2.imshow("Arrow",self.img)
        print("Now working on: %d" % self.toTag)

    def UpKey(self,event):
        print("\tUp Key pressed.")
        os.rename(self.workingFile,TAG_PATH + 'up_%d.bmp' % self.up)
        self.log.append('left')
        self.up += 1
        self.toTag += 1
        self.saveProgress()
        self.workingFile = PARSE_PATH + PARSE_NAME % self.toTag
        self.img = cv2.imread(self.workingFile)
        cv2.imshow("Arrow",self.img)
        print("Now working on: %d" % self.toTag)

    def DownKey(self,event):
        print("\tDown Key pressed.")
        os.rename(self.workingFile,TAG_PATH + 'down_%d.bmp' % self.down)
        self.log.append('down')
        self.down += 1
        self.toTag += 1
        self.saveProgress()
        self.workingFile = PARSE_PATH + PARSE_NAME % self.toTag
        self.img = cv2.imread(self.workingFile)
        cv2.imshow("Arrow",self.img)
        print("Now working on: %d" % self.toTag)

    def ReadProgress(self):
        try:
            tag_log = open(TAG_PATH+TAG_LOG,'r')
        except FileNotFoundError:
            print("Tagging log file not found. variables set to 0")
            return

        self.toTag = int(tag_log.readline().replace("\n",""))
        self.left = int(tag_log.readline().replace("\n",""))
        self.right = int(tag_log.readline().replace("\n",""))
        self.up = int(tag_log.readline().replace("\n",""))
        self.down = int(tag_log.readline())

        

    def saveProgress(self):
        print("Save start...")
        f = open(TAG_PATH + TAG_LOG,'w')
        f.write("%d\n" % self.toTag)
        f.write("%d\n" % self.left)
        f.write("%d\n" % self.right)
        f.write("%d\n" % self.up)
        f.write("%d" % self.down)
        print("Save done.")
