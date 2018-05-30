from os import system, listdir, makedirs
from re import search
from create_region import TILE_PICTURE_LOCATIONS
from create_region import GEOTIFF
from create_region import VRT
from create_region import WRAPPED_VRT
from create_region import GEOTIFF
from create_region import TILES
from tqdm import tqdm 
def create_vrt(region, source = GEOTIFF, dest = VRT):
    source_dir = TILE_PICTURE_LOCATIONS + region + source
    dest_dir = TILE_PICTURE_LOCATIONS + region + dest
    for _file in listdir(source_dir):
        #assumes that each _file has a file extension
        file_name = _file[:_file.find(".")]
        #-srcnodata 255 255 255 makes every completely white spot transparent in vrt file
        build_vrt = "gdalbuildvrt -srcnodata '255 255 255'" + " " + dest_dir + file_name + ".vrt" + " " + source_dir + _file
        system(build_vrt)
    print("Created Vrt Files for " + region + "using files in " + source + " and outputting to " + dest)

def create_tiles_from_vrt(region, source = VRT, dest = TILES):
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
        create_tile = "gdal2tiles.py -p " + dest_dir + match.group() + " -k " + source_dir + _file
        system(create_tile)
    
