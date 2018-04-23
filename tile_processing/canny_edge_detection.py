import cv2
from PIL import Image
import pytesseract as pt
import numpy as np

from create_region import TILE_PICTURE_LOCATIONS
from create_region import EDGE
from create_region import TEXT

def edge_detection(year, region, flag = 0):
    """Converts image to just its edges. Assumes original is in original/, and will write to edge/."""
    img = cv2.imread(TILE_PICTURE_LOCATIONS + region + "/original/" + year, flag)
    edges = cv2.Canny(img, 100, 200)
    cv2.imwrite(TILE_PICTURE_LOCATIONS + region + "/edge/" + year, edges)

def text_analysis(region, year):
    """Takes file from edge_detection algorithm results. Assumes filename is in edge/"""
    path = TILE_PICTURE_LOCATIONS + region + "/edge/" + year
    text = pt.image_to_string(Image.open(path))
    return text 
    
