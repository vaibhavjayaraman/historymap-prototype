//later change to use npm module import
var GeoSearchControl = window.GeoSearch.GeoSearchControl;
var OpenStreetMapProvider = window.GeoSearch.OpenStreetMapProvider;
const provider = new OpenStreetMapProvider(); 
const searchControl = new GeoSearchControl({
	provider: provider, 
}); 

map.addControl(searchControl);
