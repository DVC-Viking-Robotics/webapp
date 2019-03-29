var socket = io.connect({transports: ['websocket']});
var senses = [37.967135, -122.071210]
var gps = 
// Used to receive gps data from the raspberry pi
socket.on('gps-response', function(gps) {
    //pass gps data here
})

// Used to receive sensor9oF data from the raspberry pi
socket.on('sensor9oF-response', function(senses) {
    //pass sensor data here
})

function myMap() {
    var mapProp= {
      center:new google.maps.LatLng(37.967135, -122.071210),
      zoom:20,
      mapTypeId: google.maps.MapTypeId.SATELLITE,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);

    var bounds = {
          north: gps[0] + 0.05,
          south: gps[0] - 0.05,
          east: gps[1] + 0.05,
          west: gps[1] - 0.05
        };

        // Define the rectangle and set its editable property to true.
        rectangle = new google.maps.Rectangle({
          bounds: bounds,
          editable: true,
          draggable: true
        });

        rectangle.setMap(map);

        // Add an event listener on the rectangle.
        rectangle.addListener('bounds_changed', showNewRect);

        // Define an info window on the map.
        infoWindow = new google.maps.InfoWindow();
      }
      // Show the new coordinates for the rectangle in an info window.

      // @this {google.maps.Rectangle} 
      function showNewRect(event) {
        var ne = rectangle.getBounds().getNorthEast();
        var sw = rectangle.getBounds().getSouthWest();

        var contentString = '<b>Rectangle moved.</b><br>' +
            'New north-east corner: ' + ne.lat() + ', ' + ne.lng() + '<br>' +
            'New south-west corner: ' + sw.lat() + ', ' + sw.lng();

        // Set the info window's content and position.
        infoWindow.setContent(contentString);
        infoWindow.setPosition(ne);

        infoWindow.open(map);
      }

    