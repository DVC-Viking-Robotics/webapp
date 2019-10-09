var cameraStream = document.getElementById('camera-stream');
var cameraStreamWrapper = document.getElementById('camera-stream-wrapper');
var speedController = document.getElementById("speed");
var turnController = document.getElementById("turn");
var speedOMeter = document.getElementById('speed-o-meter');
var turnOMeter = document.getElementById('turn-o-meter');
var speedSlider;
var turnSlider;

// prototype list of all data on any connected gamepads
// each item in list represents a gamepad (if any)
// each gamepad has all info about axis and buttons
var gamepads = [];
// avoid cluttering socket with duplicate data due to setInterval polling of gamepads
var prevArgs = [];

// Grab the speed and turning values and update the text as well as send them to the robot
function sendSpeedTurnValues(gamepadAxes = []) {
    let speed = null;
    let turn = null;
    if (gamepadAxes.length){
        speed = Math.round(gamepadAxes[0] * 100);
        turn = Math.round(gamepadAxes[1] * 100);
        speedSlider.value = speed;
        turnSlider.value = turn;
    }
    else{
        speed = speedSlider.value;
        turn = turnSlider.value;
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
    let newCamRect = cameraStream.getBoundingClientRect();
    speedController.width = 80;
    speedController.height = Math.round(newCamRect.height);
    turnController.width = Math.round(newCamRect.width);
    turnController.height = 80;
    // console.log("new Cam dimensions:", Math.round(newCamRect.width), 'x', Math.round(newCamRect.height));
    speedSlider.resize();
    turnSlider.resize();
}

function initRemote(){
    // speedController = document.getElementById("speed");
    // turnController = document.getElementById("turn");
    speedSlider = new Slider(speedController, !speedController.className.includes("vertical"));
    turnSlider = new Slider(turnController, !turnController.className.includes("vertical"));
    let controls = [{el: turnController, obj: turnSlider}, {el: speedController, obj: speedSlider}];
    adjustSliderSizes();
    window.addEventListener('resize', adjustSliderSizes);
    for (let ctrl of controls){
        ctrl.obj.draw();
        ctrl.el.addEventListener('touchstart', touchStartOnSliders);
        ctrl.el.addEventListener('touchmove', touchMoveOnSliders);
        ctrl.el.addEventListener('touchend', touchEndOnSliders);
        ctrl.el.addEventListener('touchcancel', touchEndOnSliders);
        ctrl.el.addEventListener('mousedown', function(e){mouseStartOnSliders(e, ctrl.obj);});
        ctrl.el.addEventListener('mouseup', function(e){mouseEndOnSliders(e, ctrl.obj);});
        ctrl.el.addEventListener('mousemove', function(e){mouseMoveOnSliders(e, ctrl.obj);});
        ctrl.el.addEventListener('mouseleave', function(e){mouseEndOnSliders(e, ctrl.obj);});
    }

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

// detirmine if touch point is in the slider's rect
function isWithinRect(touchPos, objRect){
    let [x, y] = touchPos;
    // console.log(x, "<", objRect.right, "&& >", objRect.left)
    if (x < objRect.right && x > objRect.left)
        if (y < objRect.bottom && y > objRect.top)
            return true;
    return false;
}

// capture data from touch and mouse input
function touchStartOnSliders(e) {
    getTouchPos(e);
    e.preventDefault();// prevent canceling this event
}

function touchMoveOnSliders(e) {
    getTouchPos(e);
    e.preventDefault();
}

function touchEndOnSliders(e) {
    getTouchPos(e);
}

function getTouchPos(e) {
    let controls = [turnSlider, speedSlider];
    let touchesHandled = [false, false];
    for (let touch of e.touches) {
        let touchX = touch.clientX;
        let touchY = touch.clientY;
        for (let i = 0; i < controls.length; i++){
            if (isWithinRect([touchX, touchY], controls[i].rect)){
                touchX = (touchX / controls[i].width * 2 - 1) / ((controls[i].width - controls[i].stick.radius * 2) / controls[i].width) * 100;
                touchY = (touchY / controls[i].height * -2 + 1) / ((controls[i].height - controls[i].stick.radius * 2) / controls[i].height) * 100;
                controls[i].manip = true;
                controls[i].value = controls[i].horizontal ? touchX : touchY;
                touchesHandled[i] = true;
            }
        }
    }
    for (let i = 0; i < touchesHandled.length; i++){
        if (!touchesHandled[i]) {
            controls[i].manip = false;
            controls[i].value = 0;
        }
    }
}

// need to add mouse out of focus sentinal function
function mouseStartOnSliders(e, obj) {
    obj.stick.manip = true;
    getMousePosOnSliders(e, obj);
    e.preventDefault();// prevent canceling this event
}

function mouseMoveOnSliders(e, obj) {
    if(e.buttons == 1){
        getMousePosOnSliders(e, obj);
    }    
    e.preventDefault();
}

function mouseEndOnSliders(e, obj) {
    obj.stick.manip = false;
    obj.value = 0;
}

function getMousePosOnSliders(e, obj) {
    let targetRect = e.target.getBoundingClientRect();
    const mouseX = ((e.pageX - targetRect.left) / obj.width * 2 - 1) / ((obj.width - obj.stick.radius * 2) / obj.width) * 100;
    const mouseY = ((e.pageY - targetRect.top) / obj.height * -2 + 1) / ((obj.height - obj.stick.radius * 2) / obj.height) * 100;
    obj.value = obj.horizontal ? mouseX : mouseY;
    // console.log("slider value:", obj.value);
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
                    result.push(gamepads[0].axes[1] * -1); // used for speed
                }
                else{ // axis is within deadzone
                    result.push(0);
                }
                if (gamepads[0].axes[2] > 0.04 || gamepads[0].axes[2] < -0.04) {
                    result.push(gamepads[0].axes[2]); // used for turn
                }
                else{ // axis is within deadzone
                    result.push(0);
                }
            }
        }
    }
    // result is empty if no gamepad was initialized
    // otherwise result = [speed, turn]
    sendSpeedTurnValues(result);
}
/* 
// show gamepad button presses
// analog triggers have a preset threshold that make them behave like buttons
for (i = 0; i < gamepads.length; i++){
    for (j = 0; j < gamepads[i].buttons.length; j++) {
        var temp = gamepads[i].buttons[j].pressed;
        if (temp)
        console.log("gamepad[" + i + "], button[" + j + "] = " + temp);
    }
}
*/
