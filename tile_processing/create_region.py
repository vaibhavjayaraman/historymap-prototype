import os

TILE_PICTURE_LOCATIONS = "test_pictures/"
ORIGINAL = "/original/"
EDGE = "/edge/"
TEXT = "/text/"
NAMES = "/names/"
EDGE_ON_TEXT = "/edge_on_text/"

def create_region(region):
    """Creates directory  and subdirectories for maps of region. """
    os.makedirs(TILE_PICTURE_LOCATIONS + region)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + ORIGINAL)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + EDGE)
    os.makedirs(TILE_PICTURE_LOCATIONS + region + TEXT)

def move_file(path, region, year):
    """Moves files to correct region. """
    os.rename(path, TILE_PICTURE_LOCATIONS + region + ORIGINAL)

"""
def move_folder(path, region)
"""
