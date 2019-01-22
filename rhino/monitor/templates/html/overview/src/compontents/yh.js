/**
 * Created by Administrator on 2017/11/21.
 */
import $ from 'jquery';
(function ($) {
    window.Fireworks = function (options) {
        let obj = $('#'+options.id);
        options = options || {};
        options.width = options.width || obj.width();
        options.height = options.height || obj.height();
        let fireworksField = obj,
            SCREEN_WIDTH = options.width,
            SCREEN_HEIGHT = options.height,
            rockets = [],
            particles = [];
        let	canvas = document.createElement("canvas");
        canvas.style.width = SCREEN_WIDTH + 'px';
        canvas.style.height = SCREEN_HEIGHT + 'px';
        canvas.width = SCREEN_WIDTH;
        canvas.height = SCREEN_HEIGHT;
        canvas.style.position = 'absolute';
        canvas.style.top = '0px';
        canvas.style.left = '0px';
        let context = canvas.getContext('2d');
        let mousePos = {};
        let gravity = 0.05;
        let raf;

        $(fireworksField).append(canvas);
        document.onmousemove = mouseMove;
        setInterval(launch, 1000);
        raf = window.requestAnimationFrame(loop);

        function mouseMove(ev){
            ev = ev || window.event;
            mousePos = mousePosition(ev);
        }
        function mousePosition(ev){
            if(ev.pageX || ev.pageY){
                return {x:ev.pageX, y:ev.pageY};
            }
            return {
                x:ev.clientX + document.body.scrollLeft - document.body.clientLeft,
                y:ev.clientY + document.body.scrollTop - document.body.clientTop
            };
        }
        function launch() {
            if (rockets.length < 10) {
                let rocket = new Rocket(SCREEN_WIDTH/2);
                rocket.v.x = Math.random() * 6 - 3;
                rocket.v.y = Math.random() * -30 -4;
                rocket.color = Math.floor(Math.random() * 360 / 10) * 10;
                rockets.push(rocket);
            }
        }
        function loop () {
            let existRockets = [];
            let existParticles = [];
            if (SCREEN_WIDTH != window.innerWidth) {
                canvas.width = SCREEN_WIDTH = window.innerWidth;
            }
            if (SCREEN_HEIGHT != window.innerHeight) {
                canvas.height = SCREEN_HEIGHT = window.innerHeight;
            }
            context.fillStyle = "rgba(0,0,0,0.05)";
            context.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
            //context.save();
            for (let i = 0; i < rockets.length; i ++) {
                rockets[i].update();
                rockets[i].render(context);
                //explosion rules
                //1.above the 4/5 screen
                //2.close to the mouse
                //3.1% random chance above the 1/2 screen
                let distance = Math.sqrt(Math.pow(mousePos.x - rockets[i].pos.x, 2) + Math.pow(mousePos.y - rockets[i].pos.y, 2));
                let randomChance = (rockets[i].pos.y < SCREEN_HEIGHT/2)? (Math.random() * 100 <= 1) : false;
                if (rockets[i].pos.y < SCREEN_HEIGHT/5  || distance <= 50 || randomChance) {
                    rockets[i].explode();
                }else{
                    existRockets.push(rockets[i]);
                }
            }
            rockets = existRockets;
            for (let i = 0; i < particles.length; i ++) {
                particles[i].update();
                if (particles[i].exist()) {
                    particles[i].render(context);
                    existParticles.push(particles[i]);
                }
            }
            particles = existParticles;
            //context.restore();
            raf = window.requestAnimationFrame(loop);
        }
        //the particles object
        function Particle (pos) {
            this.pos = {
                x : pos? pos.x:0,
                y : pos? pos.y:0
            };
            this.v = {
                x : 0,
                y : 0
            };
            this.resistance = 0.005;
            this.size = 3;
            this.shrink = 0.99;
            this.alpha = 1;
            this.fade = 0.97;
            this.color = "";
        }
        Particle.prototype.update = function () {
            this.v.x += this.resistance;
            this.v.y -= this.resistance;
            //gravity
            this.v.y += gravity;
            this.pos.x += this.v.x;
            this.pos.y += this.v.y;
            this.size *= this.shrink;
            this.alpha *= this.fade;
        }
        Particle.prototype.render = function () {
            let x = this.pos.x,
                y = this.pos.y,
                r = this.size/2;
            let gradient = context.createRadialGradient(x, y, 0.1, x, y, r);
            gradient.addColorStop(0, "rgba(255, 255, 255, "+ this.alpha +")");
            gradient.addColorStop(0.9, "hsla(" + this.color + ", 100%, 50%, 1)");
            gradient.addColorStop(1, "rgba(0, 0, 0, 0.5)");
            context.fillStyle = gradient;
            context.beginPath();
            context.arc(x, y, r, 0, 2 * Math.PI, true);
            context.closePath();
            context.fill();
        }
        Particle.prototype.exist = function () {
            if (this.alpha >= 0.02 && this.size > 0.8) {
                return true;
            }else{
                return false;
            }
        }
        //the rocket object
        function Rocket (x) {
            Particle.apply(this, [{
                x : x,
                y : SCREEN_HEIGHT
            }]);
        }
        (function () {
            let Super = function () {};
            Super.prototype = Particle.prototype;
            Rocket.prototype = new Super();
        })();
        Rocket.prototype.constructor = Rocket;
        Rocket.prototype.update = function () {
            this.pos.x += this.v.x;
            this.pos.y += this.v.y;
        }
        Rocket.prototype.render = function (context) {
            let x = this.pos.x,
                y = this.pos.y,
                r = this.size/2;
            let gradient = context.createRadialGradient(x, y, 0.1, x, y, r);
            gradient.addColorStop(0, "#ffff00");
            gradient.addColorStop(1, "rgba(0, 0, 0, 1)");
            context.fillStyle = gradient;
            context.beginPath();
            context.arc(x, y, r, 0, 2 * Math.PI, true);
            context.closePath();
            context.fill();
        }
        Rocket.prototype.explode = function () {
            let count = getGaussianDistributionNumber(240, 20);
            for (let i = 0; i <= count; i++) {
                let particle = new Particle(this.pos);
                let angle = Math.random() * Math.PI * 2;
                let speed =  getGaussianDistributionNumber(2.5, 0.3);
                particle.size = 3;
                particle.v.x = Math.cos(angle) * speed;
                particle.v.y = Math.sin(angle) * speed;
                particle.color = this.color;
                particles.push(particle);
            }
        }
        function getGaussianDistributionNumber (mean, std_dev) {
            let U1 = -Math.random() + 1;
            let U2 = -Math.random() + 1;
            let R = Math.sqrt(-2 * Math.log(U2));
            let a = 2 * Math.PI * U1;
            let Z = R * Math.cos(a);
            return mean + (Z * std_dev);
        }
    }

}($));

module.exports  = Fireworks;