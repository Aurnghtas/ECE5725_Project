'''
ECE5725 Design with Embedded Operating Systems Final Project
author: Jiayi Zhou(jz2372), Bolong Tan(bt362)
'''

import pygame
from pygame.locals import * # for event MOUSE variables
import os
import sys
import random
import json

# pipes are the obstacles the bird need to avoid
def create_pipe():
    random_y = random.randint(50, height-pipe_gap-100)
    # pygame.Rect(left, top, width, height)
    top_pipe_rect = pygame.Rect(width, -pipe_flipped_image.get_height()+random_y, pipe_flipped_image.get_width(), pipe_flipped_image.get_height())
    bottom_pipe_rect = pygame.Rect(width, random_y+pipe_gap, pipe_image.get_width(), pipe_image.get_height())
    return {"top_pipe_rect": top_pipe_rect, "bottom_pipe_rect": bottom_pipe_rect, "visited": False}

def move_bird():
    global bird_speed
    bird_speed += gravity
    bird_rect.centery += bird_speed

# move base at 1 pixel per frame to the left
def move_base():
    global base_rect1, base_rect2
    base_rect1 = base_rect1.move(-1, 0)
    base_rect2 = base_rect2.move(-1, 0)

    if base_rect1.right <= 0:  # base_rect1 moves off the screen
        base_rect1.left = base_rect2.right  # move it to the right of base_rect2

    if base_rect2.right <= 0:  # base_rect2 moves off the screen
        base_rect2.left = base_rect1.right  # move it to the right of base_rect1

def draw_message():
    screen.blit(message, message_rect)

def draw_base():
    screen.blit(base, base_rect1)
    screen.blit(base, base_rect2)

def draw_background():
    screen.blit(background_day, background_day_rect)

def draw_bird():
    angle = -bird_speed * 10
    rotated_bird = pygame.transform.rotate(bird, angle)
    rotated_bird_rect = rotated_bird.get_rect(center=bird_rect.center)
    screen.blit(rotated_bird, rotated_bird_rect)

def draw_pipe(pipe):
    screen.blit(pipe_image, pipe["bottom_pipe_rect"])
    screen.blit(pipe_flipped_image, pipe["top_pipe_rect"])

def detect_collision():
    # if the bird hits the pipe
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe["bottom_pipe_rect"]) or bird_rect.colliderect(pipe["top_pipe_rect"]):
            return True

    # bird hits the top or the base
    if bird_rect.top <= -40 or bird_rect.bottom >= 360:
        return True

    return None

def draw_score():
    text_pos = (width/2, height-base_rect1.height/2)
    text_surface = font.render(f"Score: {score}", True, WHITE)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, rect)

def draw_highest_score():
    score_pos = (width/5, height-base_rect1.height/2-10)
    score_surface = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_surface.get_rect(center=score_pos)
    screen.blit(score_surface, score_rect)

    highest_score_pos = (width/2+5, height-base_rect1.height/2-10)
    highest_score_surface = font.render(f"Highest Score: {highest_score}", True, WHITE)
    highest_score_rect = score_surface.get_rect(center=highest_score_pos)
    screen.blit(highest_score_surface, highest_score_rect)

def draw_leaderboard():
    global leaderboard_box_rect
    leaderboard_pos = (width/2+5, height-base_rect1.height/2+15)
    leaderboard_surface = font.render("Leaderboard", True, WHITE)
    leaderboard_rect = leaderboard_surface.get_rect(center=(leaderboard_pos))
    leaderboard_box_rect = leaderboard_rect.inflate(10, 10)
    pygame.draw.rect(screen, WHITE, leaderboard_box_rect, 1)
    screen.blit(leaderboard_surface, leaderboard_rect)

def draw_leaderboard_data():
    global back_box_rect, restart_box_rect
    # leaderboard title
    title_font = pygame.font.Font(None, 30)
    title_surface = title_font.render("Leaderboard", True, WHITE)
    title_rect = title_surface.get_rect(center=(width/2,30))
    screen.blit(title_surface, title_rect)

    # leaderboard data
    data_font = pygame.font.Font(None, 20)
    data_surface = data_font.render("Player", True, WHITE)
    data_rect = data_surface.get_rect(topleft=(0,60))
    screen.blit(data_surface, data_rect)

    data_surface = data_font.render("Score", True, WHITE)
    data_rect = data_surface.get_rect(topleft=(120, 60))
    screen.blit(data_surface, data_rect)

    data = load_leaderboard()
    index = 1
    for entry in data:
        data_surface = data_font.render(entry["player_id"], True, WHITE)
        data_rect = data_surface.get_rect(topleft=(0, 60+index*20))
        screen.blit(data_surface, data_rect)

        data_surface = data_font.render(str(entry["score"]), True, WHITE)
        data_rect = data_surface.get_rect(topleft=(120, 60+index*20))
        screen.blit(data_surface, data_rect)

        index+=1

    back_restart_spacing = 50

    # back button
    back_font = pygame.font.Font(None, 20)
    back_surface = back_font.render("Back", True, WHITE)
    back_rect = back_surface.get_rect()
    back_box_rect = back_rect.inflate(10, 10)

    # restart button
    restart_font = pygame.font.Font(None, 20)
    restart_surface = restart_font.render("Restart", True, WHITE)
    restart_rect = restart_surface.get_rect()
    restart_box_rect = restart_rect.inflate(10, 10)

    # adjust their positions
    total_width = back_box_rect.width+back_restart_spacing+restart_box_rect.width
    back_box_rect.topleft = ((width-total_width)/2, 280)
    back_rect.center = back_box_rect.center
    restart_box_rect.topleft = ((width-total_width)/2+back_box_rect.width+back_restart_spacing, 280)
    restart_rect.center = restart_box_rect.center

    # draw buttons
    pygame.draw.rect(screen, WHITE, back_box_rect, 1)
    screen.blit(back_surface, back_rect)
    pygame.draw.rect(screen, WHITE, restart_box_rect, 1)
    screen.blit(restart_surface, restart_rect)


def draw_game_over():
    restart_font = pygame.font.Font(None, 21)
    restart = "Press Space Key to Start Over"
    restart_pos = (width/2, height/2)
    restart_surface = restart_font.render(restart, True, WHITE)
    restart_rect = restart_surface.get_rect(center=restart_pos)
    screen.blit(restart_surface, restart_rect)

    screen.blit(game_over_message, game_over_message.get_rect(center=(width/2, (height-base_rect1.height)/2)))

def draw_keybord():
    KEY_WIDTH = 20
    KEY_HEIGHT = 20
    KEY_PADDING = 5

    keyboard_layout = [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["Z", "X", "C", "V", "B", "N", "M"],
        ["Space", "Delete"],
        ["Confirm"]
    ]

    key_y = (height-base_rect1.height)/2
    for row in keyboard_layout:
        if len(row) == 2:
            key_x = (width - (5*KEY_WIDTH+KEY_PADDING+6*KEY_WIDTH))/2
        elif len(row) == 1:
            key_x = (width - 7*KEY_WIDTH)/2
        else:
            key_x = (width - (len(row)*(KEY_WIDTH+KEY_PADDING)-KEY_PADDING))/2

        for character in row:
            if character == "Space":
                key_width = 5*KEY_WIDTH
            elif character == "Delete":
                key_width = 6*KEY_WIDTH
            elif character == "Confirm":
                key_width = 7*KEY_WIDTH
            else:
                key_width = KEY_WIDTH
            key_rect = pygame.Rect(key_x, key_y, key_width, KEY_HEIGHT)
            keys.append({"key": character, "key_rect": key_rect})
            if len(row) == 2:
                key_x += 5*KEY_WIDTH+KEY_PADDING
            else:
                key_x += KEY_WIDTH+KEY_PADDING
        key_y += KEY_HEIGHT+KEY_PADDING

    key_font = pygame.font.Font(None, 20)
    for character in keys:
        key_surface = key_font.render(character["key"], True, WHITE)
        key_rect = key_surface.get_rect(center=character["key_rect"].center)
        screen.blit(key_surface, key_rect)

    subtitle_font = pygame.font.Font(None, 20)
    subtitle_surface = subtitle_font.render("Enter Your Preferred ID", True, WHITE)
    subtitle_rect = subtitle_surface.get_rect(center=(width/2, 50))
    screen.blit(subtitle_surface, subtitle_rect)

def draw_enter_to_start():
    global enter_to_start_button_rect
    enter_to_start = "Press Here to Start"
    enter_to_start_font = pygame.font.Font(None, 22)
    enter_to_start_surface = enter_to_start_font.render(enter_to_start, True, WHITE)
    enter_to_start_rect = enter_to_start_surface.get_rect(center=(width/2, height/4+8))
    enter_to_start_button_rect = enter_to_start_rect.inflate(10, 10)
    pygame.draw.rect(screen, WHITE, enter_to_start_button_rect, 1)
    screen.blit(enter_to_start_surface, enter_to_start_rect)

def draw_player_id():
    text_font = pygame.font.Font(None, 20)
    text_surface = text_font.render(player_id, True, WHITE)
    text_rect = text_surface.get_rect(center=(width/2, 20))
    text_box_rect = text_rect.inflate(10, 10)
    pygame.draw.rect(screen, WHITE, text_box_rect, 1)
    screen.blit(text_surface, text_rect)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        raise FileNotFoundError
    else:
        with open(LEADERBOARD_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

def save_leaderboard(data):
    with open (LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=4)

def update_leaderboard():
    data = load_leaderboard()
    existed_player_id = False

    for entry in data:
        if entry["player_id"] == player_id:
            existed_player_id = True
            if entry["score"] < highest_score:
                entry["score"] = highest_score
            break

    if not existed_player_id:
        data.append({"player_id": player_id, "score": highest_score})
        data.sort(key=lambda x: x["score"], reverse=True)
        data = data[:10]

    save_leaderboard(data)

pygame.init()
pygame.mixer.init()

# disable the mouse icon
pygame.mouse.set_visible(True)

# some pre-defined variables
BLACK = 0, 0, 0
WHITE = 255, 255, 255
size = width, height = 240, 320 # screen size of the piTFT
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 25)
gravity = 0.1

# background of the game
background_day = pygame.image.load("images/background-day.png") # create a Surface with the background-day data
background_day_original_width = background_day.get_width()
background_day_original_height = background_day.get_height()
background_day = pygame.transform.scale(background_day, size)  # scale to screen size
background_day_rect = background_day.get_rect()

# base of the game
base = pygame.image.load("images/base.png")
base_original_height = base.get_height()
base_scaled_height = (base_original_height/background_day_original_height)*height
base = pygame.transform.scale(base, (width, base_scaled_height))
base_rect1 = base.get_rect()
base_rect1.topleft = (0, height - base_rect1.height)
base_rect2 = base.get_rect()
base_rect2.topleft = (width, height - base_rect2.height)

# bird of the game
bird_down = pygame.image.load("images/bluebird-downflap.png")
bird_mid = pygame.image.load("images/bluebird-midflap.png")
bird_up = pygame.image.load("images/bluebird-upflap.png")
bird_states = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_states[bird_index]
bird_rect = bird.get_rect(center=(width/2, (height-base_rect1.height)/2))
bird_speed = 0
bird_spawn_time = 0

# pipe of the game
pipe_image = pygame.image.load("images/pipe-green.png")
pipe_image_scaled_width = (pipe_image.get_width()/background_day_original_width)*width
pipe_image_scaled_height = (pipe_image.get_height()/background_day_original_height)*height
pipe_image = pygame.transform.scale(pipe_image, (pipe_image_scaled_width, pipe_image_scaled_height))
pipe_flipped_image = pygame.transform.flip(pipe_image, False, True)  # flip the pipe for the top
pipe_list = []
pipe_gap = 100
pipe_spawn_time = 0
pipe_speed = 2

# welcome page
welcome = True
keys = []
player_id = ""
player_id_entered = False
message = pygame.image.load("images/message.png")
message = pygame.transform.scale(message, size)
message_rect = message.get_rect()
enter_to_start_button_rect = None

# game over page
game_over = False
game_over_message = pygame.image.load("images/gameover.png")

# leaderboard page
leaderboard = False
leaderboard_box_rect = None
LEADERBOARD_FILE = "leaderboard.json"
back_box_rect = None
restart_box_rect = None

# scores
score = 0
highest_score = 0

# levels of the game based on obtained score
easy = 10
medium = 30

# some audio
die_audio = pygame.mixer.Sound("audio/die.wav")
hit_audio = pygame.mixer.Sound("audio/hit.wav")
point_audio = pygame.mixer.Sound("audio/point.wav")
wing_audio = pygame.mixer.Sound("audio/wing.wav")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if welcome:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not player_id_entered:
                    if enter_to_start_button_rect.collidepoint(pos):
                        player_id_entered = True
                else:
                    for character in keys:
                        if character["key_rect"].collidepoint(pos):
                            if character["key"] == "Delete":
                                player_id = player_id[:-1]
                            elif character["key"] == "Space":
                                player_id += " "
                            elif character["key"] == "Confirm":
                                welcome = False
                            else:
                                player_id += character["key"]
                            break
        elif leaderboard:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if back_box_rect.collidepoint(pos):
                    leaderboard = False
                elif restart_box_rect.collidepoint(pos):
                    leaderboard = False
                    welcome = True
                    player_id_entered = False
                    player_id = ""
                    score = 0
                    highest_score = 0
                    bird_index = 0
                    bird = bird_states[bird_index]
                    bird_rect = bird.get_rect(center=(width / 2, (height - base_rect1.height) / 2))
                    bird_speed = 0
                    bird_spawn_time = 0
                    pipe_list.clear()
                    pipe_spawn_time = 0
                    pipe_speed = 2
                    game_over = False
        else:
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    bird_speed = -25*gravity
                    wing_audio.play()

            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    score = 0
                    bird_index = 0
                    bird = bird_states[bird_index]
                    bird_rect = bird.get_rect(center=(width / 2, (height - base_rect1.height) / 2))
                    bird_speed = 0
                    bird_spawn_time = 0
                    pipe_list.clear()
                    pipe_spawn_time = 0
                    pipe_speed = 2

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not leaderboard:
                    if leaderboard_box_rect.collidepoint(pos):
                        leaderboard = True

    if welcome:
        screen.fill(BLACK)
        if not player_id_entered:
            draw_message()
            draw_enter_to_start()
        else:
            draw_keybord()
            draw_player_id()
    elif leaderboard:
        screen.fill(BLACK)
        draw_leaderboard_data()
    else:
        # spawn (create) birds/pipes
        if not game_over:
            bird_spawn_time += clock.get_time()
            if  bird_spawn_time > 100:  # spawn a bird every 0.1 seconds
                bird_index = (bird_index+1)%3
                bird = bird_states[bird_index]
                bird_rect = bird.get_rect(center=bird_rect.center)
                bird_spawn_time = 0

            pipe_spawn_time += clock.get_time()
            if score < easy:
                if pipe_spawn_time > 1500:  # spawn a pipe every 1.5 seconds
                    pipe_list.append(create_pipe())
                    pipe_spawn_time = 0
            elif score>=easy and score<medium:
                if pipe_spawn_time > 1000:  # spawn a pipe every 1 seconds
                    pipe_list.append(create_pipe())
                    pipe_spawn_time = 0
            else:
                if pipe_spawn_time > 500:  # spawn a pipe every 0.5 seconds
                    pipe_list.append(create_pipe())
                    pipe_spawn_time = 0

            move_bird()

        move_base()

        screen.fill(BLACK) # erase the screen with black
        draw_background()

        if detect_collision():
            game_over = True
            pipe_list.clear()
            bird_rect = bird.get_rect(center=(width/2, height/2))
            bird_speed = 0
            hit_audio.play()

        if not game_over:
            draw_bird()

            # filter out some pipes that are out of the left boundary of the screen
            pipe_list = [pipe for pipe in pipe_list if pipe["top_pipe_rect"].right > 0]
            for pipe in pipe_list:
                pipe["top_pipe_rect"].x -= pipe_speed
                pipe["bottom_pipe_rect"].x -= pipe_speed

                # keep track of the score the player got
                if not pipe["visited"] and bird_rect.centerx > pipe["top_pipe_rect"].centerx:
                    score+=1
                    point_audio.play()
                    highest_score = max(score, highest_score)
                    pipe["visited"] = True

                draw_pipe(pipe)

        draw_base()
        if not game_over:
            draw_score()
        elif game_over:
            die_audio.play()
            draw_highest_score()
            draw_game_over()
            draw_leaderboard()
            update_leaderboard()
    pygame.display.flip() # display things on screen

    if score < medium:
        clock.tick(60) # set 60 FPS
    else:
        clock.tick(90)  # set 90 FPS