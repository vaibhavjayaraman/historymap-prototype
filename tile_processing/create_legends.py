import cv2
import numpy as np
from os import listdir

from create_region import TILE_PICTURE_LOCATIONS
from create_region import ORIGINAL, LEGEND_MASK, LEGENDS
from tqdm import tqdm


def create_masked_legend(region, filename, mask_suffix = "legendmask.png"):
    """Uses bitwise and on mask and year to create tile of the parts of the region that are wanted. 
    @param region - name of directory wanted 
    @param filename- full file name containing map of region for particular year
    @param mask_suffix - full file name containing mask of region for all years, """
    img = cv2.imread(TILE_PICTURE_LOCATIONS + region + ORIGINAL + filename)
    #perhaps here change all values that are 255 to 254 so that they do not become transparent later
    msk = cv2.imread(TILE_PICTURE_LOCATIONS + region + LEGEND_MASK + region + mask_suffix, 0) 
    masked = cv2.bitwise_and(img, img, mask = msk)
    #gets rid of columns and rows that are not wanted
    columns_to_delete = []
    rows_to_delete = []
    #checks to see if all rows in column are bad and if so discards column
    for column in range(len(masked)):
        discard_column = True
        for row in range(len(masked.T)):
            if not np.array_equal(masked[row][column], np.array([0,0,0])):
                print(column)
                discard_column = False
        if discard_column:
            columns_to_delete.append(column)
    #checks to see if all columns in row are bad and if so discards row
    for row in range(len(masked.T)):
        discard_row = True
        for column in range(len(masked)):
            if not np.array_equal(masked.T[column][row], np.array([0,0,0])):
                discard_row = False
        if discard_row:
            rows_to_delete.append(row)
    #discards rows and columns
    masked = np.delete(masked, rows_to_delete, axis = 0) 
    masked = np.delete(masked, columns_to_delete, axis = 1)
    cv2.imwrite(TILE_PICTURE_LOCATIONS + region + LEGENDS + filename, masked)

def create_legends(region):
    """Creates Legends for temporal maps of region. """
    for _file in tqdm(listdir(TILE_PICTURE_LOCATIONS + region + ORIGINAL)):
        create_masked_legend(region, _file)
    print("all legends have been created")
