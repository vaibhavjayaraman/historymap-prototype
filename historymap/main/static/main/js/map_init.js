alert("qwerty");


var map;
$("map").append("Append test");
function initMap() {
	var latitude = 59.925580
	var longitude = 30.295948
	map = new google.maps.Map(document.getElementById('map'), {
		center: {lat: latitude, lng: longitude},
		zoom: 8 
	});
}
$(document).ready(function() {
	var api_key = 'AIzaSyBByYGtP4MGtNAd9-SxOPdXk5WJML9b1gA'
    var js_file = document.createElement('script');
    js_file.type = 'text/javascript';
    js_file.src = 'https://maps.googleapis.com/maps/api/js?key=api_key&callback=initMap';
    $("map").append(js_file);
}

$(window).load(function() {
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
        var lat = map_state.lat;
        var lng = map_state.lng;
        var radius = 6;
        var file_return_limit = 50;
        $.ajax({
            type: 'POST',
            url: "https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord=${lat}|${lng}&gsradius=${radius}&gslimit=${file_return_limit}",
            data: {lat: map_state.lat, lng: map_state.lng, zoom: map.zoom},
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

