import pygame
import sys

# ================== INIT ==================
pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Gweeeh")

clock = pygame.time.Clock()

# ================== COLOR ==================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ================== FONT ==================
score_font = pygame.font.SysFont(None, 50)
win_font = pygame.font.SysFont(None, 70)

# ================== SCORE ==================
left_score = 0
right_score = 0
WIN_SCORE = 10
game_over = False
winner_text = ""

# ================== PADDLE ==================
paddle_width, paddle_height = 10, 80
left_paddle = pygame.Rect(30, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)
right_paddle = pygame.Rect(WIDTH - 40, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)
paddle_speed = 6

# ================== BALL ==================
ball_size = 12
ball = pygame.Rect(WIDTH//2 - ball_size//2, HEIGHT//2 - ball_size//2, ball_size, ball_size)
ball_speed_x = 5
ball_speed_y = 5

# ================== GAME LOOP ==================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Restart game (optional tapi berguna 😏)
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                left_score = 0
                right_score = 0
                game_over = False
                winner_text = ""
                ball.center = (WIDTH//2, HEIGHT//2)
                ball_speed_x = 5
                ball_speed_y = 5

    keys = pygame.key.get_pressed()

    # ================== CONTROL ==================
    if not game_over:
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed

        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += paddle_speed

        # ================== BALL MOVE ==================
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Bounce top & bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Bounce paddle
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x *= -1

        # ================== SCORE CHECK ==================
        if ball.left <= 0:
            right_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_speed_x *= -1

        if ball.right >= WIDTH:
            left_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_speed_x *= -1

        # ================== WIN CHECK ==================
        if left_score == WIN_SCORE:
            game_over = True
            winner_text = "LEFT PLAYER WINS!"

        if right_score == WIN_SCORE:
            game_over = True
            winner_text = "RIGHT PLAYER WINS!"

    # ================== DRAW ==================
    screen.fill(BLACK)

    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # Draw score
    left_text = score_font.render(str(left_score), True, WHITE)
    right_text = score_font.render(str(right_score), True, WHITE)
    screen.blit(left_text, (WIDTH//2 - 60, 20))
    screen.blit(right_text, (WIDTH//2 + 30, 20))

    # Draw winner
    if game_over:
        win_surface = win_font.render(winner_text, True, WHITE)
        screen.blit(
            win_surface,
            (WIDTH//2 - win_surface.get_width()//2,
             HEIGHT//2 - win_surface.get_height()//2)
        )

        restart_text = score_font.render("Press R to Restart", True, WHITE)
        screen.blit(
            restart_text,
            (WIDTH//2 - restart_text.get_width()//2,
             HEIGHT//2 + 50)
        )

    pygame.display.flip()
    clock.tick(60)
