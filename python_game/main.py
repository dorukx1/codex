import pygame
import random

WIDTH, HEIGHT = 600, 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ninja vs Zombies')
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BG = (224, 242, 241)
NINJA = (38, 50, 56)
ZOMBIE = (141, 110, 99)
ITEM = (255, 171, 64)

class Entity(pygame.Rect):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
    def draw(self, color):
        pygame.draw.rect(screen, color, self)

class Player(Entity):
    def __init__(self):
        super().__init__(50, HEIGHT-60, 40, 40)
        self.speed = 4
        self.health = 100

class Zombie(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40)
        self.speed = 1 + random.random()
    def update(self):
        self.x -= self.speed

class Item(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 10)
        self.speed = 6
    def update(self):
        self.x += self.speed

player = Player()
zombies = []
items = []
spawn_timer = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            items.append(Item(player.x + player.width, player.y + player.height//2))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x = max(0, player.x - player.speed)
    if keys[pygame.K_RIGHT]:
        player.x = min(WIDTH - player.width, player.x + player.speed)

    spawn_timer += 1
    if spawn_timer > 60:
        zombies.append(Zombie(WIDTH-50, HEIGHT-60))
        spawn_timer = 0

    for z in zombies[:]:
        z.update()
        if z.x + z.width < 0:
            zombies.remove(z)
            player.health -= 10

    for it in items[:]:
        it.update()
        for z in zombies[:]:
            if it.colliderect(z):
                zombies.remove(z)
                if it in items:
                    items.remove(it)
                break
        if it.x > WIDTH and it in items:
            items.remove(it)

    screen.fill(BG)
    player.draw(NINJA)
    for z in zombies:
        z.draw(ZOMBIE)
    for it in items:
        it.draw(ITEM)

    font = pygame.font.SysFont(None, 24)
    health_surf = font.render(f'Health: {player.health}', True, (0,0,0))
    screen.blit(health_surf, (10,10))

    if player.health <= 0:
        game_over = font.render('Game Over', True, (0,0,0))
        screen.blit(game_over, (WIDTH//2 - 40, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(2000)
        break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
