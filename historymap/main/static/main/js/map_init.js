var map;
var latitude;
var longitude;

function initMap() {
	latitude = 59.925580;
	longitude = 30.295948;
	map = new google.maps.Map(document.getElementById('map'), {
		center: {lat: latitude, lng: longitude},
		zoom: 17 
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

/**Updates map with article markers if mouse has moved**/

$(document).ready(function() { 
    $(window).on('load', function() {
        google.maps.event.addListener(map, 'click', function (event) {
        /**checks to make sure map.zoom is bigger than 16 */
            var zoom = map.getZoom();
            if (zoom > 16) {
                var pos = event.latLng;
                var lat = pos.lat();
                var lng = pos.lng();
                var radius = 1000;
                var file_return_limit = 10; 
                $.ajax({
                    type: 'POST',
                    url: "https://en.wikipedia.org/w/api.php?origin=*&action=query&list=geosearch&gscoord="+ lat +"|" + lng +"&gsradius=" + radius +"&gslimit=" + file_return_limit + "&format=json",
                    data: {lat: lat, lng: lng, zoom: zoom},
                    dataType: "json",
                    context: document.body,
                    global: false,
                    async: true,
                    crossDomain:true,
                    success: function(data) {
                        alert(url);
                        alert(data);
                        alert(Object.keys(data));
                        alert(Object.values(data));
                        var parsedData = JSON.parse(data);
                        var articles = parsedData.query.geosearch;
                        for (var i = 0; i < articles.length; i++) {
                            var article = articles[i];
                            new google.maps.Marker({
                                position: {lat: article.lat, lng: article.lng},
                                map: map,
                                title: article.title,
                            });
                        }
                    }
                });
            }
        })
    })
});
