# venv\Scripts\activate.bat
# cd crystal
# python maze_crystal_image.py
"""
ピクセル数 256x256 
"""


import random
from PIL import Image

# 迷路生成
def generate_maze( WIDTH , HEIGHT , WALL , PATH ):
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
def create_image( maze, WIDTH, HEIGHT, CELL_SIZE,PATH, PATHCOLOR, WALLCOLOR):
    img_width = WIDTH * CELL_SIZE
    img_height = HEIGHT * CELL_SIZE
    img = Image.new("RGBA", (img_width, img_height), WALLCOLOR)
    pixels = img.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            color = PATHCOLOR if maze[y][x] == PATH else WALLCOLOR
            for dy in range(CELL_SIZE):
                for dx in range(CELL_SIZE):
                    pixels[x * CELL_SIZE + dx, y * CELL_SIZE + dy] = color
    return img

WIDTH = 256
HEIGHT = 256
WALL = '#'
PATH = ' '
WALLCOLOR = (0, 255, 255, 77)  # 水色30%透過
PATHCOLOR = (0, 255, 255, 255)  # 水色（不透明）

save_img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))

for cnt_face in range(0,6):
    XYSize = 21
    maze = generate_maze( XYSize, XYSize,WALL , PATH)
    img_data = create_image(maze, XYSize, XYSize, 1,PATH, (171, 171, 171,255), (85, 85, 85,255))
    save_img.paste(img_data, (cnt_face * 21, 0), img_data)  # 透過画像として貼り付け

maze = generate_maze( WIDTH, HEIGHT,WALL , PATH)
img_data = create_image(maze, WIDTH, HEIGHT, 1, PATH, PATHCOLOR, WALLCOLOR)
save_img.paste(img_data, (0, 21), img_data)  # 透過画像として貼り付け

save_img.save("maze_crystal_image.png")
