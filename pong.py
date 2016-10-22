# My final implementation of Pong for the Coursera Class
# An Introduction to Interactive Programming in Python

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = 240
paddle2_pos = 240
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2] 
    ball_vel = [0,0]
    if RIGHT:
        # up and right
        ball_vel[0] = random.randrange(2, 5)
        ball_vel[1] = random.randrange(-3, 0)
    elif LEFT:
        # up and left
        ball_vel[0] = random.randrange(-4, -1)
        ball_vel[1] = random.randrange(-3, 0)
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, score1, score2
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, LEFT, RIGHT      

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")        
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # collide and reflect off top and bottom of canvas
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]     

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")    

    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel >= PAD_HEIGHT) and (
        paddle1_pos + paddle1_vel <= HEIGHT):
        paddle1_pos += paddle1_vel
       
    if (paddle2_pos + paddle2_vel >= PAD_HEIGHT) and (
        paddle2_pos + paddle2_vel <= HEIGHT):
        paddle2_pos += paddle2_vel
 
    # draw paddles
    canvas.draw_text('|', (-8, paddle1_pos), 117, 'White')
    canvas.draw_text('|', (585, paddle2_pos), 117, 'White')    
    
    # determine whether paddle and ball collide
    # left paddle - paddle1_pos
    if (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH) and (
        ball_pos[1] <= paddle1_pos and ball_pos[1] >= paddle1_pos - PAD_HEIGHT):
        ball_vel[0] = - ball_vel[0] * 1.1
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        score2 += 1
        LEFT = False
        RIGHT = True
        spawn_ball(RIGHT)
        
    # right paddle - paddle2_pos
    if (ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH) and (
        ball_pos[1] <= paddle2_pos and ball_pos[1] >= paddle2_pos - PAD_HEIGHT):
        ball_vel[0] = - ball_vel[0] * 1.1  
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        score1 += 1
        LEFT = True
        RIGHT = False
        spawn_ball(LEFT)

    # draw scores
    canvas.draw_text(str(score1), [200, 90], 50, 'White')
    canvas.draw_text(str(score2), [375, 90], 50, 'White')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 4
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += vel
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= vel
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += vel
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= vel   
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0  

def restart():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', restart)

# start frame
new_game()
frame.start()

