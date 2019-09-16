
var el_gps = document.getElementById('gps');
var el_compass = document.getElementById('compass');
// Sensor data request loop
var dataRequestLock = setInterval(function () {
    socket.emit('gps');
    // socket.emit('sensorDoF');
}, 1000);

// Used to receive gps data from the raspberry pi
socket.on('gps-response', function (gps) {
    //pass gps data here
    let output = '';
    for (let i = 0; i < gps.length; i++) {
        output += gps[i];
        if (i < gps.length - 1)
            output += ', ';
    }
    console.log('gps = ' + output);
    if (robotMarker)
        robotMarker.setPosition({ lat: gps[0], lng: gps[1] });
    map.setCenter({ lat: gps[0], lng: gps[1] });
    el_gps.innerHTML = output;
});

// Used to receive heading data from the raspberry pi
socket.on('heading-response', function (heading) {
    console.log('heading = ' + heading);
    el_compass.innerHTML = heading;
});