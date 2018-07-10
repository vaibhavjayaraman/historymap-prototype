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
INTERTIFF = "/inter_tiff/"
REFTIFF = "/reftiff/"
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
TRANSPARENT_PNG = "/transparent_png/"
TRANSLATED_PNG = "/translated_png/"
TRANSLATE_FILE = "/translate_file.txt"

def create_region_subdirs(region):
    try:
        _file = TILE_PICTURE_LOCATIONS + region + TRANSLATE_FILE
        if not os.path.exists(_file):
            open(_file).close()
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + ORIGINAL)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + TRANSLATED_PNG)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + MASK)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + TRANSPARENT_PNG)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + INTERTIFF)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + MASKED)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + GEOTIFF)
    except FileExistsError as e:
        print("File Exists" + str(e))
    try:
        os.makedirs(TILE_PICTURE_LOCATIONS + region + RASTER_TILES)
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
