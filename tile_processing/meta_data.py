"""This file translates the metadata from one file to another"""
from PIL import Image
from osgeo import gdal
from os import system, listdir, chmod, remove
from create_region import TILE_PICTURE_LOCATIONS
from create_region import ORIGINAL
from create_region import REFTIFF, GEOTIFF, INTERTIFF
from create_region import TIFF
from create_region import MASKED
from create_region import MODELTIFF, TRANSPARENT_TIFF, TRANSPARENT_PNG, TRANSLATED_PNG, TRANSLATE_FILE
from tqdm import tqdm


def geotiff_create(region, source = TRANSPARENT_PNG, trans = TRANSLATED_PNG, inter = INTERTIFF, dest = GEOTIFF, translatefile = TRANSLATE_FILE):
    """takes metadata from data_source in the GEOTIFF folder for a region and creates new geotiff files based off data_source metadata."""
    source_folder = TILE_PICTURE_LOCATIONS + region + source
    dest_folder = TILE_PICTURE_LOCATIONS + region + dest
    inter_folder = TILE_PICTURE_LOCATIONS + region + inter
    trans_folder = TILE_PICTURE_LOCATIONS + region + trans
    translate_file = TILE_PICTURE_LOCATIONS + region + translatefile
    for _file in tqdm(listdir(source_folder)):
        sourcepath = source_folder + _file
        trans_path = trans_folder + _file
        interpath= inter_folder + _file[:_file.find(".")] + ".tif"
        destpath = dest_folder + _file[:_file.find(".")] + ".tif"
        with open(translate_file, 'r') as translation:
            geo_ref = translation.read().replace('\n','')
        translate = geo_ref + " " + "'"+sourcepath+"'" + " " + "'" + trans_path + "'"
        system(translate)
        warp = "gdalwarp -r near -tps -co COMPRESS=NONE "+ " -overwrite " + " -s_srs EPSG:3857 -t_srs EPSG:3857 " + "'" + trans_path + "'" + " " + "'" + interpath + "'"
        system(warp)
        translate =  "gdal_translate -mask 4 " + interpath + " " + destpath
    print("Migrated metadata to geotiff")

