var tile_overlay = null;
function addTiles(year) {
	tile_overlay = L.tileLayer("http://oilspill.ocf.berkeley.edu:5000/tiles/" + year + "/{z}/{x}/{y}.png", {tms: true, opacity: .7}).addTo(map)
}


/** Supress 404 errors that arise when tileserver does not have specified tile */ 
map.on('error', e => {
	if (e && e.error != '404 (File not found)')
		console.error(e);
});

/** Changes year to year specified in html form **/
function change_year(){
	if (tile_overlay != null) {
		map.removeLayer(tile_overlay);
	}
	//include check to make sure that year is a number
	var year = document.getElementById("year_input").value;
	addTiles(year);
	document.getElementById('beginning').innerHTML = "The World in " + year;
}

/**Removes overlay tiles **/
function remove_year() {
	if (tile_overlay != null) {
		map.removeLayer(tile_overlay);
	}
	tile_overlay = null;
	document.getElementById('beginning').innerHTML = "The World Today";
}
