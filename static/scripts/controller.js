var canvas;
var ctx;
var W;
var H;
var controller;
var moving = [ false, false ];
var gamepads = {};
var socket = io.connect();
socket.on('connect', function() {
    socket.emit('connect');
});
socket.on('disconnect', function() {
    socket.emit('disconnect');
});

function getArgs(){
    let result = [];
    let xDiameter = ((controller.joystick.x + controller.joystick.radius) - (controller.joystick.x - controller.joystick.radius)) / 2;
    let yDiameter = ((controller.joystick.y + controller.joystick.radius) - (controller.joystick.y - controller.joystick.radius)) / 2;
    let xJoyPos = (controller.joystick.x - controller.joystick.stick.x) * -1;
    let yJoyPos = (controller.joystick.y - controller.joystick.stick.y);
    let zJoyPos = controller.slider.stick.x - controller.slider.x - (controller.slider.length / 2);
    result[0] = Math.round(xJoyPos / xDiameter * 100);
    result[1] = Math.round(yJoyPos / yDiameter * 100);
    result[2] = Math.round(zJoyPos / (controller.slider.length / 2) * 100);
    return result;
}
// for edge detecting changes in controller class
var prevArgs = [0, 0, 0];

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
    if (moving[0] || moving[1]){ // currently ignores gamepads
        if (args[0] != prevArgs[0] || args[1] != prevArgs[1] || args[2] != prevArgs[2]){
            // websocket event handler call
            socket.emit('remoteOut', args);
        }
        prevArgs = args;
        window.requestAnimationFrame(loop);
    }
    else{ // no input: set output data to idle
        socket.emit('remoteOut', [0, 0, 0]);
        prevArgs = [0, 0, 0];
    }
}

function resize(){
    updateDimensions();
    ctx.clearRect(0, 0, W, H);
    controller.draw();
}

function init() {
    canvas = document.getElementById("canvas");
    canvas.addEventListener('touchstart', touchStart, false);
    canvas.addEventListener('touchmove', touchMove, false);
    canvas.addEventListener('touchend', touchEnd, false);
    canvas.addEventListener('mousedown', mouseStart, false);
    canvas.addEventListener('mouseup', mouseEnd, false);
    canvas.addEventListener('mousemove', mouseMove, false);
    ctx = canvas.getContext("2d");
    updateDimensions(); // needs to be called for instantiating the Control class
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
    window.setInterval(getAxis, 17); // because gamepads aren't handled with events
}

// Controller object for use on canvas element
class Control {
    constructor() {
        this.joystick = {
            x: 0, y: 0, radius: 0,
            color: "grey",
            stick: {
                x: 0, y: 0, radius: 0,
                color: "blue",
                angle: null,
                touchRadius: 0
            },
            draw: function () {
                this.stick.angle = Math.atan2((this.stick.y - this.y), (this.stick.x - this.x));

                this.stick.touchRadius = Math.hypot((this.stick.x - this.x), (this.stick.y - this.y));
                if (this.stick.touchRadius > this.radius) {
                    this.stick.x = Math.cos(this.stick.angle) * this.radius + this.x;
                    this.stick.y = Math.sin(this.stick.angle) * this.radius + this.y;
                }
                ctx.beginPath();
                ctx.fillStyle = this.color;
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.fillStyle = this.stick.color;
                ctx.arc(this.stick.x, this.stick.y, this.stick.radius, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        this.slider = {
            x: 0, y: 0, height: 0, length: 0,
            color: "grey",
            stick: {
                x: 0, y: 0, radius: 0,
                color: "red",
            },
            draw: function () {
                this.stick.x = Math.max(this.x, Math.min(this.stick.x, this.x + this.length));
                ctx.strokeStyle = this.color;
                ctx.beginPath();
                ctx.lineCap = "round";
                ctx.lineWidth = this.height;
                ctx.moveTo(this.x + this.height / 2, this.y);
                ctx.lineTo(this.x + this.length - this.height / 2, this.y);
                ctx.stroke();
                ctx.fillStyle = this.stick.color;
                ctx.beginPath();
                ctx.arc(this.stick.x, this.stick.y, this.stick.radius, 0, Math.PI * 2);
                ctx.fill();
            }
        }
    }
    update() { // used for monitoring window size
        this.joystick.x = W > H ? W / 4 : W / 2;
        this.joystick.y = W > H ? H / 2 : H / 4;
        this.joystick.radius = Math.hypot((W > H ? W : H) / 2, (W > H ? H : W)) / 5;
        this.joystick.stick.radius = this.joystick.radius / 4;
        this.slider.x = (W > H ? W / 2 : 0) + 10;
        this.slider.y = W > H ? H / 2 : H * 3 / 4;
        this.slider.height = (W > H ? H : W) / 16;
        this.slider.length = W - this.slider.x - 10;
        this.slider.stick.radius = this.slider.height * 0.75;
        if (!moving[0] && !moving[1]) {// when in idle only
            this.joystick.stick.x = this.joystick.x;
            this.joystick.stick.y = this.joystick.y;
            this.slider.stick.x = this.slider.x + this.slider.length / 2;
            this.slider.stick.y = this.slider.y;
        }
    }
    draw() {
        this.update();
        this.joystick.draw();
        this.slider.draw();
    }
}// end canvas's controller object

// capture data from touch and mouse input
function touchStart(e) {
    //getTouchPos(e);   
    moving[0] = true;
    e.preventDefault();// prevent canceling this event
    window.requestAnimationFrame(loop);
}

function touchMove(e) {
    if(moving[0]) getTouchPos(e);
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
            var touch = e.touches[0];
            for (let touch of e.touches) {
                var touchX = touch.pageX - touch.target.offsetLeft;
                var touchY = touch.pageY - touch.target.offsetTop;
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
    var mouseX = e.pageX - e.target.offsetLeft;
    var mouseY = e.pageY - e.target.offsetTop;
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
    /*  according to the "standard" mapping scheme 
     *  (compatible w/ xBox 360 & other xinput controllers):
     * axis[0] = left stick X axis
     * axis[1] = left stick Y axis
     * axis[2] = right stick X axis
     * axis[3] = right stick Y axis
     */
    hasMovement = false;
    for (i = 0; i < gamepads.length; i++) {
        if (gamepads[i] != null) {// Chrome specific workaround
            if (gamepads[i].axes.length >= 2 && ((gamepads[i].axes[0] > 0.03 || gamepads[i].axes[0] < -0.04) || (gamepads[i].axes[1] > 0.04 || gamepads[i].axes[1] < -0.04))) {
                controller.joystick.stick.x = controller.joystick.x + (controller.joystick.radius * (gamepads[i].axes[0] / 0.97));
                controller.joystick.stick.y = controller.joystick.y + (controller.joystick.radius * (gamepads[i].axes[1] / 0.97));
                hasMovement = true;
            }
            if (gamepads[i].axes.length >= 3 && (gamepads[i].axes[2] > 0.03 || gamepads[i].axes[2] < -0.03)) {
                controller.slider.stick.x = controller.slider.x + (controller.slider.length / 2) + ((controller.slider.length / 2 - controller.slider.height / 2) * (gamepads[i].axes[2] / 0.97));
                hasMovement = true;

            }
/*             // show axes data
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
*/
        }
        if (hasMovement) {
            moving[1] = true;
            window.requestAnimationFrame(loop);
        }
        else moving[1] = false;
    }
}
