var map;
var latitude; 
var longitude;
var zoom;
var current_url;
var current_title;
var win;
var wiki_markers;
var wiki_geo_search_radius = 1000;
var WIKI_PAGE_ID_URL = "https://en.wikipedia.org/?curid="

/**Initializes map. **/
function initMap() {
	latitude = 59.925580; //will be changed to use users last session data
	longitude = 30.295948; // will be changed to use users last session data
    zoom = 5; 
	map = L.map('map').setView([latitude, longitude], zoom);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', 
	{
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
		maxZoom: 18,
		id: 'mapbox.streets',
		accessToken: 'pk.eyJ1IjoidmFpYmhhdmoiLCJhIjoiY2pmZ2d1NDVjMjdzMDMzbWlhdTRtZXAyZyJ9.X3KDHMveDXHRh795LdSFmw',
    }).addTo(map);
	wiki_markers = L.layerGroup().addTo(map);
}
var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

$.ajaxSetup({
   beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

/**Function retrieves wikipedia article first paragraph. In browser Cache at a later time */
function extract_wikipedia_head(title) {
    var extract;
    title = title.replace(/ /g,"_");
    var url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + title
    $.ajax({
        type: 'GET',
        url: url,
        datatype: "json",
        context: document.body,
        global: false,
        async: false, //async = true leaves head undefined
        crossdomain:true,
        success: function(data) {
            extract = data.extract;
        }
    });
    return extract;
}

function article_ajax_call(url_data, title, request_type) {
    	var wikipedia_title = "https://en.wikipedia.org/api/rest_v1/page/summary/" + title.replace(/ /g, "_");
	$.ajax({
		type: 'post',
		url:"",
		async: true, 
		data: {
			'url' : url_data,
			'title' : title,
			'interaction_type': request_type,
			'title_for_wikipedia' : wikipedia_title,
		},
		failure: function(data) {
			alert("Article Ajax Call Fail");
		}
	});
}

function wiki_marker_popup(marker, url, title) {
	return function() {
		var extract = extract_wikipedia_head(title);
                current_url = url;
		current_title = title;
		article_ajax_call(url, title, 'hover');
		marker.bindPopup('<button class="article">' + title.bold() + '</button><p>' 
        	+ extract + "<\p>").openPopup();
	}
}
function add_wiki_marker(lat, lon, pageid, title) {
	var marker = L.marker([lat,lon]);
        marker.addTo(wiki_markers);
	var url = WIKI_PAGE_ID_URL + pageid;
	article_ajax_call(url, title,'generation');
        marker.on('mouseover', wiki_marker_popup(marker, url, title)); 
}

/** Loads and places wikipedia articles on map. **/
function wiki_call(url) {
    $.ajax({
        type: 'GET',
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
		add_wiki_marker(article.lat, article.lon, article.pageid, article.title)
            }
        }
    });
}

initMap();

/**Updates map with article markers if mouse has moved. **/
$(document).ready(function() { 
    $(window).on('load', function() {
        map.on('click', function(e) {
                var lat = e.latlng.lat;
                var lng = e.latlng.lng;
                var file_return_limit = 5; 
                url = "https://en.wikipedia.org/w/api.php?" + 
                    "action=query&origin=*&list=geosearch&gscoord=" + lat + "|" + lng +
                    "&gsradius=" + wiki_geo_search_radius + "&gslimit=" + file_return_limit +
                    "&prop=info|extracts&inprop=url" +
                    "&format=json";
                wiki_call(url);
        });
            $('#map').on('click', '.article', function() {
                win = window.open(current_url, '_blank');
		article_ajax_call(current_url, current_title, 'click');
            });
    });
});

