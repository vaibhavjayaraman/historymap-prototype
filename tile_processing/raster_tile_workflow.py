from create_region import create_region
from mask_tiles import mask_images
from meta_data import translate_png_to_tiff
from meta_data import migrate_metadata_to_tiff
from tile_creation import create_vrt_and_transparent_tiff
from tile_creation import create_raster_tiles

"""This file goes through the entire process of the original. Assumes that there are PNGs in create_region.py's ORIGINAL directory, a mask of the desired parts in create_region.py's MASK directory, and a georeferenced tiff of the PNGs in create_region.py's MODELTIFF directory"""

def directory_structure_for_regions(region):
    create_region(region)


def generate_tiles(region):
    """Go through entire process of creating tiles. Later modularize and create path so that one can do one year instead of all years."""
    mask_images(region)    
    translate_png_to_tiff(region)
    migrate_metadata_to_tiff(region)
    create_vrt_and_transparent_tiff(region)
    create_raster_tiles(region)
