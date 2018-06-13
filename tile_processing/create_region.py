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
LEGEND_MASK = "/legend_mask/"
LEGENDS = "/legends/"

def create_region_subdirs(region):
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + ORIGINAL)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + EDGE)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + TEXT)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + MASK)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + MASKED)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + MODELTIFF)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + GEOTIFF)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + TIFF)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + VRT)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + RASTER_TILES)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + VECTOR_TILES)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + TRANSPARENT_TIFF)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + ORIGINAL_SVG)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + GEOJSON)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + LEGEND_MASK)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + LEGENDS)
    except FileExistsError as e:
        print("File Exists" + str(e))
    
def create_region(region):
    """Creates directory  and subdirectories for maps of region. """
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region)
    except FileExistsError as e:
        print("File Exists" + str(e))
    create_region_subdirs(region)

def move_file(path, region, year):
    """Moves files to correct region. """
    os.rename(path, TILE_PICTURE_LOCATIONS + region + ORIGINAL)
