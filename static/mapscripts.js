var map;

//var markers = [];

$(function () {

  function initMap() {
    var canvas = document.getElementById('map');
    var mapOptions = {
      center: {lat: 37.681057, lng: -78.203424},
      zoom: 9
    };
    map = new google.maps.Map(canvas, mapOptions);
    var marker = new google.maps.Marker({
      position: {lat: 37.681057, lng: -78.203424},
      map: map,
      title: 'Duncan Trucking',
      animation: google.maps.Animation.DROP,
      icon: 'https://maps.gstatic.com/mapfiles/ms2/micons/homegardenbusiness.png'
    });
  }

google.maps.event.addDomListener(window, 'load', initMap);

});

function addMarker(place)
{
  var myLatLng = {lat: place.latitude, lng: place.longitude};
    var icon1 = 'http://maps.google.com/mapfiles/kml/pal2/icon31.png';

    var marker = new google.maps.Marker({
        position: myLatLng,
        label: place.place_name + "," + place.admin_name1,
        map: map,
        icon: icon1
    });
}