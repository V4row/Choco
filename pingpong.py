import pygame
import sys

# Inisialisasi
pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Gweeeh")

clock = pygame.time.Clock()

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle
paddle_width, paddle_height = 10, 80
left_paddle = pygame.Rect(30, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)
right_paddle = pygame.Rect(WIDTH - 40, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)

paddle_speed = 6

# Bola
ball_size = 12
ball = pygame.Rect(WIDTH//2, HEIGHT//2, ball_size, ball_size)
ball_speed_x = 5
ball_speed_y = 5

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Kontrol paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= paddle_speed
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += paddle_speed

    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += paddle_speed

    # Gerak bola
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Pantul atas & bawah
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Pantul paddle
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1

    # Reset bola kalau keluar
    if ball.left <= 0 or ball.right >= WIDTH:
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1

    # Gambar
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    pygame.display.flip()
    clock.tick(60)
