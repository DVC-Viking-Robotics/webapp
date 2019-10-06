var speed;
var turn;
var speedSlider;
var turnSlider;

function initRemote(){
    speed = document.getElementById("speed");
    turn = document.getElementById("turn");
    speedSlider = new Slider(speed, !speed.className.includes("vertical"));
    turnSlider = new Slider(turn, !turn.className.includes("vertical"));
    let controls = [[turn, turnSlider], [speed, speedSlider]];
    // console.log("speed pos:", speedSlider.rect.left, speedSlider.rect.top);
    for (let ctrl of controls){
        ctrl[1].draw();
        ctrl[0].addEventListener('touchstart', touchStartOnSliders);
        ctrl[0].addEventListener('touchmove', touchMoveOnSliders);
        ctrl[0].addEventListener('touchend', touchEndOnSliders);
        ctrl[0].addEventListener('touchcancel', touchEndOnSliders);
        ctrl[0].addEventListener('mousedown', function(e){mouseStartOnSliders(e, ctrl[1]);});
        ctrl[0].addEventListener('mouseup', function(e){mouseEndOnSliders(e, ctrl[1]);});
        ctrl[0].addEventListener('mousemove', function(e){mouseMoveOnSliders(e, ctrl[1]);});
        ctrl[0].addEventListener('mouseleave', function(e){mouseEndOnSliders(e, ctrl[1]);});
    }
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
    const mouseX = (e.clientX / obj.width * 2 - 1) / ((obj.width - obj.stick.radius * 2) / obj.width) * 100;
    const mouseY = (e.clientY / obj.height * -2 + 1) / ((obj.height - obj.stick.radius * 2) / obj.height) * 100;
    obj.value = obj.horizontal ? mouseX : mouseY;
    // console.log("slider value:", obj.value);
}
