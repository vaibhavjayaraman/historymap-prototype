from os import rename, symlink, makedirs, listdir, getcwd, replace
from os.path import isdir, islink 
"""Allows for a centralized tile server to be deployed where all the pngs from all regions are in the same area. Currently we do not believe this will work since if there are two regions that cover the same lat/lon (even if one of them has this coordinate as invisible), there will be a potential conflict since the tile server will not know which of the two region's png of that coordinate to display. Thus the many decentralized tile servers will be used for the time being."""

"""Adds tiles from region to tile server. Modularize and allow for one year to be done at a time."""
def move_tiles(region, path = "tile_processing/test_pictures/", tile_server_base = "tile_server/", zoom = 8, tiles = RASTER_TILES):
    base = path + region + "/" + tiles
    years = [_dir for _dir in listdir(base) if isdir(base + _dir)]
    for year in years:
        #perhaps put a protection in case something destructive happens during execution
        if not isdir(tile_server_base + year):
            makedirs(tile_server_base + year)
            for val in range(1,zoom + 1):
                makedirs(tile_server_base + year + "/" + str(val))
        year_base = base + year + "/"
        zoom_levels = [_dir for _dir in listdir(year_base) if isdir(year_base + _dir)]
        for _zoom in zoom_levels:
            try:
                if int(_zoom) <= zoom:
                    for column in listdir(year_base + _zoom):
                        # column_dir is directory in tile_server
                        # column_path is location of column directory in region tile directory
                        column_dir = tile_server_base + year + "/" + _zoom + "/" + column
                        column_path = year_base + _zoom + "/" + column
                        if not isdir(column_dir):
                            makedirs(column_dir)
                        for _png in listdir(column_path):
                            region_file_path = column_path+ "/" + _png
                            ts_file_path = column_dir + "/" + _png
                            if not islink(region_file_path):
                                try:
                                    rename(region_file_path, ts_file_path)
                                except OSError:
                                    #include an option that will save old png in case of symlink override
                                    replace(region_file_path, ts_file_path)
                                    print("Replacing Column: " + column + ",_png: " + _png + " since it already exists in tile_server") 
                                symlink(getcwd()+ "/" + ts_file_path, region_file_path)
            except ValueError as e: 
                print(_zoom + "cannot be converted to int") 



