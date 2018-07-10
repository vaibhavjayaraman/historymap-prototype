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


def create_raster_tiles(region, source = GEOTIFF, dest = RASTER_TILES, zoom = 8):
    source_dir = TILE_PICTURE_LOCATIONS + region + source
    dest_dir = TILE_PICTURE_LOCATIONS + region + dest
    for _file in tqdm(listdir(source_dir)):
        match = search(r'\d+', _file)
        if match == None:
            print(_file)
            continue
        try:
            makedirs(dest_dir + match.group())
        except FileExistsError as e:
            print(_file)
        create_tile = "gdal2tiles.py --s_srs EPSG:3857 --profile=mercator -z 1-" + str(zoom) + " " + source_dir + _file + " " + dest_dir + match.group() 
        system(create_tile)
    print("Created raster tiles for " + region + "using files in " + source + "and outputting to " + dest)
    
