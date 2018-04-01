var map;
var latitude; 
var longitude;
var zoom;

/**Initializes map. **/
function initMap() {
	latitude = 59.925580; //will be changed to use users last session data
	longitude = 30.295948; // will be changed to use users last session data
    zoom = 16; 
	map = L.map('map').setView([latitude, longitude], zoom);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', 
	{
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
		maxZoom: 18,
		id: 'mapbox.streets',
		accessToken: 'pk.eyJ1IjoidmFpYmhhdmoiLCJhIjoiY2pmZ2d1NDVjMjdzMDMzbWlhdTRtZXAyZyJ9.X3KDHMveDXHRh795LdSFmw',
    }).addTo(map);
}

/** Loads and places wikipedia articles on map. **/
function wiki_call(url) {
	alert(url);
    $.ajax({
        type: 'post',
        url: url,
        datatype: "json",
        context: document.body,
        global: false,
        async: true,
        crossdomain:true,
        success: function(data) {
            var parsed_data = data
            var articles = parsed_data.query.geosearch;
            for (var i = 0; i < articles.length; i++) {
                var article = articles[i];
                var lat = article.lat;
                var lon = article.lon;
				var title = article.title;
                var marker = L.marker([lat,lon]);
                marker.addTo(map);
                var url = "https://en.wikipedia.org/?curid="
                            + article.pageid;
				var marker_popup = function(marker, url, title) {
					return function() {
						marker.bindPopup(title.bold() + "\n" + url).openPopup();
					}
				};
                marker.on('mouseover', marker_popup(marker, url, title)); 
            }
        }
    });
}

initMap();

/**Updates map with article markers if mouse has moved. **/
$(document).ready(function() { 
    $(window).on('load', function() {
        map.on('click', function(e) {
        /**checks to make sure map.zoom is bigger than 16 */
            var zoom = map.getZoom();
            if (zoom > 16) {
                var lat = e.latlng.lat;
                var lng = e.latlng.lng;
                var radius = 1000;
                var file_return_limit = 10; 
                url = "https://en.wikipedia.org/w/api.php?" + 
                    "action=query&origin=*&list=geosearch&gscoord=" + lat + "|" + lng +
                    "&gsradius=" + radius + "&gslimit=" + file_return_limit +
                    "&prop=info|extracts&inprop=url" +
                    "&format=json";
                wiki_call(url);
            }
        });
    });
});

