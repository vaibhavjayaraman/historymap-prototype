from configparser import ConfigParser
from django.conf import settings
import django
import requests
import re
import json
import mysql.connector as mariadb
from datetime import datetime
import os

#initiall env setup to get configuration file database
"""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'historymap.settings')
django.setup()
CONF = getattr(settings, "CONF", None)
"""
CONF = "/etc/historymap/historymap.conf"

def remove_html(text):
    """Removes html tags from text"""
    remove = re.compile('<.*?>')
    return re.sub(remove, '', text)

def generate_wiki_timeline(year, section_interests = {"Events", "Births", "Deaths"}):
    """Gets timeline information for wikipedia_year"""
    timeline = dict.fromkeys(section_interests, 0)
    year = str(year)
    wiki_api_url = "http://en.wikipedia.org/w/api.php?format=json&action=parse&prop=sections&page=" + year
    resp = requests.get(url = wiki_api_url)
    data = resp.json()
    if data != None:
        #gets sections numbers for sections in section_interests from this article to put in timeline
        if data.get("parse") != None:
            sections = data.get("parse").get("sections") 
            for section in sections:
                if section.get("line") in section_interests:
                    timeline[section.get("line")] = section.get("number")

            for key in timeline.keys():
                #gets section content url
                section_content_url = "https://en.wikipedia.org/w/api.php?format=json&action=parse&page=" + year + "&section=" + timeline[key]
                resp = requests.get(url = section_content_url)
                data = resp.json()
                if data != None:
                    content = data.get("parse")
                    timeline[key] = content.get("text").get("*")
    return timeline

def add_wiki_timeline(column = "wikipedia_timeline", comp = "IS", cond = "NULL"):
    database = 'mysql'
    conf = ConfigParser()
    conf.read(CONF)
    name = conf.get(database, 'name')
    user = conf.get(database, 'user')
    passwd = conf.get(database, 'password')
    host = conf.get(database, 'host')
    mariadb_connection = mariadb.connect(user = user, password = passwd, database = name) 
    cursor = mariadb_connection.cursor(buffered = True)
    insert = mariadb_connection.cursor()
    cursor.execute("SELECT year FROM main_year WHERE " + column + " " + comp +" " +  cond)
    for year_tup in cursor:
        year = year_tup[0]
        print(year)
        timeline = generate_wiki_timeline(year) 
        timeline = json.dumps(timeline)
        #store json in another file and save link to json in database
        url = "https://en.wikipedia.org/wiki/" + str(year) 
        try:
            insert.execute("""
                UPDATE main_year 
                SET wikipedia_timeline=%s,wikipedia_last_crawled=%s,url=%s
                WHERE year=%s
                """, ("timeline_json", str(datetime.now()), url, str(year)))
        except mariadb.Error as error:
            print(error)
            print("Error: ()".format(error))
    mariadb_connection.commit()

def add_wiki_timeline_all():
    """Updates wiki article timelines for all years."""
    add_wiki_timeline("TRUE", "IS", "TRUE")

def add_wiki_timeline_null():
    """Updates wiki article timelines that have not been crawled yet"""
    #update information 
    add_wiki_timeline()
    
def add_wiki_timeline_last_crawled(time):
    """Updates wiki article timelines that have not been crawled in some time."""
    return 
