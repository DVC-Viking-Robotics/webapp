// Controller object for use on canvas element
class Joystick {
    constructor() {
            this.x = 0;
            this.y = 0;
            this.radius = 0;
            this.color = "grey";
            this.stick = {
                x: 0,
                y: 0,
                radius: 0,
                color: "#008B8B",
                angle: 0,
                touchRadius: 0
            }
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
        update() { // used for monitoring window size
            this.joystick.x = W > H ? W / 4 : W / 2;
            this.joystick.y = W > H ? H / 2 : H / 4;
            this.joystick.radius = Math.hypot((W > H ? W : H) / 2, (W > H ? H : W)) / 5;
            this.joystick.stick.radius = this.joystick.radius / 4;
            if (!moving[0] && !moving[1]) {// when in idle only
                this.joystick.stick.x = this.joystick.x;
                this.joystick.stick.y = this.joystick.y;
        }
    }
}
