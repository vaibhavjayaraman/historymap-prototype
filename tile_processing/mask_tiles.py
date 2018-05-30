import cv2
import numpy as np
import os

from create_region import TILE_PICTURE_LOCATIONS
from create_region import MASK
from create_region import MASKED 
from create_region import GEOTIFF
from create_region import ORIGINAL 
from tqdm import tqdm


def create_masked_png(region, filename, mask = "mask.png"):
    """Uses bitwise and on mask and year to create tile of the parts of the region that are wanted. 
    @param region - name of directory wanted 
    @param year - full file name containing map of region for particular year
    @param mask - full file name containing mask of region for all years, """
    img = cv2.imread(TILE_PICTURE_LOCATIONS + region + ORIGINAL + filename)
    msk = cv2.imread(TILE_PICTURE_LOCATIONS + region + MASK + mask, 0) 
    masked = cv2.bitwise_and(img, img, mask = msk)
    cv2.imwrite(TILE_PICTURE_LOCATIONS + region + MASKED + filename, masked)

def mask_images(region):
    for _file in tqdm(os.listdir(TILE_PICTURE_LOCATIONS + region + ORIGINAL)):
        create_masked_png(region, _file)


