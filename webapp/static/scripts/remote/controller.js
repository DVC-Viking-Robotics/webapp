let canvas;
let ctx;
let W;
let H;
let controller;
let moving = [false, false];
let gamepads = {};

// gather data from the controller object
function getArgs() {
    let result = [];
    // new algo to return x,y as polar coordinates
    let radius = Math.round(controller.joystick.stick.touchRadius / controller.joystick.radius * 100);
    let theta = Math.round(controller.joystick.stick.angle / Math.PI * 200);
    // atan2() in controller.joystick returns negative for all positive y values and postitive for negative y values
    radius *= theta < 0 ? 1 : -1;
    theta = radius == 0 ? 0 : ((Math.abs(theta) - 100) * -1);
    let zJoyPos = controller.slider.stick.x - controller.slider.x - (controller.slider.length / 2);
    result[0] = theta;
    result[1] = radius;
    result[2] = Math.round(zJoyPos / (controller.slider.length / 2) * 100);
    return result;
}
// for edge detecting changes in controller class
let prevArgs = [0, 0, 0];

function updateDimensions() {
    W = window.innerWidth - 5;
    H = window.innerHeight - 70;
    canvas.width = W;
    canvas.height = H;
}

function loop() {
    ctx.clearRect(0, 0, W, H);
    controller.draw();
    let args = getArgs();
    // establish a base case when there is no input event
    if (moving[0] || moving[1]) {
        if (args[0] != prevArgs[0] || args[1] != prevArgs[1] || args[2] != prevArgs[2]) {
            socket.emit('remoteOut', args);
            console.log('remoteOut', args);
        }
        prevArgs = args;
        window.requestAnimationFrame(loop);
    }
    else { // no input: set output data to idle
        socket.emit('remoteOut', [0, 0, 0]);
        console.log('remoteOut', [0, 0, 0]);
        prevArgs = [0, 0, 0];
    }
}

function resize() {
    updateDimensions();
    ctx.clearRect(0, 0, W, H);
    controller.draw();
}

controls = []

function initRemote() {
    updateDimensions(); // needs to be called before instantiating the Controller classes
    canvas = document.getElementsByTagName("canvas");
    for (let i in canvas){
        canvas[i].addEventListener('touchstart', touchStart, false);
        canvas[i].addEventListener('touchmove', touchMove, false);
        canvas[i].addEventListener('touchend', touchEnd, false);
        canvas[i].addEventListener('mousedown', mouseStart, false);
        canvas[i].addEventListener('mouseup', mouseEnd, false);
        canvas[i].addEventListener('mousemove', mouseMove, false);
        ctx = canvas[i].getContext("2d");
        if (canvas[i].id == "joystick")
            controls.push(new Joystick);
        else if (canvas[i].id == "horizontal-slider")
            controls.push(new Slider("horizontal"));
        else if (canvas[i].id == "vertical-slider")
            controls.push(new Slider("vertical"));
    }
    controller = new Control();
    window.addEventListener("gamepadconnected", function (e) {
        console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
            e.gamepad.index, e.gamepad.id,
            e.gamepad.buttons.length, e.gamepad.axes.length);
    });
    window.addEventListener("gamepaddisconnected", function (e) {
        console.log("Gamepad disconnected from index %d: %s",
            e.gamepad.index, e.gamepad.id);
    });
    window.addEventListener('resize', resize);// when window is resized
    window.requestAnimationFrame(loop);

    window.setInterval(getAxis, 16); // because gamepads aren't handled with events
}


// capture data from touch and mouse input
function touchStart(e) {
    //getTouchPos(e);
    moving[0] = true;
    e.preventDefault();// prevent canceling this event
    window.requestAnimationFrame(loop);
}

function touchMove(e) {
    if (moving[0]) getTouchPos(e);
    e.preventDefault();
}

function touchEnd(e) {
    if (e.touches.length == 0)
        moving[0] = false;
    else moving[0] = true;
}

function getTouchPos(e) {
    if (e.touches) {
        if (e.touches.length >= 1) {
            const touch = e.touches[0];
            for (let touch of e.touches) {
                const touchX = touch.pageX - touch.target.offsetLeft;
                const touchY = touch.pageY - touch.target.offsetTop;
                if ((W > H ? touchX : touchY) < (W > H ? W : H) / 2) {
                    controller.joystick.stick.x = touchX;
                    controller.joystick.stick.y = touchY;
                }
                else {
                    controller.slider.stick.x = touch.pageX - touch.target.offsetLeft
                }
            }
        }
    }
}

// need to add mouse out of focus sentinal function
function mouseStart(e) {
    moving[0] = true;
    getMousePos(e);
    e.preventDefault();// prevent canceling this event
    window.requestAnimationFrame(loop);
}

function mouseMove(e) {
    if (moving[0]) getMousePos(e);
    e.preventDefault();
}

function mouseEnd(e) {
    moving[0] = false;
}

function getMousePos(e) {
    const mouseX = e.pageX - e.target.offsetLeft;
    const mouseY = e.pageY - e.target.offsetTop;
    if ((W > H ? mouseX : mouseY) < (W > H ? W : H) / 2) {
        controller.joystick.stick.x = mouseX;
        controller.joystick.stick.y = mouseY;
    }
    else {
        controller.slider.stick.x = mouseX;
    }
}

// get data from physical gamepads
function getAxis() {
    gamepads = navigator.getGamepads();
    /* according to the "standard" mapping scheme
     * (compatible w/ xBox 360 & other xinput controllers):
     * axis[0] = left stick X axis
     * axis[1] = left stick Y axis
     * axis[2] = right stick X axis
     * axis[3] = right stick Y axis
     */
    hasMovement = false;
    for (i = 0; i < gamepads.length; i++) {
        if (gamepads[i] != null) {// Chrome specific workaround
            if (gamepads[i].axes.length >= 2 && ((gamepads[i].axes[0] > 0.04 || gamepads[i].axes[0] < -0.04) || (gamepads[i].axes[1] > 0.04 || gamepads[i].axes[1] < -0.04))) {
                controller.joystick.stick.x = controller.joystick.x + (controller.joystick.radius * (gamepads[i].axes[0] / 0.97));
                controller.joystick.stick.y = controller.joystick.y + (controller.joystick.radius * (gamepads[i].axes[1] / 0.97));
                hasMovement = true;
            }
            if (gamepads[i].axes.length >= 3 && (gamepads[i].axes[2] > 0.04 || gamepads[i].axes[2] < -0.04)) {
                controller.slider.stick.x = controller.slider.x + (controller.slider.length / 2) + ((controller.slider.length / 2 - controller.slider.height / 2) * (gamepads[i].axes[2] / 0.97));
                hasMovement = true;

            }
            /* 
            // show axes data
            for (j = 0; j < gamepads[i].axes.length; j++) {
                let temp = gamepads[i].axes[j];
                if (temp > 0.025 || temp < -0.025) {
                    console.log("gamepad[" + i + "], axis[" + j + "] = " + temp);
                }
            }
            //show button presses (analog triggers have preset threshold)
            for (j = 0; j < gamepads[i].buttons.length; j++) {
                let temp = gamepads[i].buttons[j].pressed;
                if (temp)
                    console.log("gamepad[" + i + "], button[" + j + "] = " + temp);
            }
             */
        }
        if (hasMovement) {
            moving[1] = true;
            window.requestAnimationFrame(loop);
        }
        else moving[1] = false;
    }
}