var tile_overlay = null;
var opacity = .7;

function addRegionTiles(region, year) {
	tile = L.tileLayer("http://oilspill.ocf.berkeley.edu:2000/" + region + "/" + year + "/{z}/{x}/{y}.png", {
		tms: true, 
		opacity: opacity,
		className : region,
	}).addTo(tile_overlay);
}

/**Add functionality that will allow one to add and remove individual tile overlays **/

function addTiles(year) {
	//if switching to vector tiles, use L.TileLayer.MVTSource
	tile_overlay = L.layerGroup().addTo(map);
	addRegionTiles("iberia", year);
}


/** Supress 404 errors that arise when tileserver does not have specified tile */ 
map.on('error', e => {
	if (e && e.error != '404 (File not found)')
		console.error(e);
});

/** Updates page with wikipedia timeline for that year
**/

function add_wikipedia_timeline(timeline_text) {
	document.getElementById('wiki_year_timeline').innerHTML = "This Happened this year:" + timeline_text;
}

/** Adds timeline from wikipedia. **/
function addWikiYearTimeline(year) {
	console.log(year);
	$.ajax({
		type: 'POST', 
		url:"main/wiki_timeline/", 
	    	async: true, 
		data: {
			'name': 'year', 
			'year': year, 
		}, 
		dataType: 'json', 
		success: function(data) {
			add_wikipedia_timeline(data.timeline);
		}
	});
}

/** Changes year to year specified in html form **/
function change_year(){
	if (tile_overlay != null) {
		map.removeLayer(tile_overlay);
	}
	//include check to make sure that year is a number
	var year = document.getElementById("year_input").value;
	if (!isNaN(year)) {
		addTiles(year);
		addWikiYearTimeline(year)
		document.getElementById('beginning').innerHTML = "The World in " + year;
	} else {
		alert("Please Enter a number for year and resubmit.");
	}
}

/**Removes overlay tiles **/
function remove_year() {
	if (tile_overlay != null) {
		map.removeLayer(tile_overlay);
	}
	tile_overlay = null;
	document.getElementById('beginning').innerHTML = "The World Today";
}

