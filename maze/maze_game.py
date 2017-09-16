import pygame
from pygame.locals import *
from random import shuffle

# 이 소스는, 아래 원 소스를 이용하여 재작성되었습니다.
# http://www.pygame.org/project-PyMaze-733-.html
#
# 위의 원 소스가 GPL 라이선스이기 때문에,
# 본 소스도 GLP 라이선스를 따릅니다.
# 따라서, 본 소스를 어떤 목적으로든, 어떤 형태로든 사용할 수 있습니다.
# 단, 본 소스를 사용하거나, 혹은 수정/변경하여 배포하는 경우,
# 동일한 라이선스인 GPL에 의해 무조건 소스를 공개해야 합니다.

size = (800, 600)
cols = 50
rows = 36

keep_going = 1
maze = {}

def get_coords(cell):
    # grabs coords of a given cell
    coords = (-1, -1)
    for k in maze:
        if maze[k] is cell:
            coords = (k[0], k[1])
            break
    return coords

def get_neighbors(cell):
    # obvious
    neighbors = []

    (x, y) = get_coords(cell)
    if (x, y) == (-1, -1):
        return neighbors

    north = (x, y - 1)
    south = (x, y + 1)
    east = (x + 1, y)
    west = (x - 1, y)

    if north in maze:
        neighbors.append(maze[north])
    if south in maze:
        neighbors.append(maze[south])
    if east in maze:
        neighbors.append(maze[east])
    if west in maze:
        neighbors.append(maze[west])

    return neighbors

def knock_wall(cell, neighbor):
    # knocks down wall between cell and neighbor.
    xc, yc = get_coords(cell)
    xn, yn = get_coords(neighbor)

    # Which neighbor?
    if xc == xn and yc == yn + 1:
        # neighbor's above, knock out south wall of neighbor
        neighbor['south'] = 0
    elif xc == xn and yc == yn - 1:
        # neighbor's below, knock out south wall of cell
        cell['south'] = 0
    elif xc == xn + 1 and yc == yn:
        # neighbor's left, knock out east wall of neighbor
        neighbor['east'] = 0
    elif xc == xn - 1 and yc == yn:
        # neighbor's right, knock down east wall of cell
        cell['east'] = 0

def check_finished():
    # Checks if we're done generating
    done = 1
    for k in maze:
        if maze[k]['visited'] == 0:
            done = 0
            break
    if done:
        keep_going = 0

def maze_generate(start_cell=None, stack=[]):
    """Generates a random maze using a magical simple recursive function."""

    if start_cell is None:
        start_cell = maze[(cols - 1, rows - 1)]

    if not keep_going:
        return

    check_finished()
    neighbors = []

    # if the stack is empty, add the start cell
    if len(stack) == 0:
        stack.append(start_cell)

    # set current cell to last cell
    curr_cell = stack[-1]

    # get neighbors and shuffle 'em up a bit
    neighbors = get_neighbors(curr_cell)
    shuffle(neighbors)

    for neighbor in neighbors:
        if neighbor['visited'] == 0:
            neighbor['visited'] = 1
            stack.append(neighbor)
            knock_wall(curr_cell, neighbor)

            maze_generate(start_cell, stack)

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("미로 게임")

font = pygame.font.SysFont("malgungothic",64)
text = font.render("미로를 만들고 있습니다", 1, (255, 255, 255))
rect = text.get_rect()
rect.center = size[0] / 2, size[1] / 2
screen.blit(text, rect)
pygame.display.update(rect)

for y in range(rows):
    for x in range(cols):
        cell = {'south': 1, 'east': 1, 'visited': 0}
        maze[(x, y)] = cell

maze_generate(maze[(0, 0)])

#draw_maze()
screen.fill((255, 255, 255))
cell_width = size[0] / cols
cell_height = size[1] / rows

for y in range(rows):
    for x in range(cols):
        if maze[(x, y)]['south']:  # draw south wall
            pygame.draw.line(screen, (0, 0, 0), \
                             (x * cell_width, y * cell_height + cell_height), \
                             (x * cell_width + cell_width, \
                              y * cell_height + cell_height))
        if maze[(x, y)]['east']:  # draw east wall
            pygame.draw.line(screen, (0, 0, 0), \
                             (x * cell_width + cell_width, y * cell_height), \
                             (x * cell_width + cell_width, y * cell_height + \
                              cell_height))
# Screen border
pygame.draw.rect(screen, (0, 0, 0), (0, 0, size[0], size[1]), 1)
pygame.display.update()

#reset_player()
w, h = cell_width - 3, cell_height - 3
rect = 0, 0, w, h
base = pygame.Surface((w, h))
base.fill((255, 255, 255))
red_p = base.copy()
green_p = base.copy()
blue_p = base.copy()
goldy = base.copy()
r = (255, 0, 0)
g = (0, 255, 0)
b = (0, 0, 255)
gold = (0xc5, 0x93, 0x48)
pygame.draw.ellipse(red_p, r, rect)
pygame.draw.ellipse(green_p, g, rect)
pygame.draw.ellipse(blue_p, b, rect)
pygame.draw.ellipse(goldy, gold, rect)

# Make a same-size matrix for the player.
player_maze = {}
for y in range(rows):
    for x in range(cols):
        cell = {'visited': 0}  # if 1, draws green. if >= 2, draws red.
        player_maze[(x, y)] = cell
        screen.blit(base, (x * cell_width + 2, y * cell_height + 2))

screen.blit(goldy, (x * cell_width + 2, y * cell_height + 2))
cx = cy = 0
curr_cell = player_maze[(cx, cy)]  # starts at origin
last_move = None  # For last move fun

#loop()
clock = pygame.time.Clock()
keep_going = 1
is_find = 0

while keep_going:
    moved = 0
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            keep_going = 0
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                keep_going = 0
            if event.key == K_r:
                print('reset_player()')
                #reset_player()
            if event.key == K_DOWN:
                no_move = 0
                if not maze[(cx, cy)]['south']:
                    cy += 1
                    curr_cell['visited'] += 1
                else:
                    no_move = 1
                if last_move == 'u' and not no_move:
                    curr_cell['visited'] += 1
                if not no_move:
                    last_move = dir
                    curr_cell = player_maze[(cx, cy)]
                moved = 1
            if event.key == K_UP:
                no_move = 0
                if not maze[(cx, cy - 1)]['south']:
                    cy -= 1
                    curr_cell['visited'] += 1
                else:
                    no_move = 1
                if last_move == 'd' and not no_move:
                    curr_cell['visited'] += 1
                if not no_move:
                    last_move = dir
                    curr_cell = player_maze[(cx, cy)]
                moved = 1
            if event.key == K_LEFT:
                no_move = 0
                if not maze[(cx - 1, cy)]['east']:
                    cx -= 1
                    curr_cell['visited'] += 1
                else:
                    no_move = 1
                if last_move == 'r' and not no_move:
                    curr_cell['visited'] += 1
                if not no_move:
                    last_move = dir
                    curr_cell = player_maze[(cx, cy)]
                moved = 1
            if event.key == K_RIGHT:
                no_move = 0
                if not maze[(cx, cy)]['east']:
                    cx += 1
                    curr_cell['visited'] += 1
                else:
                    no_move = 1
                if dir == 'r' and not no_move:
                    curr_cell['visited'] += 1
                if not no_move:
                    last_move = dir
                    curr_cell = player_maze[(cx, cy)]
                moved = 1

            if cx + 1 == cols and cy + 1 == rows:
                print('Congratumalations, you beat this maze.')
                is_find = 1
                keep_going = 0

    #draw_player()
    for y in range(rows):
        for x in range(cols):
            if player_maze[(x, y)]['visited'] > 0:
                if player_maze[(x, y)]['visited'] == 1:
                    circ = green_p
                else:
                    circ = red_p
                # draw green circles
                screen.blit(circ, (x * cell_width + 2, y * cell_height + 2))
    screen.blit(blue_p, (cx * cell_width + 2, cy * cell_height + 2))
    pygame.display.update()

if is_find == 1:
    text = font.render("길찾기 성공", 2, (0, 0, 0))
else:
    text = font.render("길찾기 실패", 2, (0, 0, 0))

rect = text.get_rect()
rect.center = size[0] / 2, size[1] / 2
screen.blit(text, rect)
pygame.display.update(rect)

keep_going = 1
while keep_going:
    for event in pygame.event.get():
        if event.type == QUIT:
            keep_going = 0
