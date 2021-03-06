var map;
var geocoder;
var markers = [];
var counter = 0;

$(function () {

  function initMap() {
    var canvas = document.getElementById('map');
    var mapOptions = {
      center: {lat: 37.681057, lng: -78.203424},
      zoom: 9
    };
    map = new google.maps.Map(canvas, mapOptions);
    geocoder = new google.maps.Geocoder();
    var marker = new google.maps.Marker({
      position: {lat: 37.681057, lng: -78.203424},
      map: map,
      title: 'Duncan Trucking',
      animation: google.maps.Animation.DROP,
      icon: 'https://maps.gstatic.com/mapfiles/ms2/micons/homegardenbusiness.png'
    });

  }

google.maps.event.addDomListener(window, 'load', initMap);
google.maps.event.addDomListener(window, 'load', update);
});

function update()
{
  $.getJSON("/markers")
  .done(function(data, textStatus, jqXHR){
        for (var i = 0; i < data.length; i++)
        {
          if (i % 2 == 0)
            addMarker(data[i]);
          else
            addInfo(data[i]);
        }
  })
  .fail(function(jqXHR, textStatus, errorThrown) {
        // log error to browser's console
        console.log(errorThrown.toString());
  });
}

function addMarker(place)
{
  var myLatLng = {lat: place.lat, lng: place.lng};

  var marker = new google.maps.Marker({
      position: myLatLng,
      map: map,
  });

  markers.push(marker);

}

function addInfo(place)
{
  var windowcontent = place.comments;

  var infowindow = new google.maps.InfoWindow({
    content: windowcontent
  });

  var marker = markers[counter];

  if (marker != undefined)
    marker.addListener('click', function() {
      infowindow.open(map, marker);
    });
    google.maps.event.addListener(map, 'click', function() {
      infowindow.close();
    });

  counter++;
}