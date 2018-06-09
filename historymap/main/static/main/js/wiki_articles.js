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

function article_ajax_call(url_data, title, request_type, lat, lon) {
    	var wikipedia_title = "https://en.wikipedia.org/api/rest_v1/page/summary/" + title.replace(/ /g, "_");
	$.ajax({
		type: 'post',
		url:"",
		async: true, 
		data: {
			'name': 'wiki_article',
			'url' : url_data,
			'title' : title,
			'interaction_type': request_type,
			'title_for_wikipedia' : wikipedia_title,
			'lat': lat,
			'lon': lon,
		},
		failure: function(data) {
			alert("Article Ajax Call Fail");
		}
	});
}

function wiki_marker_popup(marker, url, title, lat, lon) {
	return function() {
		var extract = extract_wikipedia_head(title);
                current_url = url;
		current_title = title;
		current_article_lat = lat;
		current_article_lon = lon;
		article_ajax_call(url, title, 'hover', lat, lon);
		marker.bindPopup('<button class="article">' + title.bold() + '</button><p>' 
        	+ extract + "<\p>").openPopup();
	}
}
function add_wiki_marker(lat, lon, pageid, title) {
	var marker = L.marker([lat,lon]);
        marker.addTo(wiki_markers);
	var url = WIKI_PAGE_ID_URL + pageid;
	article_ajax_call(url, title,'generation', lat, lon);
        marker.on('mouseover', wiki_marker_popup(marker, url, title, lat, lon)); 
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
            if (articles.length == 0) {
		    alert("This location does not seem to be around wikipedia articles");
	    } else {
		    for (var i = 0; i < articles.length; i++) {
			var article = articles[i];
			add_wiki_marker(article.lat, article.lon, article.pageid, article.title)
            	}
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
		article_ajax_call(current_url, current_title, 'click', current_article_lat, current_article_lon);
            });
    });
});

