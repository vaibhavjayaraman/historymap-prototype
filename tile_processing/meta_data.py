"""This file translates the metadata from one file to another"""
from PIL import Image
from osgeo import gdal
import os
from create_region import TILE_PICTURE_LOCATIONS
from create_region import ORIGINAL
from create_region import GEOTIFF
from create_region import TIFF
from create_region import MASKED

def translate_png_to_tiff(region, source = MASKED, dest = TIFF):
    """Translates all pngs in source folder and converts them to tiffs that will be put into dest folder."""
    for _file in os.listdir(TILE_PICTURE_LOCATIONS + region + source):
        img = Image.open(TILE_PICTURE_LOCATIONS + region + source + _file)
        ext_index = _file.find(".png")
        if ext_index != -1:
            img.save(TILE_PICTURE_LOCATIONS + region + dest + _file[:ext_index] + ".tiff")
        else:
            img.save(TILE_PICTURE_LOCATIONS + region + dest + _file + ".tiff")

def get_geo_transform(region, data_source = None):
    """Uses gdalinfo to return the the geotransform and projection type"""
    if data_source == None:
        data_source = GEOTIFF + region + "geo.tif"
    ds = gdal.Open(TILE_PICTURE_LOCATIONS + region + data_source)
    return ds.GetGeoTransform(), ds.GetProjection(), ds.GetMetadata()

def migrate_metadata_to_tiff(region, source = TIFF, data_folder = GEOTIFF, data_file = None):
    """takes metadata from data_source in the GEOTIFF folder for a region and creates new geotiff files based off data_source metadata."""
    if data_file == None:
        data_file = region + "geo.tif"
    data_source = data_folder + data_file
    #gdalinfo to get coordinates of location
    geo_transform, projection, meta_data= get_geo_transform(region, data_source)
    #assumes that _file is a tiff
    for _file in os.listdir(TILE_PICTURE_LOCATIONS + region + source):
        #changes file permissions of file
        os.chmod(TILE_PICTURE_LOCATIONS + region + source + _file, 0o777)     
        src_ds = gdal.Open(TILE_PICTURE_LOCATIONS + region + source + _file, gdal.GA_Update)
        #These property alterations will not change the Image Structure Metadata of the tiff that is acted upon.Therefore, INTERLEAVE field will still be PIXEL, while the model will be BAND.This changes the corner coordinates a bit.
        src_ds.SetGeoTransform(geo_transform) 
        src_ds.SetProjection(projection)
        src_ds.SetMetadata(meta_data)
        dst_ds = src_ds.GetDriver().CreateCopy(TILE_PICTURE_LOCATIONS + region + data_folder + "geo" + _file, src_ds, strict = 0)
        dst_ds = None
        src_ds = None 
