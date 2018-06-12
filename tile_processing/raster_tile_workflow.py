from create_region import create_region
from create_region import TILE_PICTURE_LOCATIONS
from create_region import GEOTIFF, TIFF, MASKED, TRANSPARENT_TIFF
from mask_tiles import mask_images
from meta_data import translate_png_to_tiff
from meta_data import migrate_metadata_to_tiff
from tile_creation import create_vrt_and_transparent_tiff
from tile_creation import create_raster_tiles
from os import system

"""This file goes through the entire process of the original. Assumes that there are PNGs in create_region.py's ORIGINAL directory, a mask of the desired parts in create_region.py's MASK directory, and a georeferenced tiff of the PNGs in create_region.py's MODELTIFF directory"""

def directory_structure_for_region(region):
    create_region(region)

def delete_directory_contents(region, subdir):
    """Deletes directory contents after use to save space."""
    folder = TILE_PICTURE_LOCATIONS + region + subdir
    system("rm -rf " + folder)
    print("deleted " + folder)

def generate_tiles(region, delete_used_dir = True):
    """Go through entire process of creating tiles. Later modularize and create path so that one can do one year instead of all years."""
    directory_structure_for_region(region)
    mask_images(region)    
    translate_png_to_tiff(region)
    if delete_used_dir:
        delete_directory_contents(region, MASKED)
    migrate_metadata_to_tiff(region)
    if delete_used_dir:
        delete_directory_contents(region, TIFF)
    create_vrt_and_transparent_tiff(region)
    if delete_used_dir:
        delete_directory_contents(region, GEOTIFF)
    create_raster_tiles(region)
    if delete_used_dir:
        delete_directory_contents(region, TRANSPARENT_TIFF)
