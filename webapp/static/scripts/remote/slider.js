// Controller object for use on canvas element
class Slider {
    constructor(canvas, horizontal = true) {
        this.canvas = canvas;
        this.rect = 0;
        this.height = this.canvas.width;
        this.width = this.canvas.height;
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
        this.resize();
    }
    resize(){
        // let currentStyle = window.getComputedStyle(this.canvas.id);
        let currentStyle = this.canvas.getBoundingClientRect();
        // console.log(this.canvas.id, currentStyle.width, currentStyle.height);
        this.height = currentStyle.height;
        this.width = currentStyle.width;
        this.draw();
    }
    set value(val){
        this.pos = Math.max(-100, Math.min(100, Math.round(val)));
        this.draw();
    }
    get value(){
        return this.pos;
    }
    draw() {
        let ctx = this.canvas.getContext("2d");
        ctx.clearRect(0, 0, this.width, this.height);
        ctx.strokeStyle = this.color;
        ctx.fillStyle = this.stick.color;
        ctx.beginPath();
        ctx.lineCap = "round";
        if (this.horizontal){
            // draw slider
            ctx.lineWidth = this.height / 3;
            ctx.moveTo(this.x + this.height / 4, this.y + this.height / 2);
            ctx.lineTo(this.x + this.width - this.height / 4, this.y + this.height / 2);
            ctx.stroke();
            // draw stick
            this.stick.radius = this.height * (this.stick.manip ? 0.35 : 0.3);
            this.stick.x = this.x + this.width / 2 + (this.pos / 200 * (this.width - this.stick.radius * 2));
            this.stick.y = this.y + this.height / 2;
        }
        else{
            // draw slider
            ctx.lineWidth = this.width / 3;
            ctx.moveTo(this.x + this.width / 2, this.y + this.width / 4);
            ctx.lineTo(this.x + this.width / 2, this.y + this.height - this.width / 4);
            ctx.stroke();
            // draw stick
            this.stick.radius = this.width * (this.stick.manip ? 0.35 : 0.3);
            this.stick.x = this.x + this.width / 2;
            this.stick.y = this.y + this.height / 2 + (this.pos / -200 * (this.height - this.stick.radius * 2));
        }
        ctx.beginPath();
        ctx.arc(this.stick.x, this.stick.y, this.stick.radius, 0, Math.PI * 2);
        let gradient = ctx.createRadialGradient(this.stick.x, this.stick.y, this.stick.radius * 0.25, this.stick.x, this.stick.y, this.stick.radius * 0.6);
        gradient.addColorStop(0, '#a3a3a3');
        gradient.addColorStop(0.7, '#f3f3f3');
        ctx.fillStyle = gradient;        
        ctx.fill();
    }
}// end canvas's slider object
