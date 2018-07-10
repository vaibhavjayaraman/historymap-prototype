from os import rename, symlink, makedirs, listdir, getcwd, replace
from os.path import isdir, islink 
from tile_processing.create_region import RASTER_TILES
"""Adds legends (original pngs) from region to tile server. Modularize and allow for one year to be done at a time."""
def move_legends(region, path = "tile_processing/test_pictures/", legend_server_base = "legend_server/", legends = "/original/"):
    region_legends = path + region + "/" + legends
    ls_region_base = legend_server_base + region + "/" 
    if not isdir(legend_server_base):
        makedirs(legend_server_base)
        print("Made Legend Server at: " + legend_server_base)
    if not isdir(ls_region_base):
        makedirs(ls_region_base)
        print("Made region legend server for: " + region)
    for year in listdir(region_legends):
        region_year_path = region_legends + "/" + year
        ls_year_path = ls_region_base + year
        try:
            rename(region_year_path, ls_year_path)
        except OSError:
            #include an option that will save old png in case of symlink override
            replace(region_year_path, ls_year_path)
            print("Replacing Column: " + column + ",_png: " + _png + " since it already exists in tile_server")
        symlink(getcwd()+ "/" + ls_year_path, region_year_path)
    print("Moved legends to " + region + " legend server")


