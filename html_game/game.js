const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');

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
  update() {
    this.x -= this.speed;
  }
}

class Item extends Entity {
  constructor(x, y) {
    super(x, y, 10, 10, '#ffab40');
    this.speed = 6;
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

function spawnZombie() {
  zombies.push(new Zombie(canvas.width - 50, canvas.height - 60));
}

function update() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
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
