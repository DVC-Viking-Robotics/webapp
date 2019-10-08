// Controller object for use on canvas element
class Joystick {
    constructor(canvas) {
        this.canvas = canvas;
        this.height = this.canvas.width;
        this.width = this.canvas.height;
        this.radius = (this.height > this.width ? this.width : this.height) / 2;
        this.color = window.getComputedStyle(this.canvas)["color"];
        this.x = 0;
        this.y = 0;
        this.stick = {
            x: 0,
            y: 0,
            angle: 0,
            touchRadius: 0,
            color: "#f3f3f3"
        }
        this.draw();
    }
    get value(){
        return [this.stick.x, this.stick.y];
    }
    set value([x, y]){
        this.stick.x = x;
        this.stick.y = y;
        this.draw();
    }
    draw() {
        this.stick.angle = Math.atan2((this.stick.y - this.y), (this.stick.x - this.x));
        this.stick.touchRadius = Math.hypot((this.stick.x - this.x), (this.stick.y - this.y));
        if (this.stick.touchRadius > this.radius) {
            this.stick.x = Math.cos(this.stick.angle) * this.radius + this.x;
            this.stick.y = Math.sin(this.stick.angle) * this.radius + this.y;
            this.stick.touchRadius = this.radius;
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
