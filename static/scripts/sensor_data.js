var socket = io.connect({transports: ['websocket']});
var el_compass = document.getElementById('compass');
var el_gyro = document.getElementById('gyro');
var el_accel = document.getElementById('accel');
var el_gps = document.getElementById('gps');
var el_speed = document.getElementById('speed');

// Sensor data request loop
var dataRequestLock = setInterval(function() {
  socket.emit('gps');
  socket.emit('sensor9oF');
}, 1000);

// Used to receive gps data from the raspberry pi
socket.on('gps-response', function(gps) {
    //pass gps data here
    let output = '';
    for (let i = 0; i < gps.length; i++){
      output += gps[i];
      if (i < gps.length - 1)
        output += ', ';
    }
    console.log('gps = ' + output);
    el_gps.innerHTML = output;
});

// Used to receive sensor9oF data from the raspberry pi
socket.on('sensor9oF-response', function(senses) {
  //pass sensor data here
  for (let i = 0; i < senses.length; i++){
    let output = '';
    for (let j = 0; j < senses[i].length; j++){
      output += senses[i][j];
      if (j < senses[i].length - 1)
        output += ', ';
    }
    console.log('senses[' + i + '] = ' + output)
  }
});