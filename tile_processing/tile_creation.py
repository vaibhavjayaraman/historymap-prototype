from os import system, listdir, makedirs, remove
from re import search
from create_region import TILE_PICTURE_LOCATIONS
from create_region import GEOTIFF
from create_region import VRT
from create_region import WRAPPED_VRT
from create_region import GEOTIFF
from create_region import TILES
from create_region import TRANSPARENT_TIFF
from tqdm import tqdm 

def create_vrt_and_transparent_tiff(region, source = GEOTIFF, vrt = VRT, dest = TRANSPARENT_TIFF):
    source_dir = TILE_PICTURE_LOCATIONS + region + source
    vrt_dir = TILE_PICTURE_LOCATIONS + region + vrt
    dest_dir = TILE_PICTURE_LOCATIONS + region + dest
    for _file in listdir(source_dir):
        #assumes that each _file has a file extension
        file_name = _file[:_file.find(".")]
        #-srcnodata 255 255 255 makes every completely white spot transparent in vrt file
        transparent_black = "'0 0 0'"
        #at this point gdalbuildvrt does not seem to be able to output vrt files to diff directories
        build_vrt = "gdalbuildvrt -srcnodata {}" + " " + file_name + ".vrt" + " " + source_dir + _file
        system(build_vrt.format(transparent_black))
        system("gdal_translate " + file_name + ".vrt" + " " + dest_dir + _file)
        #have to get rid of vrt file that is created in this process
        remove(file_name + ".vrt")
    print("Created Vrt Files for " + region + " using files in " + source + " and outputting to " + dest)

def create_tiles(region, source = TRANSPARENT_TIFF , dest = TILES, zoom = 8):
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
        create_tile = "gdal2tiles.py --profile=mercator -z 1-" + str(zoom) + " " + source_dir + _file + " " + dest_dir + match.group() 
        system(create_tile)
    print("Created raster tiles for " + region + "using files in " + source + "and outputting to " + dest)
    
