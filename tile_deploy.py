from os import rename, symlink, makedirs, listdir, getcwd
from os.path import isdir, islink 
"""Adds tiles from region to tile server. Modularize and allow for one year to be done at a time."""
def move_tiles(region, path = "tile_processing/test_pictures/", tile_server_base = "tile_server/", zoom = 8):
    base = path + region + "/" + "tiles/"
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
                                    symlink(getcwd()+ "/" + ts_file_path, region_file_path)
                                except OSError:
                                    print("Column: " + column + ",_png: " + _png + " already exists in tile_server") 
            except ValueError as e: 
                print(_zoom + "cannot be converted to int") 



