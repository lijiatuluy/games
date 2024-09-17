import pygame
import random


# 游戏窗口大小
WIDTH = 800
HEIGHT = 800
# 图块大小
TILE_SIZE = 80
BLOCK_SIZE = TILE_SIZE
# 块的数量
NUM_BLOCKS = 11
# 帧率
FPS = 30
# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)
TEXT_COLOR = (0, 0, 0)
# 块间距
BLOCK_SPACING = 30
# 槽位最大数量
MAX_SLOTS = 7


def load_image(image_path):
    try:
        image = pygame.image.load(image_path)
        return image
    except pygame.error as e:
        print(f"Failed to load image {image_path}: {e}")


def scale_image(image, size):
    return pygame.transform.scale(image, size)


# 初始化Pygame
pygame.init()


def generate_blocks(patterns):
    blocks = []
    all_patterns = []
    for i in range(11):
        pattern = random.choice(patterns)
        all_patterns.extend([pattern] * 3)
    random.shuffle(all_patterns)
    for i in range(0, len(all_patterns), 3):
        block_patterns = all_patterns[i:i + 3]
        block = (block_patterns, 3)
        blocks.append(block)
    return blocks


# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("泥了个塑")

# 加载图案图片
patterns = [scale_image(load_image(f"assets/pattern_{i}.png"), (TILE_SIZE, TILE_SIZE)) for i in range(1, 4)]

# 加载背景图片并调整大小
menu_background = scale_image(load_image("assets/menu_background.png"), (WIDTH, HEIGHT))
board_background = scale_image(load_image("assets/board_background.png"), (WIDTH, HEIGHT))
result_background = scale_image(load_image("assets/result_background.png"), (WIDTH, HEIGHT))


blocks = generate_blocks(patterns)
slots = []
game_active = False
time_left = 90 * 1000  # 默认难度为简单
start_time = None
game_result = None
difficulty = None  # 记录当前难度

# 道具相关
add_time_item = None
item_used = False


def draw_button(text, x, y, width, height, active):
    font = pygame.font.SysFont("SimSun", 40)
    color = BUTTON_HOVER_COLOR if active else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)


def draw_menu():
    screen.blit(menu_background, (0, 0))
    start_button = pygame.Rect(300, 300, 200, 50)
    quit_button = pygame.Rect(300, 400, 200, 50)
    mouse_pos = pygame.mouse.get_pos()
    draw_button("开始游戏", start_button.x, start_button.y, start_button.width, start_button.height,
                start_button.collidepoint(mouse_pos))
    draw_button("退出游戏", quit_button.x, quit_button.y, quit_button.width, quit_button.height,
                quit_button.collidepoint(mouse_pos))
    return start_button, quit_button


def draw_difficulty_selection():
    screen.blit(menu_background, (0, 0))
    easy_button = pygame.Rect(300, 300, 200, 50)
    hard_button = pygame.Rect(300, 400, 200, 50)
    mouse_pos = pygame.mouse.get_pos()
    draw_button("简单", easy_button.x, easy_button.y, easy_button.width, easy_button.height,
                easy_button.collidepoint(mouse_pos))
    draw_button("困难", hard_button.x, hard_button.y, hard_button.width, hard_button.height,
                hard_button.collidepoint(mouse_pos))
    return easy_button, hard_button


def draw_board():
    screen.blit(board_background, (0, 0))
    block_width = BLOCK_SIZE + BLOCK_SPACING
    num_cols = 4
    num_rows = (NUM_BLOCKS // num_cols)+(1 if NUM_BLOCKS % num_cols else 0)
    start_x = (WIDTH - (block_width * num_cols))//2
    start_y = (HEIGHT - (block_width * num_rows))//2

    # 绘制增加时间道具按钮
    global add_time_item
    if add_time_item is None:
        # 计算图片块区域的中心x坐标
        center_x = (WIDTH - (block_width * num_cols))//2+(block_width * num_cols)//2
        add_time_item = pygame.Rect(center_x - 50, start_y - 60, 100, 50)
    font = pygame.font.SysFont("SimSun", 30)
    item_text = font.render("+10s", True, RED)
    item_rect = item_text.get_rect(center=(add_time_item.x+add_time_item.width//2, add_time_item.y+add_time_item.height//2))
    # 修改按钮颜色为黄色
    pygame.draw.rect(screen, (255, 255, 0), add_time_item)
    screen.blit(item_text, item_rect)

    for i, (tiles, layers) in enumerate(blocks):
        row = i//num_cols
        col = i % num_cols
        base_x = start_x + col * block_width
        base_y = start_y + row * block_width
        for layer in range(layers):
            offset_x = layer*(BLOCK_SPACING//2)
            offset_y = layer*(BLOCK_SPACING//2)
            screen.blit(tiles[layer], (base_x + offset_x, base_y + offset_y))



def draw_slots():
    slot_x = 50
    slot_y = HEIGHT - TILE_SIZE - 50
    slot_width = TILE_SIZE + 10
    slot_height = TILE_SIZE
    pygame.draw.rect(screen, BLACK, (slot_x - 10, slot_y - 10, MAX_SLOTS * slot_width + 20, slot_height + 20))
    for i in range(MAX_SLOTS):
        pygame.draw.rect(screen, WHITE, (slot_x + i * slot_width, slot_y, slot_width, slot_height))
        pygame.draw.rect(screen, BLACK, (slot_x + i * slot_width, slot_y, slot_width, slot_height), 2)
    for i, tile in enumerate(slots):
        if i < MAX_SLOTS:
            screen.blit(tile, (slot_x + i * slot_width + 5, slot_y + 5))


def check_slots():
    if len(slots) >= 3:
        for i in range(len(slots) - 2):
            if slots[i] is not None and slots[i] == slots[i + 1] == slots[i + 2]:
                return True
    return False


def remove_matching():
    global slots
    new_slots = []
    i = 0
    while i < len(slots):
        if i <= len(slots) - 3 and slots[i] == slots[i + 1] == slots[i + 2]:
            i += 3
        else:
            new_slots.append(slots[i])
            i += 1
    slots = new_slots


def draw_timer(time_left):
    font = pygame.font.SysFont("SimSun", 60)
    minutes = time_left // 60000
    seconds = (time_left % 60000) // 1000
    time_text = f"{minutes:02}:{seconds:02}"
    timer_surf = font.render(time_text, True, RED)
    screen.blit(timer_surf, (WIDTH - 250, 60))


def draw_victory_screen():
    screen.blit(result_background, (0, 0))
    font = pygame.font.SysFont("SimSun", 80)
    victory_text = font.render("WIN", True, RED)
    text_rect = victory_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(victory_text, text_rect)
    restart_button = pygame.Rect(300, 500, 200, 50)
    quit_button = pygame.Rect(300, 600, 200, 50)
    mouse_pos = pygame.mouse.get_pos()
    draw_button("重新开始", restart_button.x, restart_button.y, restart_button.width, restart_button.height,
                restart_button.collidepoint(mouse_pos))
    draw_button("退出游戏", quit_button.x, quit_button.y, quit_button.width, quit_button.height,
                quit_button.collidepoint(mouse_pos))
    return restart_button, quit_button


def draw_defeat_screen():
    screen.blit(result_background, (0, 0))
    font = pygame.font.SysFont("SimSun", 80)
    defeat_text = font.render("LOSE", True, RED)
    text_rect = defeat_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(defeat_text, text_rect)
    restart_button = pygame.Rect(300, 500, 200, 50)
    quit_button = pygame.Rect(300, 600, 200, 50)
    mouse_pos = pygame.mouse.get_pos()
    draw_button("重新开始", restart_button.x, restart_button.y, restart_button.width, restart_button.height,
                restart_button.collidepoint(mouse_pos))
    draw_button("退出游戏", quit_button.x, quit_button.y, quit_button.width, quit_button.height,
                quit_button.collidepoint(mouse_pos))
    return restart_button, quit_button


# 主游戏循环
running = True
clock = pygame.time.Clock()
previous_time = pygame.time.get_ticks()

while running:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_active:
                if difficulty is None:
                    start_button, quit_button = draw_menu()
                    if start_button.collidepoint(mouse_pos):
                        difficulty = "select"
                    elif quit_button.collidepoint(mouse_pos):
                        running = False
                elif difficulty == "select":
                    easy_button, hard_button = draw_difficulty_selection()
                    if easy_button.collidepoint(mouse_pos):
                        difficulty = "easy"
                        time_left = 90 * 1000
                        game_active = True
                        start_time = pygame.time.get_ticks()
                    elif hard_button.collidepoint(mouse_pos):
                        difficulty = "hard"
                        time_left = 20 * 1000
                        game_active = True
                        start_time = pygame.time.get_ticks()
            else:
                if game_result is None:
                    x, y = event.pos
                    block_width = BLOCK_SIZE + BLOCK_SPACING
                    num_cols = 4
                    block_index = ((x - (WIDTH - (block_width * num_cols)) // 2) // block_width) + ((y - (HEIGHT - (
                                block_width * ((NUM_BLOCKS // num_cols) + (1 if NUM_BLOCKS % num_cols else 0)))) // 2) // block_width) * num_cols

                    if block_index >= 0 and block_index < NUM_BLOCKS:
                        if len(slots) < MAX_SLOTS:
                            tiles, _ = blocks[block_index]
                            if tiles:
                                slots.append(tiles[-1])
                                if len(tiles) > 1:
                                    blocks[block_index] = (tiles[:-1], len(tiles) - 1)
                                else:
                                    blocks[block_index] = ([], 0)
                                if check_slots():
                                    remove_matching()
                                if len(slots) >= MAX_SLOTS:
                                    game_result = "LOSE"
                                    game_active = False
                                elif all(layers == 0 for _, layers in blocks):
                                    game_result = "WIN"
                                    game_active = False
                # 处理道具按钮点击
                if add_time_item is not None and add_time_item.collidepoint(mouse_pos) and not item_used:
                    time_left += 10 * 1000
                    item_used = True

    if game_active:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - previous_time
        time_left = max(0, time_left - elapsed_time)
        previous_time = current_time
        if time_left <= 0:
            game_result = "LOSE"
            game_active = False

        screen.fill(WHITE)
        draw_board()
        draw_slots()
        draw_timer(time_left)

    else:
        if game_result == "WIN":
            restart_button, quit_button = draw_victory_screen()
            if pygame.mouse.get_pressed()[0]:
                if restart_button.collidepoint(mouse_pos):
                    blocks = generate_blocks(patterns)
                    slots = []
                    game_active = False
                    time_left = 90 * 1000
                    start_time = None
                    game_result = None
                    difficulty = None
                    add_time_item = None
                    item_used = False
                elif quit_button.collidepoint(mouse_pos):
                    running = False
        elif game_result == "LOSE":
            restart_button, quit_button = draw_defeat_screen()
            if pygame.mouse.get_pressed()[0]:
                if restart_button.collidepoint(mouse_pos):
                    blocks = generate_blocks(patterns)
                    slots = []
                    game_active = False
                    time_left = 90 * 1000
                    start_time = None
                    game_result = None
                    difficulty = None
                    add_time_item = None
                    item_used = False
                elif quit_button.collidepoint(mouse_pos):
                    running = False
        else:
            if difficulty == "select":
                draw_difficulty_selection()
            else:
                draw_menu()

    pygame.display.update()

pygame.quit()
