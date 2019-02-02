from create_region import create_region, ORIGINAL, TILE_PICTURE_LOCATIONS, GEOTIFF, INTERTIFF, MASKED, TRANSPARENT_PNG
from mask_tiles import mask_images, make_transparent_png
from meta_data import geotiff_create
from tile_creation import create_raster_tiles
from os import system, listdir
from re import search
from tqdm import tqdm

"""This file goes through the entire process of the original. Assumes that there are PNGs in create_region.py's ORIGINAL directory, a mask of the desired parts in create_region.py's MASK directory, and a georeferenced tiff of the PNGs in create_region.py's MODELTIFF directory"""

def directory_structure_for_region(region):
    create_region(region)

def delete_directory_contents(region, subdir):
    """Deletes directory contents after use to save space."""
    folder = TILE_PICTURE_LOCATIONS + region + subdir
    system("rm -rf  "+ folder + "/*")
    print("deleted " + folder)

def generate_tiles(region, delete_used_dir = True):
    """Go through entire process of creating tiles. Later modularize and create path so that one can do one year instead of all years."""
    directory_structure_for_region(region)
    for png in tqdm(listdir(TILE_PICTURE_LOCATIONS + region + ORIGINAL)):
        #change to include negative numbers
        match = search(r'\d+', png)
        year = match.group()
        mask_images(region, year + ".png")    
        make_transparent_png(region, year + ".png")
        geotiff_create(region, year + ".png")
        create_raster_tiles(region, year + ".tif", year)
        if delete_used_dir:
            delete_directory_contents(region, MASKED)
            delete_directory_contents(region, TRANSPARENT_PNG)
            delete_directory_contents(region, GEOTIFF)
            delete_directory_contents(region, TRANSPARENT_PNG)
            delete_directory_contents(region, INTERTIFF)
