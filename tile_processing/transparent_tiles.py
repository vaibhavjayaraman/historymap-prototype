import cv2
import numpy as np
import os

from create_region import TILE_PICTURE_LOCATIONS
from create_region import MASK
from create_region import GEOTIFF
from create_region import ORIGINAL 


def create_transparent_tiles(region, year, mask)
"""Uses bitwise and on mask and year to create tile of the parts of the region that are wanted. 
@param region - name of directory wanted 
@param year - full file name containing map of region for particular year
@param mask - full file name containing mask of region for all years, """

img = cv2.imread(TILE_PICTURE_LOCATIONS + region + ORIGINAL + year)
msk = cv2.imread(TILE_PICTURE_LOCATIONS + region + 
