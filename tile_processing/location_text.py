import cv2
import pytesseract
import numpy as np
import os

from create_region import TILE_PICTURE_LOCATIONS
from create_region import ORIGINAL
from create_region import EDGE
from create_region import TEXT

def text_to_black(region, year):
    img = cv2.imread(TILE_PICTURE_LOCATIONS + region + ORIGINAL + year,cv2.IMREAD_GRAYSCALE)
    np.save('orig', img)
    dest = cv2.inRange(img,1, 255)
    np.save('dest', dest)
    if not os.path.isdir(TILE_PICTURE_LOCATIONS + region + TEXT + year):
        os.makedirs(TILE_PICTURE_LOCATIONS + region + TEXT + year)
    cv2.imwrite(TILE_PICTURE_LOCATIONS + region + TEXT + year, dest)
    

def text_analysis(region, year):
    """Takes file from original. Assumes filename is in TEXT/"""
    path = TILE_PICTURE_LOCATIONS + region + TEXT + year
    text = pt.image_to_string(Image.open(path))
    return text 


