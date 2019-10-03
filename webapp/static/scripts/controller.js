var cameraStream = document.getElementById('camera-stream');
var cameraStreamWrapper = document.getElementById('camera-stream-wrapper');

var speedController = document.getElementById('slider-speed-control');
var turnController = document.getElementById('slider-turning-control');

var speedOMeter = document.getElementById('speed-o-meter');
var turnOMeter = document.getElementById('turn-o-meter');

// prototype list of all data on any connected gamepads
// each item in list represents a gamepad (if any)
// each gamepad has all info about axis and buttons
var gamepads = [];
// avoid cluttering socket with duplicate data due to setInterval polling of gamepads
var prevArgs = [];

// Grab the speed and turning values and update the text as well as send them to the robot
function sendSpeedTurnValues(gamepadAxes = []) {
    var speed = null;
    var turn = null;
    if (gamepadAxes.length > 1){
        speed = round(gamepadAxes[0] * 100);
        turn = round(gamepadAxes[1] * 100);
    }
    else{
        speed = parseInt(speedController.value);
        turn = parseInt(turnController.value);
    }

    speedOMeter.innerText = speed;
    turnOMeter.innerText = turn;

    var args = [speed, turn];
    // only send data if it has changed
    if (prevArgs[0] != args[0] || prevArgs[1] != args[1]){
        prevArgs = args;
        socket.emit('remoteOut', args);
    }
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
    speedController.onmouseup = resetSliders;
    turnController.onmouseup = resetSliders;
    // event listeners for connected gamepads
    window.addEventListener("gamepadconnected", function (e) {
        console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
        e.gamepad.index, e.gamepad.id,
        e.gamepad.buttons.length, e.gamepad.axes.length);
    });
    window.addEventListener("gamepaddisconnected", function (e) {
        console.log("Gamepad disconnected from index %d: %s",
        e.gamepad.index, e.gamepad.id);
    });
    // because gamepads aren't handled with events   
    window.setInterval(getGamepadChanges, 16);
}

// get data from physical gamepads
// Google's Chrome handles gamepads differently than others, so we implement a workaraound
function getGamepadChanges() {
    // do this here as it is needed for Chrome workaround
    gamepads = navigator.getGamepads();
    /*  according to the "standard" mapping scheme
     *  (compatible w/ xBox 360 & other xinput controllers):
     * axis[0] = left stick X axis
     * axis[1] = left stick Y axis
     * axis[2] = right stick X axis
     * axis[3] = right stick Y axis
     */
    let result = [];
    // only grab data from gamepad @ index 0
    if (gamepads.length) {
        if (gamepads[0] != null) {// Chrome specific workaround
            // if there is at least 3 axes on the gamepad
            if (gamepads[0].axes.length >= 3){
                // using a deadzone of +/- 4%
                if (gamepads[0].axes[1] > 0.04 || gamepads[0].axes[1] < -0.04){
                    result.push(gamepads[0].axes[1] / 0.97); // used for speed
                }
                else{ // axis is within deadzone
                    result.push(0)
                }
                if (gamepads[0].axes[2] > 0.04 || gamepads[0].axes[2] < -0.04) {
                    result.push(gamepads[0].axes[2] / 0.97); // used for turn
                }
                else{ // axis is within deadzone
                    result.push(0)
                }
            }
        /*             
        for (i = 0; i < gamepads.length; i++){
            // show axes data
            for (j = 0; j < gamepads[i].axes.length; j++) {
                var temp = gamepads[i].axes[j];
                if (temp > 0.025 || temp < -0.025) {
                    console.log("gamepad[" + i + "], axis[" + j + "] = " + temp);
                }
            }
            //show button presses (analog triggers have preset threshold)
            for (j = 0; j < gamepads[i].buttons.length; j++) {
                var temp = gamepads[i].buttons[j].pressed;
                if (temp)
                console.log("gamepad[" + i + "], button[" + j + "] = " + temp);
            }
        }
        */
        }
    }
    // result is empty if no usable data was detected
    // otherwise result = [speed, turn]
    sendSpeedTurnValues(result);
}
