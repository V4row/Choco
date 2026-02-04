import pygame
import random
import sys
import time

pygame.init()

# ======================
# WINDOW
# ======================
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fighting Game - Kick & Ultimate")
clock = pygame.time.Clock()

# ======================
# COLORS
# ======================
WHITE = (240, 240, 240)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 100, 220)
PURPLE = (160, 60, 200)
YELLOW = (255, 220, 50)
ORANGE = (255, 150, 50)
BLACK = (0, 0, 0)

# ======================
# FONTS
# ======================
FONT = pygame.font.SysFont(None, 30)
BIG_FONT = pygame.font.SysFont(None, 48)

# ======================
# ENTITY
# ======================
def create_fighter(x, hp=100, damage=1.0, facing=1):
    return {
        "x": x,
        "y": 250,
        "w": 50,
        "h": 80,
        "hp": hp,
        "max_hp": hp,
        "blocking": False,
        "combo": 0,
        "last_attack": 0,
        "cooldown": 0,
        "damage": damage,
        "facing": facing,
        "punch_time": 0,
        "kick_time": 0,
        "hit_effect": 0,
        "ultimate_cd": 0
    }

PLAYER = create_fighter(150, facing=1)
ENEMY = create_fighter(600, facing=-1)

# ======================
# GAME STATE
# ======================
level = 1
MAX_LEVEL = 3
game_over = False
level_clear = False
screen_shake = 0

# ======================
# DRAW
# ======================
def draw_hp_bar(x, y, hp, max_hp):
    pygame.draw.rect(screen, RED, (x, y, 220, 22))
    pygame.draw.rect(screen, GREEN, (x, y, 220 * (hp / max_hp), 22))

def draw_fighter(f, color):
    pygame.draw.rect(screen, color, (f["x"], f["y"], f["w"], f["h"]))

    # Punch
    if f["punch_time"] > 0:
        px = f["x"] + (f["w"] if f["facing"] == 1 else -30)
        pygame.draw.rect(screen, YELLOW, (px, f["y"] + 30, 30 * f["facing"], 10))

    # Kick
    if f["kick_time"] > 0:
        kx = f["x"] + (f["w"] if f["facing"] == 1 else -40)
        pygame.draw.rect(screen, ORANGE, (kx, f["y"] + 55, 40 * f["facing"], 12))

    # Hit effect
    if f["hit_effect"] > 0:
        pygame.draw.circle(
            screen, YELLOW,
            (f["x"] + f["w"] // 2, f["y"] + f["h"] // 2),
            22, 2
        )

# ======================
# COMBAT
# ======================
def base_damage(attacker):
    return (8 + attacker["combo"] * 4) * attacker["damage"]

def attack(attacker, defender):
    now = time.time()

    attacker["combo"] = attacker["combo"] + 1 if now - attacker["last_attack"] < 0.6 else 1
    attacker["combo"] = min(attacker["combo"], 3)
    attacker["last_attack"] = now
    attacker["punch_time"] = 6

    dmg = int(base_damage(attacker))
    if defender["blocking"]:
        dmg = max(2, dmg // 3)

    defender["hp"] -= dmg
    defender["hit_effect"] = 6

def kick(attacker, defender):
    attacker["kick_time"] = 8
    dmg = int(12 * attacker["damage"])

    if defender["blocking"]:
        dmg //= 2

    defender["hp"] -= dmg
    defender["hit_effect"] = 8

def ultimate(attacker, defender):
    global screen_shake

    if attacker["combo"] < 3 or attacker["ultimate_cd"] > 0:
        return

    attacker["ultimate_cd"] = 300
    attacker["combo"] = 0
    screen_shake = 15

    dmg = int(35 * attacker["damage"])
    defender["hp"] -= dmg
    defender["hit_effect"] = 15

# ======================
# AI
# ======================
def enemy_ai():
    if game_over or level_clear:
        return

    if ENEMY["cooldown"] > 0:
        ENEMY["cooldown"] -= 1
        return

    if PLAYER["combo"] >= 2:
        ENEMY["blocking"] = True
    else:
        ENEMY["blocking"] = False

    roll = random.randint(0, 100)
    if roll < 60:
        attack(ENEMY, PLAYER)
    elif roll < 80:
        kick(ENEMY, PLAYER)

    ENEMY["cooldown"] = random.randint(20, 40)

# ======================
# LEVEL
# ======================
def setup_level():
    global ENEMY
    if level == 1:
        ENEMY = create_fighter(600, 100, 1.0, -1)
    elif level == 2:
        ENEMY = create_fighter(600, 140, 1.2, -1)
    elif level == 3:
        ENEMY = create_fighter(600, 280, 1.6, -1)

def next_level():
    global level, game_over
    level += 1
    PLAYER["hp"] = PLAYER["max_hp"]
    PLAYER["combo"] = 0
    if level > MAX_LEVEL:
        game_over = True
    else:
        setup_level()

def reset_game():
    global level, game_over
    level = 1
    game_over = False
    PLAYER.update(create_fighter(150, facing=1))
    setup_level()

setup_level()

# ======================
# MAIN LOOP
# ======================
while True:
    offset_x = random.randint(-screen_shake, screen_shake) if screen_shake > 0 else 0
    offset_y = random.randint(-screen_shake, screen_shake) if screen_shake > 0 else 0
    if screen_shake > 0:
        screen_shake -= 1

    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and not game_over:
                attack(PLAYER, ENEMY)
            if event.key == pygame.K_d and not game_over:
                kick(PLAYER, ENEMY)
            if event.key == pygame.K_SPACE and not game_over:
                ultimate(PLAYER, ENEMY)
            if event.key == pygame.K_s:
                PLAYER["blocking"] = True
            if event.key == pygame.K_r and game_over:
                reset_game()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                PLAYER["blocking"] = False

    if not game_over:
        enemy_ai()

        if ENEMY["hp"] <= 0:
            pygame.time.delay(500)
            next_level()

        if PLAYER["hp"] <= 0:
            game_over = True

    for f in (PLAYER, ENEMY):
        f["punch_time"] = max(0, f["punch_time"] - 1)
        f["kick_time"] = max(0, f["kick_time"] - 1)
        f["hit_effect"] = max(0, f["hit_effect"] - 1)
        f["ultimate_cd"] = max(0, f["ultimate_cd"] - 1)

    draw_fighter(PLAYER, BLUE)
    draw_fighter(ENEMY, PURPLE if level == 3 else RED)

    draw_hp_bar(40, 30, PLAYER["hp"], PLAYER["max_hp"])
    draw_hp_bar(520, 30, ENEMY["hp"], ENEMY["max_hp"])

    screen.blit(FONT.render(f"Level {level}", True, BLACK), (360, 10))
    screen.blit(FONT.render(f"Combo: {PLAYER['combo']}", True, BLACK), (40, 60))

    if game_over:
        msg = "YOU WIN!" if level > MAX_LEVEL else "GAME OVER"
        screen.blit(BIG_FONT.render(msg, True, BLACK), (WIDTH//2 - 120, HEIGHT//2 - 30))

    pygame.display.flip()
    clock.tick(60)



# 
# A	Pukul / Combo
#D	Tendang
#S	Block
#SPACE	Ultimate
#R	Restart