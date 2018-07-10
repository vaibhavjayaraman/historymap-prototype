from create_region import create_region
from create_region import TILE_PICTURE_LOCATIONS
from create_region import GEOTIFF, TIFF, MASKED, TRANSPARENT_TIFF
from mask_tiles import mask_images, make_transparent_png
from meta_data import translate_png_to_tiff
from meta_data import migrate_metadata_to_tiff
from meta_data import metadata_move, mask_geotiff
from meta_data import geotiff_create
from tile_creation import create_vrt_and_transparent_tiff
from tile_creation import create_raster_tiles, store_transparent_tiff
from os import system

"""This file goes through the entire process of the original. Assumes that there are PNGs in create_region.py's ORIGINAL directory, a mask of the desired parts in create_region.py's MASK directory, and a georeferenced tiff of the PNGs in create_region.py's MODELTIFF directory"""

def directory_structure_for_region(region):
    create_region(region)

def delete_directory_contents(region, subdir):
    """Deletes directory contents after use to save space."""
    folder = TILE_PICTURE_LOCATIONS + region + subdir
    system("rm -rf " + folder)
    print("deleted " + folder)

def generate_tiles(region, sparse = False, delete_used_dir = True):
    """Go through entire process of creating tiles. Later modularize and create path so that one can do one year instead of all years."""
    directory_structure_for_region(region)
    mask_images(region, sparse)    
    make_transparent_png(region)
    geotiff_create(region)
    create_raster_tiles(region)
    if delete_used_dir:
        delete_directory_contents(region, GEOTIFF)
