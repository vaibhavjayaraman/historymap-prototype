var map;
var latitude; 
var longitude;
var zoom;
var current_url;
var current_title;
var win;
var wiki_markers;
var wiki_geo_search_radius = 1000;
var current_article_lat;
var current_article_lon;
var WIKI_PAGE_ID_URL = "https://en.wikipedia.org/?curid="

/**Initializes map. **/
function initMap() {
	latitude = 47.3769; //will be changed to use users last session data
	longitude = 8.5417; // will be changed to use users last session data
    zoom = 5; 
	map = L.map('map').setView([latitude, longitude], zoom);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', 
	{
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
		maxZoom: 18,
		id: 'mapbox.streets',
		accessToken: '',
    }).addTo(map);
	wiki_markers = L.layerGroup().addTo(map);
}
