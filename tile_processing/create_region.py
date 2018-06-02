import os
"""Folder which contains tile picture locations. """
TILE_PICTURE_LOCATIONS = "test_pictures/"
"""Contains PNGs of original images"""
ORIGINAL = "/original/"
EDGE = "/edge/"
TEXT = "/text/"
NAMES = "/names/"
EDGE_ON_TEXT = "/edge_on_text/"
MASK = "/mask/"
MASKED = "/masked/"
"""Folder that contains georeferenced tiffs."""
GEOTIFF = "/geotiff/"
"""Folder that contains non georeferenced tiffs."""
TIFF = "/tiff/"
MODELTIFF = "/modeltiff/"
TRANSPARENT_TIFF= "/transparent_tiff/"
VRT = "/vrt/"
WRAPPED_VRT = "/wrapped_vrt/"
RASTER_TILES = "/raster_tiles/"
VECTOR_TILES = "/vector_tiles/"
ORIGINAL_SVG = "/original_svg/"
GEOJSON="/geojson/"

def create_region(region):
    """Creates directory  and subdirectories for maps of region. """
    os.makedirs(TILE_PICTURE_LOCATIONS + region)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + ORIGINAL)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + EDGE)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + TEXT)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + MASK)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + MASKED)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + GEOTIFF)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + TIFF)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + VRT)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + TILES)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + TRANSPARENT_TIFF)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + ORIGINAL_SVG)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + GEOJSON)
def move_file(path, region, year):
    """Moves files to correct region. """
    os.rename(path, TILE_PICTURE_LOCATIONS + region + ORIGINAL)
