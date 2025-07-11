import pygame
import random

WIDTH, HEIGHT = 600, 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ninja vs Zombies')
clock = pygame.time.Clock()

FLOOR_HEIGHT = 50
BG = (236, 239, 241)
FLOOR = (176, 190, 197)
NINJA = (38, 50, 56)
ZOMBIE = (76, 175, 80)
ITEM = (255, 143, 0)

class Entity(pygame.Rect):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
    def draw(self, color):
        pygame.draw.rect(screen, color, self)

class Player(Entity):
    def __init__(self):
        super().__init__(50, HEIGHT - FLOOR_HEIGHT - 40, 40, 40)
        self.speed = 4
        self.health = 100
    def draw(self):
        pygame.draw.circle(screen, NINJA, (self.x + self.w//2, self.y + self.h//2), self.w//2)

class Zombie(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40)
        self.speed = 1 + random.random()
    def draw(self):
        pygame.draw.rect(screen, ZOMBIE, self)
    def update(self):
        self.x -= self.speed

class Item(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 10)
        self.speed = 6
    def draw(self):
        points = [(self.x, self.y), (self.x + self.w, self.y + self.h//2), (self.x, self.y + self.h)]
        pygame.draw.polygon(screen, ITEM, points)
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
        zombies.append(Zombie(WIDTH - 50, HEIGHT - FLOOR_HEIGHT - 40))
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
    pygame.draw.rect(screen, FLOOR, (0, HEIGHT - FLOOR_HEIGHT, WIDTH, FLOOR_HEIGHT))
    player.draw()
    for z in zombies:
        z.draw()
    for it in items:
        it.draw()

    font = pygame.font.SysFont(None, 24)
    health_surf = font.render(f'Health: {player.health}', True, (0,0,0))
    screen.blit(health_surf, (10,10))
    help_txt = font.render('Arrows move | Space throw', True, (0,0,0))
    screen.blit(help_txt, (WIDTH - 220, 10))

    if player.health <= 0:
        game_over = font.render('Game Over', True, (0,0,0))
        screen.blit(game_over, (WIDTH//2 - 40, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(2000)
        break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
