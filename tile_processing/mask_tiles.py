import cv2
import numpy as np
from os import listdir, system

from create_region import TILE_PICTURE_LOCATIONS
from create_region import MASK
from create_region import MASKED, TRANSPARENT_PNG
from create_region import GEOTIFF
from create_region import ORIGINAL 
from tqdm import tqdm


def mask_images(region, filename, mask = "mask.png"):
    """Uses bitwise and on mask and year to create tile of the parts of the region that are wanted. 
    @param region - name of directory wanted 
    @param filename- full file name containing map of region for particular year
    @param mask - full file name containing mask of region for all years, """
    img = cv2.imread(TILE_PICTURE_LOCATIONS + region + ORIGINAL + filename)
    #change all bits that are 0 to 1 here so that they do not become transparent later
    img[np.where((img == [0,0,0]).all(axis = 2))] = [1,1,1]
    msk = cv2.imread(TILE_PICTURE_LOCATIONS + region + MASK + region + mask, 0) 
    masked = cv2.bitwise_and(img, img, mask = msk)
    cv2.imwrite(TILE_PICTURE_LOCATIONS + region + MASKED + filename, masked)
    print("masked  PNG ")

def make_transparent_png(region, _file, source = MASKED, dest = TRANSPARENT_PNG):
    source_dir = TILE_PICTURE_LOCATIONS + region + source
    dest_dir = TILE_PICTURE_LOCATIONS + region + dest
    sourcefile = source_dir + _file
    destfile = dest_dir + _file
    convert = "convert " + sourcefile + " -transparent black -alpha on " + destfile
    system(convert)
    print("Made png transparent from " + source + " to " + dest)



