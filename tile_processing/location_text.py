import cv2
import pytesseract as pt
import numpy as np
import os

from create_region import TILE_PICTURE_LOCATIONS
from create_region import ORIGINAL
from create_region import EDGE
from create_region import TEXT
from create_region import NAMES
from create_region import EDGE_ON_TEXT
from canny_edge_detection import edge_detection
from PIL import Image

def text_to_black(region, year):
    img = cv2.imread(TILE_PICTURE_LOCATIONS + region + ORIGINAL + year, 0)
    edge = cv2.imread(TILE_PICTURE_LOCATIONS + region + EDGE + year, 0)

    with_borders = cv2.inRange(img,5, 150)

    without_borders = cv2.bitwise_xor(with_borders, edge)
    if not os.path.isdir(TILE_PICTURE_LOCATIONS + region + TEXT):
        os.makedirs(TILE_PICTURE_LOCATIONS + region + TEXT)
    if not os.path.isdir(TILE_PICTURE_LOCATIONS + region + NAMES):
        os.makedirs(TILE_PICTURE_LOCATIONS + region + NAMES)
    if not os.path.isdir(TILE_PICTURE_LOCATIONS + region + EDGE_ON_TEXT):
        os.makedirs(TILE_PICTURE_LOCATIONS + region + EDGE_ON_TEXT)
    cv2.imwrite(TILE_PICTURE_LOCATIONS + region + TEXT + year, with_borders)
    cv2.imwrite(TILE_PICTURE_LOCATIONS + region + NAMES + year, without_borders)
    edge_detection(year, region, TEXT, EDGE_ON_TEXT) 

def text_analysis(region, year):
    """Takes file from original. Assumes filename is in TEXT/"""
    path = TILE_PICTURE_LOCATIONS + region + TEXT + year
    text = pt.image_to_string(Image.open(path))
    print(text)
    return text 


