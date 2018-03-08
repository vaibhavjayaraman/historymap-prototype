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
    

def generate_lat_lon_points():
    """ Script to generate a bunch of lat_lon_points
        to be used in map."""
    #base for google reverse geocoding api(will return json)
	base_url = "http://maps.googleapis.com/maps/api/geocode/json?"
    api_key =  "AIzaSyBByYGtP4MGtNAd9-SxOPdXk5WJML9b1gA"

    #MariaDb connection
    mariadb_connection = mariadb.connect(user='vaibhavj',
                                         password='ocfuser',
                                         database='default')
    cursor = mariadb_connection.cursor()
    step_size = .0004
    lons = arange(-180, 180, step_size).tolist()
    lats = arange(-90, 90, step_size).tolist()
    #numpy.lib.recfunctions.join_by
    for lon in lons:
        for lat in lats:
            time.sleep(20)
            #formatting url string for google reverse geocoding api
            param_url = "latlng={lat},{lon}&key={api_key}".format(
                        lat = lat,
                        lon = lon,
                        api_key = api_key
                    )
            url = "{base}{params}".format(
                    base= base_url, params = param_url)
            try:
                response = requests.get(url).json()
                if response['status'] == 'OK':
                    country_string = reverse_geo_code(response['results'][0]['address_components'])
                    if country_string == None:
                        print("Country String Error:" + str(lat) + "," + str(lon))
                        continue
                    try:
                        cursor.execute("INSERT INTO default (latitude, longitude, 
                                country) VALUES (%f, %f, %s)", (lat, lon, country_string))
                    except mariadb.Error as error:
                        print("Error: {}".format(error))
                else:
                    print("GeoCoding status error: " + str(lat) + "," + str(lon))
            except requests.exceptions.RequestException as e:
                print(e)
                print("GeoCoding URL Error: " + str(lat)+ "," + str(lon))
                    
                
            

