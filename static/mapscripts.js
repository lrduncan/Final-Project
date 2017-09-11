var map;

//var markers = [];

$(function () {

  function initMap() {
    var canvas = document.getElementById('map');
    var mapOptions = {
      center: {lat: 37.681057, lng: -78.203424},
      zoom: 12
    };
    map = new google.maps.Map(canvas, mapOptions);
  }

google.maps.event.addDomListener(window, 'load', initMap);

});