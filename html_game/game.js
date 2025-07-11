const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');

const BG_COLOR = '#eceff1';
const FLOOR_COLOR = '#b0bec5';

class Entity {
  constructor(x, y, w, h, color) {
    this.x = x; this.y = y; this.w = w; this.h = h; this.color = color;
  }
  draw() {
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x, this.y, this.w, this.h);
  }
}

class Player extends Entity {
  constructor() {
    super(50, canvas.height - 60, 40, 40, '#263238');
    this.speed = 4;
    this.health = 100;
  }
  draw() {
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.x + this.w / 2, this.y + this.h / 2, this.w / 2, 0, Math.PI * 2);
    ctx.fill();
  }
  move(dir) {
    this.x += dir * this.speed;
    this.x = Math.max(0, Math.min(canvas.width - this.w, this.x));
  }
}

class Zombie extends Entity {
  constructor(x, y) {
    super(x, y, 40, 40, '#8d6e63');
    this.speed = 1 + Math.random();
  }
  draw() {
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x, this.y, this.w, this.h);
    ctx.fillStyle = '#2e7d32';
    ctx.fillRect(this.x + 5, this.y + 5, this.w - 10, this.h - 10);
  }
  update() {
    this.x -= this.speed;
  }
}

class Item extends Entity {
  constructor(x, y) {
    super(x, y, 10, 10, '#ffab40');
    this.speed = 6;
  }
  draw() {
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.moveTo(this.x, this.y);
    ctx.lineTo(this.x + this.w, this.y + this.h / 2);
    ctx.lineTo(this.x, this.y + this.h);
    ctx.closePath();
    ctx.fill();
  }
  update() {
    this.x += this.speed;
  }
}

const player = new Player();
let zombies = [];
let items = [];
let keys = {};
let spawnTimer = 0;

function drawBackground() {
  ctx.fillStyle = BG_COLOR;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = FLOOR_COLOR;
  ctx.fillRect(0, canvas.height - 50, canvas.width, 50);
}

function spawnZombie() {
  zombies.push(new Zombie(canvas.width - 50, canvas.height - 60));
}

function update() {
  drawBackground();
  if (keys['ArrowLeft']) player.move(-1);
  if (keys['ArrowRight']) player.move(1);
  spawnTimer++;
  if (spawnTimer > 100) { spawnZombie(); spawnTimer = 0; }
  zombies.forEach((z, zi) => {
    z.update();
    if (z.x < 0) { zombies.splice(zi, 1); player.health -= 10; }
  });
  items.forEach((it, ii) => {
    it.update();
    zombies.forEach((z, zi) => {
      if (it.x < z.x + z.w && it.x + it.w > z.x && it.y < z.y + z.h && it.y + it.h > z.y) {
        zombies.splice(zi, 1); items.splice(ii, 1);
      }
    });
    if (it.x > canvas.width) items.splice(ii, 1);
  });
  player.draw();
  zombies.forEach(z => z.draw());
  items.forEach(it => it.draw());
  ctx.fillStyle = 'black';
  ctx.fillText('Health: ' + player.health, 10, 20);
  ctx.fillText('Arrows: move  |  Space: throw', canvas.width - 230, 20);
  if (player.health <= 0) {
    ctx.fillText('Game Over', canvas.width / 2 - 30, canvas.height / 2);
    return;
  }
  requestAnimationFrame(update);
}

window.addEventListener('keydown', e => {
  keys[e.key] = true;
  if (e.key === ' ') {
    items.push(new Item(player.x + player.w, player.y + player.h / 2));
  }
});
window.addEventListener('keyup', e => { keys[e.key] = false; });

update();
