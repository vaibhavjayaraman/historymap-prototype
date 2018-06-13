"""This file translates the metadata from one file to another"""
from PIL import Image
from osgeo import gdal
from os import system, listdir, chmod, remove
from create_region import TILE_PICTURE_LOCATIONS
from create_region import ORIGINAL
from create_region import GEOTIFF
from create_region import TIFF
from create_region import MASKED
from create_region import MODELTIFF
from tqdm import tqdm

def translate_png_to_tiff(region, source = MASKED, dest = TIFF):
    """Translates all pngs in source folder and converts them to tiffs that will be put into dest folder."""
    source_dir = TILE_PICTURE_LOCATIONS + region + source
    dest_dir = TILE_PICTURE_LOCATIONS + region + dest
    for _file in tqdm(listdir(TILE_PICTURE_LOCATIONS + region + source)):
        ext_index = _file.find(".png")
        if ext_index == -1:
            system("gdal_translate -scale " + source_dir + _file + " " + dest_dir + _file + ".tiff")
        else:
            system("gdal_translate -scale " + source_dir + _file + " " + dest_dir + _file[:ext_index] + ".tiff")
    print("Translated png to tiff")

def geotiff_create(region, source = MASKED, dest = GEOTIFF):
    """takes metadata from data_source in the GEOTIFF folder for a region and creates new geotiff files based off data_source metadata."""
    source_folder = TILE_PICTURE_LOCATIONS + region + source
    dest_folder = TILE_PICTURE_LOCATIONS + region + dest
    for _file in tqdm(listdir(source_folder)):
        sourcepath = source_folder + _file
        inter_path = dest_folder + _file
        ext_index = _file.find(".png")
        #assumes that there will be no -1 indexes (.png will always be found)
        destpath = dest_folder + _file[:ext_index] + ".tif"
        translate = "gdal_translate -of GTiff -gcp 567.344 496.649 4.00783e+06 4.42978e+06 -gcp 391.051 1127.79 3.89327e+06 3.44496e+06 -gcp 1595.33 290.84 5.60473e+06 4.91106e+06 -gcp 164.791 32.1259 3.23639e+06 5.03231e+06 -gcp 1562.15 1131.46 5.57244e+06 3.53e+06 -gcp 447.23 586.995 3.84236e+06 4.2981e+06 -gcp 1.73364 49.8788 3e+06 4.936e+06 -gcp 999.31 38.3279 4.5828e+06 5.2809e+06 " + "'"+sourcepath+"'" + " " + "'" + inter_path + "'"
        print(translate)
        system(translate)
        warp = "gdalwarp -r near -tps -co COMPRESS=NONE -dstalpha -s_srs EPSG:3857 -t_srs EPSG:3857 " + "'" + inter_path + "'" + " " + "'" + destpath + "'"
        print(warp)
        system(warp)

    print("Migrated metadata to geotiff")
def metadata_move(region, source = TIFF, model_folder = MODELTIFF, dest = GEOTIFF, model_file = None):
    """takes metadata from data_source in the GEOTIFF folder for a region and creates new geotiff files based off data_source metadata."""
    if model_file == None:
        model_file = region + "geo.tif"
    modeltiff = TILE_PICTURE_LOCATIONS + region + model_folder + model_file
    source_folder = TILE_PICTURE_LOCATIONS + region + source
    dest_folder = TILE_PICTURE_LOCATIONS + region + dest
    for _file in tqdm(listdir(source_folder)):
        sourcepath = source_folder + _file
        destpath = dest_folder + _file
        model = gdal.Open(modeltiff, gdal.GA_Update) 
        img = model.GetDriver().CreateCopy(dest_folder +  "geo" + _file, model, strict = 0)
        del model
        model_img = Image.open(modeltiff)
        im = Image.open(sourcepath)
        im = im.resize(model_img.size, Image.ANTIALIAS)
        pixel_ref = im.load()
        print(pixel_ref[45,45])
        for band_count in range(1,4):
            band = img.GetRasterBand(band_count)
            ar = band.ReadAsArray()
            print(str(ar[45,45]) +"\n" + "helo")
            continue
            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    num = pixel_ref[i, j][band_count - 1]
                    ar[j,i] = num
            band.WriteArray(ar)
            del ar, band
        del img
    print("Migrated metadata to geotiff")
    
def get_geo_transform(region, data_file, data_folder = MODELTIFF):
    """Uses gdalinfo to return the geotransform and projection type"""
    data_source = data_folder + data_file
    modeltiff = TILE_PICTURE_LOCATIONS + region + data_source
    ds = gdal.Open(modeltiff)
    im = Image.open(modeltiff)
    return ds.GetGeoTransform(), ds.GetProjection(), ds.GetMetadata(), im.size

def migrate_metadata_to_tiff(region, source = TIFF, model_folder = MODELTIFF, data_folder = GEOTIFF, data_file = None):
    """takes metadata from data_source in the GEOTIFF folder for a region and creates new geotiff files based off data_source metadata."""
    if data_file == None:
        data_file = region + "geo.tif"
    #gdalinfo to get coordinates of location
    geo_transform, projection, meta_data, model_size = get_geo_transform(region, data_file, model_folder)
    size = model_size[0], model_size[1]
    #assumes that _file is a tiff
    for _file in tqdm(listdir(TILE_PICTURE_LOCATIONS + region + source)):
        #changes file permissions of file
        filepath = TILE_PICTURE_LOCATIONS + region + source + _file
        chmod(filepath, 0o777)     
        im = Image.open(filepath)
        im = im.resize(size, Image.ANTIALIAS)
        im.save(filepath, "TIFF")
        src_ds = gdal.Open(filepath, gdal.GA_Update)
        #These property alterations will not change the Image Structure Metadata of the tiff that is acted upon.Therefore, INTERLEAVE field will still be PIXEL, while the model will be BAND.This changes the corner coordinates a bit.
        dst_ds = src_ds.GetDriver().CreateCopy(TILE_PICTURE_LOCATIONS + region + data_folder + "geo" + _file, src_ds, strict = 0)
        dst_ds.SetGeoTransform(geo_transform) 
        dst_ds.SetProjection(projection)
        dst_ds.SetMetadata(meta_data)
        dst_ds = None
        src_ds = None 
    print("Migrated metadata to geotiff")
