from configparser import ConfigParser
from historymap.settings import CONF
import requests
import re
import mysql.connector as mariadb

def remove_html(text):
    remove = re.compile('<.*?>')
    return re.sub(remove, '', text)

def generate_wiki_timeline(year, section_interests = {"Events", "Births", "Deaths"}):
    """Gets timeline information for wikipedia_year"""
    timeline = dict.fromkeys(section_interests, 0)
    year = str(year)
    wiki_api_url = "http://en.wikipedia.org/w/api.php?format=json&action=parse&prop=sections&page=" + year
    resp = requests.get(url = wiki_api_url)
    data = resp.json()
    #gets sections numbers for sections in section_interests from this article to put in timeline
    sections = data.get("parse").get("sections") 
    for section in sections:
        if section.get("line") in section_interests:
            timeline[section.get("line")] = section.get("number")

    for key in timeline.keys():
        #gets section content url
        section_content_url = "https://en.wikipedia.org/w/api.php?format=json&action=parse&page=" + year + "&section=" + timeline[key]
        resp = requests.get(url = section_content_url)
        content = resp.json().get("parse")
        timeline[key] = remove_html(content.get("text").get("*"))
    return timeline

def add_wiki_timeline():
    database = 'mysql'
    conf = ConfigParser()
    conf.read(CONF)
    name = conf.get(database, 'name')
    user = conf.get(database, 'user')
    passwd = conf.get(database, 'password')
    host = conf.get(database, 'host')
    mariadb_connection = mariadb.connect(user = user, password = passwd, database = name) 
    cursor = mariadb_conection.cursor()
    c
