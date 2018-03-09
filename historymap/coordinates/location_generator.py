import sys
import os
import requests
import mysql.connector as mariadb
import time
from numpy import arange

def reverse_geo_code(address_components): 
    """Finds country lat/lon value is in from given address components by analyzing
        type array"""
    for address_component in address_components:
        types = address_component['types']
        for address_type in types:
            if (address_type == 'country'):
                return address_component['long_name']
            else
    

def generate_lat_lon_points(countries, min_lat = 0, max_lat = 0, min_lon = 0, 
        max__lon = 0, step_size = .04,):
    #France, belgium, luxembourg - max lat 51.5, min 42.4, max lon: 8.23, min lon - -4.78
    """ Script to generate a bunch of lat_lon_points
        to be used in map."""
    #base for google reverse geocoding api(will return json)
    base_url = "http://maps.googleapis.com/maps/api/geocode/json?"
    api_key =  "AIzaSyBByYGtP4MGtNAd9-SxOPdXk5WJML9b1gA"
    error_dir = "location_generator_error_output/" + countries
    file_count = 0
    entry_count_per_file = 0
    #MariaDb connection
    mariadb_connection = mariadb.connect(user='vaibhavj',
                                         password='ocfuser',
                                         host='mysql',
                                         database='historymap')
    cursor = mariadb_connection.cursor()
    lons = arange(min_lon, max_lon, step_size).tolist()
    lats = arange(min_lat , max_lat , step_size).tolist()
    fd = os.open(error_dir + "/" + str(error_dir)+ ":" + str(min_lat), str(min_lon))
    #numpy.lib.recfunctions.join_by
    for lon in lons:
        for lat in lats:
            entry_count_per_file += 1
            if entry_count_per_file > 250:
                entry_count_per_file = 0
                file_count += 1
                os.close(fd)
                fd = os.open(error_dir + "/" + str(file_count) + ":" + str(lat), str(lon))
            time.sleep(20) #formatting url string for google reverse geocoding api 
            param_url = "latlng={lat},{lon}&key={api_key}".format( lat = lat, 
                 lon = lon, api_key = api_key) 
            url = "{base}{params}".format(
                            base= base_url, params = param_url)
            try:
                response = requests.get(url).json()
                if response['status'] == 'OK':
                    country_string = reverse_geo_code(response['results'][0]['address_components'])
                    if country_string == None:
                        os.write(fd, "Country String Error:" + str(lat) + "," + str(lon))
                        continue
                    try:
                        cursor.execute("INSERT INTO default (latitude, longitude, 
                                country) VALUES (%f, %f, %s)", (lat, lon, country_string))
                    except mariadb.Error as error:
                        os.write(fd, "Error: {}".format(error))
                else:
                    os.write(fd, "GeoCoding status error: " + str(lat) + "," + str(lon))
            except requests.exceptions.RequestException as e:
                os.write(fd, e)
                os.write(fd, "GeoCoding URL Error: " + str(lat)+ "," + str(lon))
   mariadb_connection.close()
   os.close(fd)
                
            

