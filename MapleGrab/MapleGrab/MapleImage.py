from PIL import ImageGrab
import cv2
import numpy as np

"""
A module for capturing various objects in MapleStory(KMS).
Only for 800*600, with the program running on the top left corner of the screen.
"""

# Constants
CAPTURE_CV = 0
CAPTURE_PIL = 1
CAPTURE_CV_GRAY = 2
CAPTURE_TF = 3


def tuple_addition(t1,t2,size=4):
    """
    A function for convenient tuple addition.
    Defalt size = 4.
    """
    added = [0,0,0,0]
    for i in range(size):
        added[i] = t1[i] + t2[i]
    return tuple(added)

class MapleCapture:          # 나중에 MapleImageHandler로 바꿀 것
    """
    Maplestory capturing agent.
    need resolution of 640*480 and window mode.
    """

    # Class variables
    pos_factor = (0,0)      # Calibration factor(The position of the window)
    pos_factor_extended = (0,0,0,0)     # Repeat pos_factor two times

    # Constants
    DEFAULT_POS = (0,26,800,626)     # Defalt position of the window.


    # List of other variables
    # self.img_cache = temporary saves captured image

    def __init__(self,double = False):
        self.set_window_pos()
        self.double = double

    def set_window_pos(self):
        """
        Automatically finds the position of maplestory window.
        Uses template search, works only for 600*400.
        Returns calibration factor.
        """
        screen = cv2.cvtColor(np.array(ImageGrab.grab()),cv2.COLOR_RGB2BGR)      # Grab image
        logo = cv2.imread("./Data/Logo.PNG")
        logo_position = match_template_bgr(screen,logo,0.9)
        if logo_position == None:
            print("[MapleCapture] No logo found. If you are not using double monitor,\nPlease adjust the factor.")
            MapleCapture.pos_factor = (0,0)
            MapleCapture.pos_factor_extended = (0,0,0,0)
            print("[MapleCapture] calibration set to (0,0)")
            return None
        else:
            MapleCapture.pos_factor = (logo_position[0] - 4,logo_position[1] - 5)
            MapleCapture.pos_factor_extended = (MapleCapture.pos_factor[0],MapleCapture.pos_factor[1],MapleCapture.pos_factor[0],MapleCapture.pos_factor[1])
        return  MapleCapture.pos_factor

    def capture_all(self, format = 0):
        """
        Captures whole game screen.
        Returnes the captured image, and updates image cache

        Fields
        - format: the format of returned image(0:OpenCV,1:PIL,2:Gray(OpenCV))
        """
        if self.double == False:
            pil_image = ImageGrab.grab(bbox=tuple_addition(MapleCapture.DEFAULT_POS,MapleCapture.pos_factor_extended))
        else:
            pil_image = ImageGrab.grab()

        if format == 0:
            image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        elif format == 1:
            image = pil_image
        elif format == 2:
            image = cv2.cvtColor(np.array(pil_image),cv2.COLOR_RGB2GRAY)

        # Update image cache
        self.img_cache = image
        return image

class MapleCollect(MapleCapture):
    """
    Maplestory Capturing agent for collection.
    """

    # Templates
    TEMPLATE_COMMENT = cv2.imread('./Data/Comment.bmp',0)

    # Constants
    ARROW = (                       
        (-89,79,-28,140),
        (4,79,65,140),
        (97,79,158,140),
        (190,79,251,140)
        )

    def __init__(self):
        self.set_window_pos()

    def crop_arrow(self,scr = None):
        """
        Captures the arrows on minigame for collection.
        Returnes the list of 4 ARROWs(with format of YELLOW image).

        Fields
        - scr: screen image(if nothing given, uses image cache)
        """

        # Preprocessing
        scr = scr if scr is not None else self.img_cache
        b,g,r = cv2.split(scr)
        y_img = g/2+r/2
        y_img = y_img.astype(np.uint8)

        # Find comment(for the arrow minigame). If there is no such thing, return none. 
        pos_comment = match_template_gray(y_img,MapleCollect.TEMPLATE_COMMENT,thresh=0.7)
        if pos_comment == None:
            return None

        # Now Capture
        img = []        # This will store images of arrows
        for i in range(4):
            arro = scr[pos_comment[1]+MapleCollect.ARROW[i][1] : pos_comment[1]+MapleCollect.ARROW[i][3] , pos_comment[0]+MapleCollect.ARROW[i][0] : pos_comment[0]+MapleCollect.ARROW[i][2]]
            img.append(arro)
        return img

def crop_minimap_collection(image):
    """
    Crop the given image to show only minimap.

    Fields
    - image: screenshot
    """
    minimap = image[19:123,8:175]
    return minimap

def match_template_gray(image,template,thresh=0.8):
    """
    Template matching function(Grayscale).
    Returns the top-left location of matching place with tuple (x,y) = (col,row).
    If nothing found, returns None.

    Fields
    - image: source image
    - template: template image
    - thresh: threshold
    """

    res = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)
    _a,maxima,_c,loc = cv2.minMaxLoc(res)
    if maxima < thresh:
        return None
    return loc

def match_template_bgr(image,template,thresh=0.8):
    """
    Template matching function(bgr).
    Returns the top-left location of matching place with tuple (x,y) = (col,row).
    If nothing found, returns None.

    Fields
    - image: source image
    - template: template image
    - thresh: threshold
    """
    img_b, img_g, img_r = cv2.split(image)
    temp_b, temp_g, temp_r = cv2.split(template)
    res_b = cv2.matchTemplate(img_b,temp_b,cv2.TM_CCOEFF_NORMED)
    res_g = cv2.matchTemplate(img_g,temp_g,cv2.TM_CCOEFF_NORMED)
    res_r = cv2.matchTemplate(img_r,temp_r,cv2.TM_CCOEFF_NORMED)
    res = res_b / 3 + res_g / 3 + res_r / 3
    _a,maxima,_c,loc = cv2.minMaxLoc(res)
    if maxima < thresh:
        return None
    return loc

def get_distance_gray(image,temp_chara,temp_target,correction=(0,0),thresh=(0.8,0.8)):
    """
    Calculates the distance from the character to target.
    Returnes the (x,y) = (col,row) difference.

    Fields
    - image: source image
    - charaTemp: character recognizing template
    - targetTemp: target template
    - correction: x,y-correction parameter for the template.
    - thresh: threshold(character,target)
    """

    targetPos = match_template_gray(image,temp_target,thresh=thresh[1])
    charaPos = match_template_gray(image,temp_chara,thresh=thresh[0])
    if targetPos == None or charaPos == None:
        return None
    return (targetPos[0] - charaPos[0] + correction[0], targetPos[1] - charaPos[1] + correction[1])

def get_distance_bgr(image,temp_chara,temp_target,correction=(0,0),thresh=(0.8,0.8)):
    """
    Calculates the distance from the character to target.
    Returnes the (x,y) = (col,row) difference.

    Fields
    - image: source image
    - charaTemp: character recognizing template
    - targetTemp: target template
    - correction: x,y-correction parameter for the template.
    - thresh: threshold(character,target)
    """

    targetPos = match_template_bgr(image,temp_target,thresh=thresh[1])
    charaPos = match_template_bgr(image,temp_chara,thresh=thresh[0])
    if targetPos == None or charaPos == None:
        return None
    return (targetPos[0] - charaPos[0] + correction[0], targetPos[1] - charaPos[1] + correction[1])

def get_distance_gray_multi(image,temp_chara,temp_target,correction=((None,None)),thresh=(0.8,0.8)):
    """
    Calculates the distance from the character to a target.
    This does not finds the closest one, but just finds first one founded.
    Returnes the (x,y) difference.

    Fields
    - image: source image
    - charaTemp: character recognizing template
    - targetTemp: target template
    - correction: x,y-correction parameter for each template.
    - thresh: threshold(character,target)
    """
    temp_num = 0
    for temp in temp_target:
        if correction[0] == (None,None):
            dist = get_distance_gray(image,temp_chara,temp,thresh)
        else:
            dist = get_distance_gray(image,temp_chara,temp,correction[temp_num],thresh)
        if dist != None:
            dist_out = (dist[0],dist[1],temp_num)
            return dist_out
        else:
            temp_num += 1
    return None

def get_distance_bgr_multi(image,temp_chara,temp_target,correction=((None,None)),thresh=(0.8,0.8)):
    """
    Calculates the distance from the character to a target.
    This does not finds the closest one, but just finds first one founded.
    Returnes the (x,y) difference.

    Fields
    - image: source image
    - charaTemp: character recognizing template
    - targetTemp: target template
    - correction: x,y-correction parameter for each template.
    - thresh: threshold(character,target)
    """
    temp_num = 0
    for temp in temp_target:
        if correction[0] == (None,None):
            dist = get_distance_bgr(image,temp_chara,temp,thresh)
        else:
            dist = get_distance_bgr(image,temp_chara,temp,correction[temp_num],thresh)
        if dist != None:
            dist_out = (dist[0],dist[1],temp_num)
            return dist_out
        else:
            temp_num += 1
    return None
