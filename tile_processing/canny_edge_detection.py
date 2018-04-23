import cv2
from PIL import Image
import pytesseract as pt
import numpy as np

from create_region import TILE_PICTURE_LOCATIONS
from create_region import EDGE
from create_region import TEXT
from create_region import ORIGINAL

def edge_detection(year, region, src = ORIGINAL, dest = EDGE, flag = 0):
    """Converts image to just its edges. Assumes original is in original/, and will write to edge/."""
    img = cv2.imread(TILE_PICTURE_LOCATIONS + region + src + year, flag)
    edges = cv2.Canny(img, 100, 200)
    cv2.imwrite(TILE_PICTURE_LOCATIONS + region + dest + year, edges)
