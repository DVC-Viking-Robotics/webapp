// Controller object for use on canvas element
class Slider {
    constructor(orientation = "horizontal") {
        this.x = 0;
        this.y = 0;
        this.height = 0;
        this.length = 0;
        this.color = "grey";
        this.orientation = orientation;
        this.stick = {
            x: 0, y: 0, radius: 0,
            y: 0, radius: 0,
            color: "#FF4500",
        };
    }
    draw() {
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
    update() { // used for monitoring window size
        this.slider.x = (W > H ? W / 2 : 0) + 10;
        this.slider.y = W > H ? H / 2 : H * 3 / 4;
        this.slider.height = (W > H ? H : W) / 16;
        this.slider.length = W - this.slider.x - 20;
        this.slider.stick.radius = this.slider.height * 0.75;
        if (!moving[0] && !moving[1]) {// when in idle only
            this.slider.stick.x = this.slider.x + this.slider.length / 2;
            this.slider.stick.y = this.slider.y;
        }
    }
}// end canvas's slider object
