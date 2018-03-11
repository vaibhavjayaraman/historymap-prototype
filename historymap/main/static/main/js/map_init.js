var map;
document.addEventListener('DOMContentLoaded', function() {
	var api_key = 'AIzaSyBByYGtP4MGtNAd9-SxOPdXk5WJML9b1gA'
    if (document.querySelectorAll('map').length > 0) {
        var js_file = document.createElement('script');
        js_file.type = 'text/javascript';
        js_file.src = 'https://maps.googleapis.com/maps/api/js?key=${api_key}&callback=initMap';
		document.getElementsByTagName('head')[0].appendChild(js_file);
    }
}

function initMap() {
	var latitude = 59.925580
	var longitude = 30.295948
	map = new google.maps.Map(document.getElementById('map'), {
		center: {lat: latitude, lng: longitude},
		zoom: 8 
	});
}

$(document).ready(function() {
    /**Updates map with article markers if mouse has moved**/
    function calculateCoordinates(pnt) {
        /**Returns information about point **/
        var obj = {
            lat: pnt.lat().toFixed(4),
            lng = pnt.lng().toFixed(4),
            zoom: map.zoom,
        }
        return obj;
    }

    google.maps.event.addListener(map, 'mousemove', function (event) {
        /**checks to make sure map.zoom is bigger than 16 */
        if (map.zoom > 16) {
        var map_state = calculateCoordinates(event.latlng);
    
            $.ajax({
                type: 'POST',
                url: "/main/generate_wiki_articles.py",
                data: {lat: map_state.lat, lng: map_state.lng, zoom: map.zoom}
                dataType: "json";
                context: document.body,
                global: false,
                async: false,
                success: function(data) {
                    function plotMarkers(markers) {
                        markers.forEach(function (marker) {
                            var position = new google.maps.LatLng(
                                marker.lat, 
                                marker.lng);
                            var marker = new google.maps.Marker({
                                position: position,
                                map: map,
                                animation: google.maps.Animation.DROP
                            });
                        });
                    }
                }
            });
        }
    });
}

