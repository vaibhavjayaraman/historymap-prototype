from os import system, listdir, makedirs, remove
from re import search
from create_region import TILE_PICTURE_LOCATIONS
from create_region import VRT
from create_region import WRAPPED_VRT
from create_region import GEOTIFF, TIFF, REFTIFF
from create_region import RASTER_TILES 
from create_region import VECTOR_TILES
from create_region import TRANSPARENT_TIFF, TRANSPARENT_PNG
from create_region import GEOJSON

from tqdm import tqdm 


def create_raster_tiles(region, tiff_file, year, source = GEOTIFF, dest = RASTER_TILES, zoom = 8):
    source_dir = TILE_PICTURE_LOCATIONS + region + source
    dest_dir = TILE_PICTURE_LOCATIONS + region + dest
    try:
        makedirs(dest_dir + year)
    except FileExistsError as e:
        print(tiff_file)
    create_tile = "gdal2tiles.py --s_srs EPSG:3857 --profile=mercator -z 1-" + str(zoom) + " " + source_dir + tiff_file + " " + dest_dir + year 
    system(create_tile)
    print("Created raster tiles for " + region + "using files in " + source + "and outputting to " + dest)
    
