import pygame
import sys

# 初期設定
pygame.init()

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# ブロックの色を各行ごとに設定
BLOCK_COLORS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]

# 画面サイズの設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('ブロック崩し')

# フォントの設定
font = pygame.font.SysFont("MS Gothic", 74)
small_font = pygame.font.SysFont("MS Gothic", 36)

# FPSの設定
clock = pygame.time.Clock()
FPS = 60

# ブロック、パドル、ボールの設定
BLOCK_ROWS = 6
BLOCK_COLS = 10
BLOCK_WIDTH = (SCREEN_WIDTH - 2 * (BLOCK_COLS - 1)) // BLOCK_COLS  # 隙間を考慮
BLOCK_HEIGHT = 30
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_SIZE = 10

# ゲームの状態
lives = 3
game_over = False
game_clear = False

# タイトル画面
def show_title_screen():
    screen.fill(BLACK)
    title_text = font.render('ブロック崩し', True, WHITE)
    start_text = small_font.render('スタート', True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//3))
    start_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50)
    pygame.draw.rect(screen, BLUE, start_button)
    screen.blit(start_text, (start_button.x + start_button.width//2 - start_text.get_width()//2, start_button.y + 10))
    pygame.display.flip()
    return start_button

# ゲームオーバー画面
def show_game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render('ゲームオーバー', True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//3))
    pygame.display.flip()
    pygame.time.wait(2000)

# クリア画面
def show_game_clear_screen():
    screen.fill(BLACK)
    game_clear_text = font.render('クリア！', True, BLUE)
    back_text = small_font.render('タイトルに戻る', True, WHITE)
    screen.blit(game_clear_text, (SCREEN_WIDTH//2 - game_clear_text.get_width()//2, SCREEN_HEIGHT//3))
    back_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50)
    pygame.draw.rect(screen, BLUE, back_button)
    screen.blit(back_text, (back_button.x + back_button.width//2 - back_text.get_width()//2, back_button.y + 10))
    pygame.display.flip()
    return back_button

# ゲームの初期化
def reset_game():
    global blocks, paddle, ball, ball_speed_x, ball_speed_y, lives, game_over, game_clear
    blocks = []
    for row in range(BLOCK_ROWS):
        for col in range(BLOCK_COLS):
            block = pygame.Rect(col * (BLOCK_WIDTH + 2), row * (BLOCK_HEIGHT + 2), BLOCK_WIDTH, BLOCK_HEIGHT)
            blocks.append((block, BLOCK_COLORS[row]))
    paddle = pygame.Rect(SCREEN_WIDTH//2 - PADDLE_WIDTH//2, SCREEN_HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH//2 - BALL_SIZE//2, SCREEN_HEIGHT//2, BALL_SIZE, BALL_SIZE)
    ball_speed_x = 5
    ball_speed_y = -5
    lives = 3
    game_over = False
    game_clear = False

# メインループ
def main():
    global lives, game_over, game_clear, ball, ball_speed_x, ball_speed_y

    show_title = True
    in_game = False

    reset_game()

    while True:
        screen.fill(BLACK)

        if show_title:
            start_button = show_title_screen()

        elif game_over:
            show_game_over_screen()
            reset_game()
            show_title = True

        elif game_clear:
            back_button = show_game_clear_screen()

        else:
            # パドルの操作
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle.left > 0:
                paddle.move_ip(-10, 0)
            if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
                paddle.move_ip(10, 0)

            # ボールの移動
            ball.move_ip(ball_speed_x, ball_speed_y)

            # 壁との衝突判定
            if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
                ball_speed_x = -ball_speed_x
            if ball.top <= 0:
                ball_speed_y = -ball_speed_y
            if ball.bottom >= SCREEN_HEIGHT:
                lives -= 1
                if lives == 0:
                    game_over = True
                else:
                    ball = pygame.Rect(SCREEN_WIDTH//2 - BALL_SIZE//2, SCREEN_HEIGHT//2, BALL_SIZE, BALL_SIZE)
                    ball_speed_y = -5

            # パドルとの衝突判定
            if ball.colliderect(paddle):
                ball_speed_y = -ball_speed_y

            # ブロックとの衝突判定
            hit_index = ball.collidelist([block[0] for block in blocks])
            if hit_index != -1:
                hit_block = blocks.pop(hit_index)
                ball_speed_y = -ball_speed_y

            # クリア判定
            if not blocks:
                game_clear = True

            # 描画
            pygame.draw.rect(screen, WHITE, paddle)
            pygame.draw.ellipse(screen, WHITE, ball)
            for block, color in blocks:
                pygame.draw.rect(screen, color, block)

            # 残機表示
            lives_text = small_font.render(f'残機: {lives}', True, WHITE)
            screen.blit(lives_text, (10, 10))

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and show_title:
                if start_button.collidepoint(event.pos):
                    show_title = False
                    in_game = True
            elif event.type == pygame.MOUSEBUTTONDOWN and game_clear:
                if back_button.collidepoint(event.pos):
                    game_clear = False
                    show_title = True
                    reset_game()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
