# historymap-prototype
This is a prototype written using the Django web framework and vanilla javascript/jquery. 
To run prototype locally: Use standard Django conventions:
        python3 manage.py runserver 0.0.0.0:PORT
To also display historical maps in prototype: 
        Place a webserver (python3 -m http.server PORT) at the root of the directory with all the region tiles, and have the ajax requests (in add_tiles.js) point to the url of this webserver. 
        
