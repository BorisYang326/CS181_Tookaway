import simplegui
import math
import random

WIDTH = 350
HEIGHT = 600
BALL_RADIUS = 3
BALL_VEL = 10
CORNER_DIR = [ [1, 1], [1, -1], [-1, -1], [-1, 1] ]
TOP_HEIGHT = 45
BOTTOM_HEIGHT = 505
TILE_RADIUS = 20
time = 0
started = False
ball_number = 1
level = 0
tile_set = set()
ball_set = set()
position = []
angle = math.pi * 1.5
del_angle = 0
balls_to_shoot = 0
arrow_len = 25
del_arrow_len = 0
ready_next = False
next_pos0 = 0
first_die = False

colliding = 0 # tbd


def angle_to_dir(ang):
    return [math.cos(ang), math.sin(ang)]

class Ball:
    def __init__(self, pos, dir):
        self.pos = list(pos)
        self.dir = list(dir)
        
    def draw(self, canvas):
        canvas.draw_circle(self.pos, BALL_RADIUS, 1, 'White', 'White')
        
    def update(self):
        new_pos = [self.pos[0] + self.dir[0] * BALL_VEL, 
                   self.pos[1] + self.dir[1] * BALL_VEL]
        if new_pos[0] >= WIDTH or new_pos[0] <= 0:
            self.dir[0] = -self.dir[0]
        if new_pos[1] >= HEIGHT or new_pos[1] <= TOP_HEIGHT:
            self.dir[1] = -self.dir[1]
        new_pos = [self.pos[0] + self.dir[0] * BALL_VEL, 
                   self.pos[1] + self.dir[1] * BALL_VEL]
        self.pos = new_pos
        
    def die(self):
        global first_die, next_pos0
        
        if self.pos[1] > BOTTOM_HEIGHT:
            if first_die:
                first_die = False
                next_pos0 = self.pos[0]
            return True
        else:
            return False
    
    def collide(self, tile):
        global colliding
        
        tile_pos = tile.get_pos()
        del_x = abs(self.pos[0] - tile_pos[0])
        del_y = abs(self.pos[1] - tile_pos[1])
        x_in = del_x <= TILE_RADIUS + 5
        y_in = del_y <= TILE_RADIUS + 5
        if x_in and y_in:
            if del_x >= del_y:
                colliding += 1
                self.dir[0] = -self.dir[0]
            if del_x <= del_y:
                colliding -= 1
                self.dir[1] = -self.dir[1]
            return True
        else:
            return False

tb = Ball([WIDTH / 2, HEIGHT / 5], [0, 0])

class Tile:
    def __init__(self, pos, start_level):
        self.pos = list(pos)
        self.life = start_level
        self.start_level = start_level
        
    def get_pos(self):
        global level

        self.pos[1] = level - self.start_level + 1
        return [25 + self.pos[0] * 50, 25 + self.pos[1] * 50]
    
    def draw(self, canvas):        
        center_pos = self.get_pos()
        point_list = []
        for i in range(4):
            point_list.append([center_pos[0] + CORNER_DIR[i][0] * TILE_RADIUS, 
                               center_pos[1] + CORNER_DIR[i][1] * TILE_RADIUS])
        canvas.draw_polygon(point_list, 3, 'Red')
        
        text_pos = [center_pos[0] - 5, center_pos[1] + 6]
        if self.life >= 10:
            text_pos[0] -= 6
            if self.life >= 100:
                text_pos[0] -= 6
        canvas.draw_text(str(self.life), text_pos, 20, 'Red')
    
    def update(self):
        global started
        
        self.get_pos()
        if self.pos[1] >= 9:
            started = False
    
    def die(self):
        return self.life <= 0
    
    def got_hit(self):
        self.life -= 1

def decide():
    return random.randrange(10) < 5

def next_level():
    global level
    
    level += 1
    
    for i in range(7):
        if decide():
            tile_set.add( Tile([i, 0], level) )
    
        
def process_group(group, canvas):
    for item in set(group):
        item.draw(canvas)
        item.update()
        if item.die():
            group.remove(item)
        
def draw_arrow(canvas):
    global angle, position, arrow_len, del_arrow_len
    
    dir = angle_to_dir(angle)
    new_arrow_len = arrow_len + del_arrow_len
    if 25 <= new_arrow_len <= BOTTOM_HEIGHT - TOP_HEIGHT:
        arrow_len = new_arrow_len
    tip_pos = [position[0] + dir[0] * arrow_len, position[1] + dir[1] * arrow_len]
    dir_left, dir_right = angle_to_dir(angle - math.pi * 0.75), angle_to_dir(angle + math.pi * 0.75)
    lr_len = 7
    left_pos =  [tip_pos[0] +  dir_left[0] * lr_len, tip_pos[1] +  dir_left[1] * lr_len]
    right_pos = [tip_pos[0] + dir_right[0] * lr_len, tip_pos[1] + dir_right[1] * lr_len]
    
    canvas.draw_line(position, tip_pos, 2, 'White')
    canvas.draw_line(tip_pos, left_pos, 2, 'White')
    canvas.draw_line(tip_pos, right_pos, 2, 'White')
    
def ball_hit_group(ball, group):
    for item in set(group):
        if ball.collide(item):
            item.got_hit()
            if item.die():
                group.remove(item)
    
    
def draw(canvas):
    global started, time, tile_set, ball_set, angle, del_angle, level, colliding
    
    if not started:
        canvas.draw_text('BB-TAN', [50, 300], 70, 'Yellow')
        canvas.draw_line([40, 230], [310, 230], 4, 'Yellow')
        canvas.draw_line([40, 320], [310, 320], 4, 'Yellow')
        if time % 500 <= 250:
            canvas.draw_text('Press SPACE to play', [90, 500], 20, 'White')
    else:
        # updates
        process_group(tile_set, canvas)
        process_group(ball_set, canvas)
        if math.pi * 1.1 < angle + del_angle < math.pi * 1.9:
            angle = (angle + del_angle) % (math.pi * 2)
        
        # top and bottom lines
        canvas.draw_line([0,    TOP_HEIGHT], [WIDTH,    TOP_HEIGHT], 3, 'White')
        canvas.draw_line([0, BOTTOM_HEIGHT], [WIDTH, BOTTOM_HEIGHT], 3, 'White')
        
        # arrow
        draw_arrow(canvas)
        
        # texts
        canvas.draw_text("Level " + str(level), [WIDTH / 2 - 35, TOP_HEIGHT - 15], 20, 'White')
        canvas.draw_text(str(ball_number) + ' balls', [WIDTH / 2 - 35, BOTTOM_HEIGHT + 35], 20, 'White')
        #canvas.draw_text(str(colliding) , [WIDTH / 2 + 70, BOTTOM_HEIGHT + 35], 20, 'White')
        
        # hit
        for ball in ball_set:
            ball_hit_group(ball, tile_set)
            
        # test, to be deleted
        global tb
        #tb.draw(canvas)
        for tile in tile_set:
            if tb.collide(tile):
                pass
                #colliding += 1

def new_game():
    global started, ball_number, level, tile_set, ball_set, position, angle, del_angle, balls_to_shoot
    
    started = True
    ball_number = 1
    level = 0
    tile_set = set()
    ball_set = set()
    position = [WIDTH / 2, BOTTOM_HEIGHT]
    angle = math.pi * 1.5
    del_angle = 0
    balls_to_shoot = 0
    ready_next = False
    
    next_level()
    
def shoot():
    global ball_number, balls_to_shoot, first_die
    
    ball_number += 1 # deleted later
    first_die = True
    balls_to_shoot = ball_number
    
def keydown(key):
    global started, del_angle, del_arrow_len
    
    global tb # tbd

    # shooting, cannot move
    if len(ball_set) > 0:
        return
    
    if key == simplegui.KEY_MAP['space']:
        if not started:
            new_game()
        else:
            shoot()
    elif key == simplegui.KEY_MAP['left']:
        del_angle = -0.02
    elif key == simplegui.KEY_MAP['right']:
        del_angle = 0.02
    elif key == simplegui.KEY_MAP['up']:
        del_arrow_len = 5
    elif key == simplegui.KEY_MAP['down']:
        del_arrow_len = -5
    elif key == simplegui.KEY_MAP['z']:
        next_level()
    elif key == simplegui.KEY_MAP['x']:
        for i in range(10):
            next_level()
            
    # test, tbd
    elif key == simplegui.KEY_MAP['w']:
        tb.pos[1] -= 1
    elif key == simplegui.KEY_MAP['s']:
        tb.pos[1] += 1
    elif key == simplegui.KEY_MAP['a']:
        tb.pos[0] -= 1
    elif key == simplegui.KEY_MAP['d']:
        tb.pos[0] += 1
    
    
def keyup(key):
    global del_angle, del_arrow_len
    
    if key == simplegui.KEY_MAP['left']:
        del_angle = 0
    elif key == simplegui.KEY_MAP['right']:
        del_angle = 0
    elif key == simplegui.KEY_MAP['up']:
        del_arrow_len = 0
    elif key == simplegui.KEY_MAP['down']:
        del_arrow_len = 0

def timer_handler():
    global time, position, angle, balls_to_shoot, ball_set, ready_next, next_pos0
    
    time += 1
    if time % 20 == 0 and balls_to_shoot > 0:
        ball_set.add( Ball(position, angle_to_dir(angle)) )
        balls_to_shoot -= 1
        if balls_to_shoot == 0:
            ready_next = True
            

    if ready_next and len(ball_set) == 0:
        ready_next = False
        position[0] = next_pos0
        next_level()
    
frame = simplegui.create_frame('BBTAN', WIDTH, HEIGHT)
frame.set_canvas_background('Black')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1, timer_handler)

timer.start()
frame.start()