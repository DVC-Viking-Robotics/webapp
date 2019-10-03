var cameraStream = document.getElementById('camera-stream');
var cameraStreamWrapper = document.getElementById('camera-stream-wrapper');

var speedController = document.getElementById('slider-speed-control');
var turnController = document.getElementById('slider-turning-control');

var speedOMeter = document.getElementById('speed-o-meter');
var turnOMeter = document.getElementById('turn-o-meter');

const enableSockets = true;

function sendSpeedTurnValues() {
    var speed = parseInt(speedController.value);
    var turn = parseInt(turnController.value);

    speedOMeter.innerText = speed;
    turnOMeter.innerText = turn;

    var args = [speed, turn];

    if (enableSockets)
        socket.emit('remoteOut', args);
    else
        console.log('remoteOut', args);
}

function resetSliders() {
    speedController.value = 0;
    turnController.value = 0;
    sendSpeedTurnValues();
}

function adjustSliderSizes() {
    speedController.style.height = cameraStream.clientHeight + 'px';
    turnController.style.width = cameraStream.clientWidth + 'px';
}

function initRemote() {
    // This is used for resizing the sliders
    new ResizeSensor(cameraStreamWrapper, adjustSliderSizes);

    speedController.addEventListener('input', sendSpeedTurnValues);
    turnController.addEventListener('input', sendSpeedTurnValues);

    speedController.onmouseup = resetSliders;
    turnController.onmouseup = resetSliders;
}