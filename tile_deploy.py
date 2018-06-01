from os import rename, symlink, makedirs, listdir, getcwd
from os.path import isdir, islink 
"""Adds tiles from region to tile server. Modularize and allow for one year to be done at a time. """
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
                    for _file in listdir(year_base + _zoom):
                        _file_path = year_base + _zoom + "/" + _file
                        _ts_file = tile_server_base + year + "/" + _zoom + "/" + _file
                        if not islink(_file_path):
                            rename(_file_path, _ts_file)
                            symlink(getcwd()+ "/" + _ts_file, _file_path)
            except ValueError as e: 
                print(_zoom + "cannot be converted to int") 



