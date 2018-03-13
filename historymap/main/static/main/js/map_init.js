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
