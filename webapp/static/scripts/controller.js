var cameraStream = document.getElementById('camera-stream');
var cameraStreamWrapper = document.getElementById('camera-stream-wrapper');

var speedController = document.getElementById('slider-speed-control');
var turnController = document.getElementById('slider-turning-control');

var speedOMeter = document.getElementById('speed-o-meter');
var turnOMeter = document.getElementById('turn-o-meter');

// Grab the speed and turning values and update the text as well as send them to the robot
function sendSpeedTurnValues() {
    var speed = parseInt(speedController.value);
    var turn = parseInt(turnController.value);

    speedOMeter.innerText = speed;
    turnOMeter.innerText = turn;

    var args = [speed, turn];

    socket.emit('remoteOut', args);
}

// Take the width/height of the camera feed and adjust the sliders accordingly
function adjustSliderSizes() {
    speedController.style.height = cameraStream.clientHeight + 'px';
    turnController.style.width = cameraStream.clientWidth + 'px';
}

function resetSliders() {
    speedController.value = 0;
    turnController.value = 0;

    // Make sure to update the text and robot with the new readings
    sendSpeedTurnValues();
}

function initRemote() {
    // This is used for resizing the sliders dynamically for responsiveness compliance
    // The wrapper is needed since resize monitoring doesn't work on 'img' tags
    new ResizeSensor(cameraStreamWrapper, adjustSliderSizes);

    // Whenever the slider moves around, send the values to the robot
    speedController.addEventListener('input', sendSpeedTurnValues);
    turnController.addEventListener('input', sendSpeedTurnValues);

    // Reset the sliders to their zero whenever the user lets go of either slider
    speedController.addEventListener('mouseup', resetSliders);
    turnController.addEventListener('mouseup', resetSliders);
}