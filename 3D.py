import pygame, math, random

pygame.init()

# ================= SCREEN =================
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft-like 3D (Pygame)")
clock = pygame.time.Clock()

# ================= RAYCAST =================
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
SCALE = WIDTH // NUM_RAYS

# ================= MAP =================
MAP_W, MAP_H = 24, 24
TILE = 100

world_map = [[0]*MAP_W for _ in range(MAP_H)]

# Map generator
for y in range(MAP_H):
    for x in range(MAP_W):
        if x == 0 or y == 0 or x == MAP_W-1 or y == MAP_H-1:
            world_map[y][x] = 1
        elif random.random() < 0.15:
            world_map[y][x] = random.choice([1, 2])

# 1 grass | 2 stone

# ================= PLAYER =================
px, py = 300, 300
angle = 0
speed = 3
vel_y = 0
gravity = 0.6
jump_power = -10
on_ground = True
height = 0

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# ================= INVENTORY =================
inventory = {1: 10, 2: 10}
selected = 1

# ================= COLORS =================
SKY = (135, 206, 235)
GROUND = (60, 60, 60)
COLORS = {
    1: (80, 200, 80),   # grass
    2: (120, 120, 120) # stone
}

# ================= RAYCAST =================
def raycast():
    cur_angle = angle - HALF_FOV
    for ray in range(NUM_RAYS):
        for depth in range(1, MAX_DEPTH * TILE):
            x = px + depth * math.cos(cur_angle)
            y = py + depth * math.sin(cur_angle)
            mx, my = int(x//TILE), int(y//TILE)

            if world_map[my][mx]:
                depth *= math.cos(angle - cur_angle)
                h = DIST / (depth + 0.0001)

                block = world_map[my][mx]
                shade = max(0, 255 - depth * 0.4)
                color = tuple(min(255, c * shade // 255) for c in COLORS[block])

                pygame.draw.rect(
                    screen,
                    color,
                    (ray*SCALE, HEIGHT//2 - h//2 - height, SCALE, h)
                )
                break
        cur_angle += DELTA_ANGLE

# ================= GAME LOOP =================
while True:
    screen.fill(SKY)
    pygame.draw.rect(screen, GROUND, (0, HEIGHT//2, WIDTH, HEIGHT//2))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); exit()

        if e.type == pygame.MOUSEBUTTONDOWN:
            tx = int((px + math.cos(angle)*150)//TILE)
            ty = int((py + math.sin(angle)*150)//TILE)

            if e.button == 1 and world_map[ty][tx]:
                inventory[world_map[ty][tx]] += 1
                world_map[ty][tx] = 0

            if e.button == 3 and inventory[selected] > 0:
                if world_map[ty][tx] == 0:
                    world_map[ty][tx] = selected
                    inventory[selected] -= 1

    keys = pygame.key.get_pressed()

    # Mouse look
    mx, _ = pygame.mouse.get_rel()
    angle += mx * 0.003

    # Movement
    dx = math.cos(angle) * speed
    dy = math.sin(angle) * speed

    if keys[pygame.K_w]:
        px += dx; py += dy
    if keys[pygame.K_s]:
        px -= dx; py -= dy
    if keys[pygame.K_a]:
        px += dy; py -= dx
    if keys[pygame.K_d]:
        px -= dy; py += dx

    # Jump & gravity
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump_power
        on_ground = False

    vel_y += gravity
    height += vel_y
    if height > 0:
        height = 0
        vel_y = 0
        on_ground = True

    # Inventory select
    if keys[pygame.K_1]: selected = 1
    if keys[pygame.K_2]: selected = 2

    raycast()
    pygame.display.flip()
    clock.tick(60)