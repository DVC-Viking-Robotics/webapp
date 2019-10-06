// Controller object for use on canvas element
class Slider {
    constructor(canvas, horizontal = true) {
        this.canvas = canvas;
        this.rect = this.canvas.parentNode.getBoundingClientRect();
        this.ctx = this.canvas.getContext("2d");
        this.height = this.rect.bottom - this.rect.top;
        this.width = this.rect.right - this.rect.left;
        this.canvas.height = this.height;
        this.canvas.width = this.width;
        this.horizontal = horizontal;
        this.color = window.getComputedStyle(this.canvas)["color"];
        this.pos = 0;
        this.x = 0;
        this.y = 0;
        this.stick = {
            x: 0, y: 0, radius: 0,
            color: "#f3f3f3",
            manip: false // for shrink/swell of stick on manipulation
        };
    }
    set value(val){
        this.pos = Math.max(-100, Math.min(100, val));
        this.draw();
    }
    get value(){
        return this.pos;
    }
    draw() {
        this.ctx.clearRect(0, 0, this.width, this.height);
        this.ctx.strokeStyle = this.color;
        this.ctx.fillStyle = this.stick.color;
        this.ctx.beginPath();
        this.ctx.lineCap = "round";
        if (this.horizontal){
            // draw slider
            this.ctx.lineWidth = this.height / 3;
            this.ctx.moveTo(this.x + this.height / 4, this.y + this.height / 2);
            this.ctx.lineTo(this.x + this.width - this.height / 4, this.y + this.height / 2);
            this.ctx.stroke();
            // draw stick
            this.stick.radius = this.height * (this.stick.manip ? 0.35 : 0.3);
            this.stick.x = this.x + this.width / 2 + (this.pos / 200 * (this.width - this.stick.radius * 2));
            this.stick.y = this.y + this.height / 2;
        }
        else{
            // draw slider
            this.ctx.lineWidth = this.width / 3;
            this.ctx.moveTo(this.x + this.width / 2, this.y + this.width / 4);
            this.ctx.lineTo(this.x + this.width / 2, this.y + this.height - this.width / 4);
            this.ctx.stroke();
            // draw stick
            this.stick.radius = this.width * (this.stick.manip ? 0.35 : 0.3);
            this.stick.x = this.x + this.width / 2;
            this.stick.y = this.y + this.height / 2 + (this.pos / -200 * (this.height - this.stick.radius * 2));
        }
        this.ctx.beginPath();
        this.ctx.arc(this.stick.x, this.stick.y, this.stick.radius, 0, Math.PI * 2);
        let gradient = this.ctx.createRadialGradient(this.stick.x, this.stick.y, this.stick.radius * 0.25, this.stick.x, this.stick.y, this.stick.radius * 0.6);
        gradient.addColorStop(0, '#a3a3a3');
        gradient.addColorStop(0.7, '#f3f3f3');
        this.ctx.fillStyle = gradient;        
        this.ctx.fill();

    }
}// end canvas's slider object
