// TODO: uncomment receiving sensor data

const el_gps = document.getElementById('gps');
// const el_compass = document.getElementById('compass');

// Sensor data request loop
const dataRequestLock = setInterval(function () {
    socket.emit('gps');
}, 1000);

// Used to receive gps data from the raspberry pi
socket.on('gps-response', function (gps) {
    const robotPos = { lat: gps[0], lng: gps[1] };
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