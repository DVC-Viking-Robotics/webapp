// In the following example, markers appear when the user clicks on the map.
// The markers are stored in an array.
// The user can then click an option to hide, show or delete the markers.
let map;
const ground0 = { lat: 37.96713657090229, lng: -122.0712176165581 };
let markers = [];
let robotMarker;
const dLat = 0.00001, dLng = 0.00001;
let uPos, rPos;

const enableSockets = true;

const txtGps = document.getElementById('gps');

function printMarkers() {
    for (let i = 0; i < markers.length; i++) {
        console.log(markers[i].label + ': ' + markers[i].getPosition())
    }
}

function setInitialMarkers() {
    // Adds a marker at the center of the map.
    robotMarker = addMarker(ground0, false, "Robot", false);

    // ask's to Add your locaction to the map
    getLocation();
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showYourPosition);
    }
}

function showYourPosition(position) {
    uPos = { lat: position.coords.latitude, lng: position.coords.longitude };
    // updateGPSReadout(uPos);
    addMarker(uPos, false, "You", false);
}

// gets your GPS location and updates '#gps' element
function updateGPSReadout(pos) {
    txtGps.innerHTML = '(' + pos.lat.toFixed(5) + ', ' + pos.lng.toFixed(5) + ')';
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 20,
        center: ({ lat: ground0.lat, lng: ground0.lng }),
        mapTypeId: 'satellite'
    });
    // console.log(ground0);
    // This event listener will call addMarker() when the map is clicked.
    map.addListener('click', function (event) {
        addMarker(event.latLng, true, null, true);
    });

    setInitialMarkers();
}

// Adds a marker to the map and push to the array.
function addMarker(location, canDrag, label, addToArray) {
    if (label === null)
        label = String.fromCharCode(65 + markers.length);

    const marker = new google.maps.Marker({
        position: location,
        map: map,
        draggable: canDrag,
        label: label
    });

    if (addToArray === true)
        markers.push(marker);

    return marker;
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
    for (let i = 0; i < markers.length; i++) {
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
// Do add the initial markers though.
function deleteMarkers() {
    clearMarkers();
    markers = [];
    setInitialMarkers();
}

function latPlus() {
    const tempLen = markers.length - 1;
    const temp = { lat: markers[tempLen].getPosition().lat() + dLat, lng: markers[tempLen].getPosition().lng() };
    markers[tempLen].setPosition(temp);
}
function latMinus() {
    const tempLen = markers.length - 1;
    const temp = { lat: markers[tempLen].getPosition().lat() - dLat, lng: markers[tempLen].getPosition().lng() };
    markers[tempLen].setPosition(temp);
}
function lngPlus() {
    const tempLen = markers.length - 1;
    const temp = { lat: markers[tempLen].getPosition().lat(), lng: markers[tempLen].getPosition().lng() + dLng };
    markers[tempLen].setPosition(temp);
}
function lngMinus() {
    const tempLen = markers.length - 1;
    const temp = { lat: markers[tempLen].getPosition().lat(), lng: markers[tempLen].getPosition().lng() - dLng };
    markers[tempLen].setPosition(temp);
}

function copyMarkers() {
    // assemble modified shadow copy for transfering to navigator
    let result = [];
    for (let i = 1; i < markers.length; ++i) {
        if (markers[i].label != 'You') {
            let currPos = result.push({ lat: markers[i].getPosition().lat(), lng: markers[i].getPosition().lng() });
            console.log(currPos + ' = ' + result[currPos - 1].lat + '; ' + result[currPos - 1].lng)
        }
    }
    return result;
}

function dumpMarkers(clear = true) {
    // console.log('sending waypoints list')
    if (enableSockets)
        socket.emit('WaypointList', copyMarkers(), clear);
    else
        console.log('WaypointList', copyMarkers(), clear);
}