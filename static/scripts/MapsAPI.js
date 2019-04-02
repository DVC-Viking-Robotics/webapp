
// In the following example, markers appear when the user clicks on the map.
// The markers are stored in an array.
// The user can then click an option to hide, show or delete the markers.
var map;
var ground0 = {lat: 37.96713657090229, lng: -122.0712176165581};
var markers = [];

function printMarkers(){
    for (var i = 0; i < markers.length; i++) {
        console.log(markers[i].label + ': ' + markers[i].getPosition())
    }
}

function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    }
}
  
function showPosition(position) {
    uPos  = {lat:position.coords.latitude , lng:position.coords.longitude};
    addMarker(uPos, false, "You");
}
  
function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: ({lat: ground0.lat, lng: ground0.lng}),
        mapTypeId: 'terrain'
    });
    // console.log(ground0);
    // This event listener will call addMarker() when the map is clicked.
    map.addListener('click', function(event) {
        addMarker(event.latLng, true, null);
    });
    
    // Adds a marker at the center of the map.
    addMarker(ground0, false, "Robot");
    // ask's to Add your locaction to the map 
    getLocation();
}

// Adds a marker to the map and push to the array.
function addMarker(location, canDrag, label) {
    if (label == null){
        label = String.fromCharCode(64 + markers.length);
    }
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        draggable: canDrag,
        label: label
    });
    markers.push(marker);
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
        console.log(markers[i].label + ': ' + markers[i].getPosition())
    }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
    setMapOnAll(null);
}

// Shows any markers currently in the array.
function showMarkers() {
    setMapOnAll(map);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    clearMarkers();
    markers = [];
}

function latPlus(){
    var tempLen = markers.length - 1;
    var temp = {lat: markers[tempLen].getPosition().lat() + 0.01, lng: markers[tempLen].getPosition().lng()};
    markers[tempLen].setPosition(temp);
}
function latMinus(){
    var tempLen = markers.length - 1;
    var temp = {lat: markers[tempLen].getPosition().lat() - 0.01, lng: markers[tempLen].getPosition().lng()};
    markers[tempLen].setPosition(temp);
}
function lngPlus(){
    var tempLen = markers.length - 1;
    var temp = {lat: markers[tempLen].getPosition().lat(), lng: markers[tempLen].getPosition().lng() + 0.01};
    markers[tempLen].setPosition(temp);
}
function lngMinus(){
    var tempLen = markers.length - 1;
    var temp = {lat: markers[tempLen].getPosition().lat(), lng: markers[tempLen].getPosition().lng() - 0.01};
    markers[tempLen].setPosition(temp);
}
