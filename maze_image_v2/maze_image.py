# venv\Scripts\activate.bat
# pip install pillow
# cd maze_image_v2
# python maze_image.py
"""
12 x 12
ピクセル数 256x256 
"""


import random
from PIL import Image
WIDTH = 21
HEIGHT = 21
WALL = '#'
PATH = ' '
WALLCOLOR = (85, 85, 85)
PATHCOLOR = (171, 171, 171)

# 迷路生成
def generate_maze( WIDTH , HEIGHT):
    # マップの初期化
    maze = [[WALL for _ in range(WIDTH)] for _ in range(HEIGHT)]
    walls = []
    start_x, start_y = 1, 1
    maze[start_y][start_x] = PATH
    def add_walls(x, y):
        if x >= 2 and maze[y][x-2] == WALL:
            walls.append((x-2, y, x-1, y))
        if x <= WIDTH-3 and maze[y][x+2] == WALL:
            walls.append((x+2, y, x+1, y))
        if y >= 2 and maze[y-2][x] == WALL:
            walls.append((x, y-2, x, y-1))
        if y <= HEIGHT-3 and maze[y+2][x] == WALL:
            walls.append((x, y+2, x, y+1))
    add_walls(start_x, start_y)
    while walls:
        idx = random.randint(0, len(walls)-1)
        x, y, between_x, between_y = walls.pop(idx)
        if maze[y][x] == WALL:
            maze[y][x] = PATH
            maze[between_y][between_x] = PATH
            add_walls(x, y)
    maze[1][0] = PATH
    maze[HEIGHT-2][WIDTH-1] = PATH
    return maze

# 画像を生成する
def create_image( maze, WIDTH, HEIGHT, CELL_SIZE):
    img_width = WIDTH * CELL_SIZE
    img_height = HEIGHT * CELL_SIZE
    img = Image.new("RGB", (img_width, img_height), WALLCOLOR)
    pixels = img.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            color = PATHCOLOR if maze[y][x] == PATH else WALLCOLOR
            for dy in range(CELL_SIZE):
                for dx in range(CELL_SIZE):
                    pixels[x * CELL_SIZE + dx, y * CELL_SIZE + dy] = color
    return img

# 画像を右に結合する関数
def imgjoin_right(img_data1, img_data2):
    if img_data1 == None:
        return img_data2
    w1, h1 = img_data1.size
    w2, h2 = img_data2.size
    new_width = w1 + w2
    new_height = max(h1, h2)
    new_img = Image.new("RGB", (new_width, new_height), WALLCOLOR)
    new_img.paste(img_data1, (0, 0))
    new_img.paste(img_data2, (w1, 0))
    return new_img

# 画像を下に結合する関数
def imgjoin_down(img_data1, img_data2):
    if img_data1 is None:
        return img_data2
    w1, h1 = img_data1.size
    w2, h2 = img_data2.size
    new_width = max(w1, w2)
    new_height = h1 + h2
    new_img = Image.new("RGB", (new_width, new_height), WALLCOLOR)
    new_img.paste(img_data1, (0, 0))
    new_img.paste(img_data2, (0, h1))
    return new_img

base_img = None
for cnt_x in range(0,12):
    face_img = None
    for cnt_face in range(0,12):
        maze = generate_maze( WIDTH, HEIGHT)
        img_data = create_image(maze, WIDTH, HEIGHT, CELL_SIZE = 1)
        face_img = imgjoin_right(face_img, img_data)
    base_img = imgjoin_down(base_img, face_img)


save_img = Image.new("RGB", (256, 256), (255, 255, 255))
save_img.paste(base_img, (0, 0))
save_img.save("maze_combined.png")
