# historymap-prototype
</br>
This is a prototype written using the Django web framework and vanilla javascript/jquery. 
</br>
To run prototype locally: Use standard Django conventions: </br>
        python3 manage.py runserver 0.0.0.0:PORT</br>
To also display historical maps in prototype: </br>
        Place a webserver (python3 -m http.server PORT) at the root of the directory with all the region tiles, and have the ajax requests (in add_tiles.js) point to the url of this webserver. 
        
