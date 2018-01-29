from PIL import Image
import cv2
import FrontHandler_v2 as fh
import MapleImage

PARSE_PATH = "./ParsedArrow/"
PARSE_NAME = "Arrow_%d.bmp"
PARSE_LOG = "00NumParsed.txt"
CAPTURE_PATH = fh.CAPTURE_PATH
CAPTURE_NAME = fh.CAPTURE_NAME
CAPTURE_LOG = fh.CAPTURE_LOG

class Parser:
    
    def __init__(self):
        print("Initializing parser...")
        self.numImageSet = 0
        self.numParsedSet = 0
        self.nextArrow = 0
        print("\tReading files...")
        self.UpdateNumber()
        print("Initializing done.")
        self.mcol = MapleImage.MapleCollect()
        

    def UpdateNumber(self):
        # Read total Number of 
        try:
            numImageFile = open(CAPTURE_PATH + CAPTURE_LOG ,'r')
            self.numImageSet = int(numImageFile.readline().replace("\n",""))
        except FileNotFoundError:
            print("Seems like there is no Screenshot!")
            exit(1)
        try:
            lastParsedFile = open(PARSE_PATH + PARSE_LOG,'r')
            self.numParsedSet = int(lastParsedFile.readline())
            self.nextArrow = int(lastParsedFile.readline())
        except FileNotFoundError:
            self.numParsedSet = -1
            self.nextArrow = 0
        print("Read Success. numImage:%d, numParsed:%d" % (self.numImageSet,self.numParsedSet))

    def saveNumber(self):
        out = open(PARSE_PATH + PARSE_LOG, 'w')
        out.write("%d\n%d" % (self.numImageSet,self.nextArrow))

    def parse(self):
        # This is an old box size
        #box = [(248,231,276,259), (341,231,369,259), (434,231,462,259), (527,231,555,259)]

        if self.numImageSet == self.numParsedSet:
            print("Nothing to parse")
            return

        for setNum in range(self.numParsedSet+1,self.numImageSet+1):
            setstr = CAPTURE_PATH + "miniGame_%d" % setNum
            print("Processing set %d" % setNum)
            imgnum = 0
            while True:
                imgstr = setstr + "_%d.bmp" % imgnum
                img = cv2.imread(imgstr)
                if img is None: break

                arrows = self.mcol.crop_arrow(img)
                for arrow in arrows:
                    cv2.imwrite(PARSE_PATH + PARSE_NAME % self.nextArrow,arrow)
                    self.nextArrow += 1
                imgnum += 1
        self.saveNumber()
            