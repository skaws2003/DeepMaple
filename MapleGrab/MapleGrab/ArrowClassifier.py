import MapleImage
import ArrowTagger
import os
import cv2
import time
from tkinter import *

TAG_PATH = ArrowTagger.TAG_PATH
TAG_LOG = ArrowTagger.TAG_LOG
TMP_PATH = './tmp/'
ARROW_PATH = './Arrow/'
ARROW_LOG = '00numClass.txt'


class ArrowClassifier:
    def __init__(self):
        print("Let's start tagging...")
        self.root = Tk()
        self.root.bind("<Left>",self.LeftKey)       # Full arrow
        self.root.bind("<Right>",self.RightKey)     # Empty arrow
        self.root.bind("<Button-3>",self.UndoTag)

        # Variables
        self.left = 0       # Working progress
        self.right = 0
        self.up = 0
        self.down = 0
        self.full = 0       # Number of type arrows
        self.empty = 0
        self.left_full = 0      # Num classified arrows
        self.right_full = 0
        self.up_full = 0
        self.down_full = 0
        self.left_empty = 0
        self.right_empty = 0
        self.up_empty = 0
        self.down_empty = 0
        self.pended = 0     # Number of undo arrows
        self.max_left = 0   # Number of files needed to be tagged
        self.max_right = 0
        self.max_up = 0
        self.max_down = 0
        self.log = []       # Working log

        self.ReadWhatToDo()     # Restore working progress
        self.ReadProgress()

        # Initial setup
        self.workingFile = self.GetFilename()
        img = cv2.imread(self.workingFile)
        cv2.imshow("Arrow",img)

    def UndoTag(self,event):
        print("\tUndo")
        self.toTag -= 1
        last_job = self.log.pop()
        if last_job is 'full':
            self.full -= 1
            os.rename(ARROW_PATH+str(self.full),'./tmp/arr%d.bmp'%self.pended)
            self.pended += 1
            self.workingFile = self.GetFilename()
            self.saveProgress()
            img = cv2.imread(self.workingFile)
            cv2.imshow("Arrow",img)
            print("Now working on: %s"%self.workingFile)
        if last_job is 'empty':
            self.empty -= 1
            os.rename(ARROW_PATH+str(self.empty),'./tmp/arr%d.bmp'%self.pended)
            self.pended += 1
            self.workingFile = self.GetFilename()
            self.saveProgress()
            img = cv2.imread(self.workingFile)
            cv2.imshow("Arrow",img)
            print("Now working on: %s"%self.workingFile)

    def LeftKey(self,event):
        print("\tLeft Key pressed. Full arrow.")
        changed_filename = ARROW_PATH + "full_"
        if 'left' in self.workingFile:
            changed_filename = changed_filename + 'left_' + str(self.left_full) + '.bmp'
            self.left_full += 1
        elif 'right' in self.workingFile:
            changed_filename = changed_filename + 'right_' + str(self.right_full) + '.bmp'
            self.right_full += 1
        elif 'up' in self.workingFile:
            changed_filename = changed_filename + 'up_' + str(self.up_full) + '.bmp'
            self.up_full += 1
        elif 'down' in self.workingFile:
            changed_filename = changed_filename + 'down_' + str(self.down_full) + '.bmp'
            self.down_full += 1
        os.rename(self.workingFile, changed_filename)
        self.full += 1
        self.log.append('full')
        self.workingFile = self.GetFilename()
        self.saveProgress()
        img = cv2.imread(self.workingFile)
        cv2.imshow("Arrow",img)
        print("Now working on: %s"%self.workingFile)

    def RightKey(self,event):
        print("\tRight Key pressed. Empty arrow")
        changed_filename = ARROW_PATH + "empty_"
        if 'left' in self.workingFile:
            changed_filename = changed_filename + 'left_' + str(self.left_empty) + '.bmp'
            self.left_empty += 1
        elif 'right' in self.workingFile:
            changed_filename = changed_filename + 'right_' + str(self.right_empty) + '.bmp'
            self.right_empty += 1
        elif 'up' in self.workingFile:
            changed_filename = changed_filename + 'up_' + str(self.up_empty) + '.bmp'
            self.up_empty += 1
        elif 'down' in self.workingFile:
            changed_filename = changed_filename + 'down_' + str(self.down_empty) + '.bmp'
            self.down_empty += 1
        os.rename(self.workingFile, changed_filename)
        self.empty += 1
        self.log.append('empty')
        self.workingFile = self.GetFilename()
        self.saveProgress()
        img = cv2.imread(self.workingFile)
        cv2.imshow("Arrow",img)
        print("Now working on: %s"%self.workingFile)


    def ReadWhatToDo(self):
        try:
            tag_log = open(TAG_PATH+TAG_LOG,'r')
        except FileNotFountError:
            print("Something happened to the arrow direction log file.")
            exit(1)

        tag_log.readline()
        self.max_left = int(tag_log.readline().replace("\n",""))
        self.max_right = int(tag_log.readline().replace("\n",""))
        self.max_up = int(tag_log.readline().replace("\n",""))
        self.max_down = int(tag_log.readline().replace("\n",""))

    def GetFilename(self):
        if self.left < self.max_left:
            filename = TAG_PATH + "left_%d.bmp"%self.left
            self.left += 1
            return filename
        if self.right < self.max_right:
            filename = TAG_PATH + "right_%d.bmp"%self.right
            self.right += 1
            return filename
        if self.up < self.max_up:
            filename = TAG_PATH + "up_%d.bmp"%self.up
            self.up += 1
            return filename
        if self.down < self.max_down:
            filename = TAG_PATH + "down_%d.bmp"%self.down
            self.down += 1
            return filename
        print("Now every arrows are classified.")
        print("Program ends in..")
        for i in range(5):
            print(str(5-i))
            time.sleep(1)
        exit(0)
    def ReadProgress(self):
        try:
            arrow_log = open(ARROW_PATH+ARROW_LOG,'r')
        except FileNotFoundError:
            print("Arrow Classification log file not found. variables set to 0")
            return

        self.full = int(arrow_log.readline().replace("\n",""))
        self.empty = int(arrow_log.readline().replace("\n",""))
        self.left = int(arrow_log.readline().replace("\n",""))
        self.right = int(arrow_log.readline().replace("\n",""))
        self.up = int(arrow_log.readline().replace("\n",""))
        self.down = int(arrow_log.readline().replace("\n",""))
        self.left_full = int(arrow_log.readline().replace("\n",""))
        self.right_full = int(arrow_log.readline().replace("\n",""))
        self.up_full = int(arrow_log.readline().replace("\n",""))
        self.down_full = int(arrow_log.readline().replace("\n",""))
        self.left_empty = int(arrow_log.readline().replace("\n",""))
        self.right_empty = int(arrow_log.readline().replace("\n",""))
        self.up_empty = int(arrow_log.readline().replace("\n",""))
        self.down_empty = int(arrow_log.readline().replace("\n",""))
        self.pended = int(arrow_log.readline())

    def saveProgress(self):
        print("Save start...")
        arrow_log = open(ARROW_PATH + ARROW_LOG,'w')
        arrow_log.write("%d\n" % self.full)
        arrow_log.write("%d\n" % self.empty)
        arrow_log.write("%d\n" % self.left)
        arrow_log.write("%d\n" % self.right)
        arrow_log.write("%d\n" % self.up)
        arrow_log.write("%d\n" % self.down)
        arrow_log.write("%d\n" % self.left_full)
        arrow_log.write("%d\n" % self.right_full)
        arrow_log.write("%d\n" % self.up_full)
        arrow_log.write("%d\n" % self.down_full)
        arrow_log.write("%d\n" % self.left_empty)
        arrow_log.write("%d\n" % self.right_empty)
        arrow_log.write("%d\n" % self.up_empty)
        arrow_log.write("%d\n" % self.down_empty)
        arrow_log.write("%d" % self.pended)
        print("Save done.")