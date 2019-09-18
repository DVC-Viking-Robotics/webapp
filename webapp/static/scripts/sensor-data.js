// TODO: uncomment receiving sensor data

var el_gps = document.getElementById('gps');
// var el_compass = document.getElementById('compass');

// Sensor data request loop
var dataRequestLock = setInterval(function () {
    socket.emit('gps');
    // socket.emit('sensorDoF');
}, 1000);

// Used to receive gps data from the raspberry pi
socket.on('gps-response', function (gps) {
    var robotPos = { lat: gps[0], lng: gps[1] };
    updateGPSReadout(robotPos);

    if (robotMarker)
        robotMarker.setPosition(robotPos);

    map.setCenter(robotPos);
});

// Used to receive heading data from the raspberry pi
// socket.on('heading-response', function (heading) {
//     console.log('heading = ' + heading);
//     el_compass.innerHTML = heading;
// });