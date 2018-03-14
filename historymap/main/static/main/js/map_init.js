var map;
var latitude;
var longitude;

function initMap() {
	latitude = 59.925580;
	longitude = 30.295948;
	map = new google.maps.Map(document.getElementById('map'), {
		center: {lat: latitude, lng: longitude},
		zoom: 6 
	});
}

function map_call() {
    var api_key =  'AIzaSyAa8xh6DKU5tSCrqMc22HeLdXHDWoRioRw';
    var url = 'https://maps.googleapis.com/maps/api/js?key=' + api_key + '&callback=initMap';
    var js_file = document.createElement('script');
    js_file.type = 'text/javascript';
    js_file.src = url;
    $("#map").append(js_file);
}

map_call();
function calculateCoordinates(pnt) {
    /**Returns information about point **/
    var obj = {
        lat: pnt.lat().toFixed(4),
        lng: pnt.lng().toFixed(4),
        zoom: map.zoom,
    }
    return obj;
}

$(window).load(function() {
    /**Updates map with article markers if mouse has moved**/

    google.maps.event.addListener(map, 'click', function (event) {
        /**checks to make sure map.zoom is bigger than 16 */
        if (map.zoom > 16) {
            var map_state = calculateCoordinates(event.latlng);
            var lat = map_state.lat;
            var lng = map_state.lng;
            var radius = 6;
            var file_return_limit = 50;
            console.log(lat, lng, radius);
            $.ajax({
                type: 'POST',
                url: "https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord=${lat}|${lng}&gsradius=${radius}&gslimit=${file_return_limit}",
                data: {lat: lat, lng: lng, zoom: zoom},
                dataType: "json",
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
});
