from os import rename, symlink, makedirs, listdir, getcwd, replace
from os.path import isdir, islink 
from tile_processing.create_region import RASTER_TILES
"""Adds tiles from region to tile server. Modularize and allow for one year to be done at a time."""
def move_tiles(region, path = "tile_processing/test_pictures/", tile_server_base = "region_tile_server/", zoom = 8, tiles = RASTER_TILES):
    region_tiles = path + region + "/" + tiles
    ts_region_base = tile_server_base + region + "/" 
    if not isdir(tile_server_base):
        makedirs(tile_server_base)
        print("Made Tile Server at: " + tile_server_base)
    if not isdir(ts_region_base):
        makedirs(ts_region_base)
        print("Made region tile server for: " + region)
    for year in listdir(region_tiles):
        region_year_path = region_tiles + "/" + year
        ts_year_path = ts_region_base + year
        try:
            rename(region_year_path, ts_year_path)
        except OSError:
            #include an option that will save old png in case of symlink override
            replace(region_year_path, ts_year_path)
            print("Replacing Column: " + column + ",_png: " + _png + " since it already exists in tile_server")
        symlink(getcwd()+ "/" + ts_year_path, region_year_path)
    print("Moved tiles to " + region + " tile server")


