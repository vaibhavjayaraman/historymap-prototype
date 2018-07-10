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

def mask_geotiff(region, source = GEOTIFF, dest = TRANSPARENT_TIFF):
    source_dir = TILE_PICTURE_LOCATIONS + region + source
    dest_dir  = TILE_PICTURE_LOCATIONS + region + dest
    for _file in listdir(source_dir):
        sourcepath = source_dir + _file
        destpath = dest_dir + _file
        translate = "gdal_translate -mask 4 " + sourcepath + " " + destpath
        system(translate)
    print("masked tiffs from " + source + " to " + dest)

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

def migrate_metadata_to_tiff(region, source = TIFF, model_folder = MODELTIFF, data_folder = REFTIFF, data_file = None):
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
