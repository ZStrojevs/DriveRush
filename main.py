import pygame
from pygame.locals import *
import random
import button
import math
import json
pygame.init()

# create the window
width = 600
height = 800
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
#vehicle gap
vehicle_gap = 25

# colors
gray = (44, 51, 51)
green = (83, 145, 101)
red = (223, 46, 56)
white = (238, 238, 238)
yellow = (253, 211, 106)
black = (0, 0, 0)
blue = (25, 167, 206)

# road and marker sizes
road_width = 300
marker_width = 5
marker_height = 50

# lane coordinates
lane_offset = (width - road_width) // 2
left_lane = lane_offset + 50
center_lane = lane_offset + 150
right_lane = lane_offset + 250
lanes = [left_lane, center_lane, right_lane]

# calculate the position of the road and markers relative to the screen size
road_x = (width - road_width) // 2
left_edge_marker_x = road_x - marker_width
right_edge_marker_x = road_x + road_width

# road and edge markers
road = (road_x, 0, road_width, height)
left_edge_marker = (left_edge_marker_x, 0, marker_width, height)
right_edge_marker = (right_edge_marker_x, 0, marker_width, height)

# for animating movement of the lane markers
lane_marker_move_y = 0
# pause
game_paused = False
# sound 
crash_sound = pygame.mixer.Sound("crash.wav")
main_menu_sound = pygame.mixer.Sound("Main_menu.wav")
hard_diff_sound = pygame.mixer.Sound("Hard_diff.wav")
crash_sound.set_volume(0.1)
hard_diff_sound.set_volume(0.1)
# images 
resume_img = pygame.image.load("button/button_resume.png").convert_alpha()
quit_img = pygame.image.load("button/button_quit.png").convert_alpha()
back_img = pygame.image.load('button/button_back.png').convert_alpha()
start_img = pygame.image.load('button/button_start.png').convert_alpha()
exit_img = pygame.image.load('button/button_exit.png').convert_alpha()
easy_img = pygame.image.load('button/button_easy.png').convert_alpha()
medium_img = pygame.image.load('button/button_medium.png').convert_alpha()
hard_img = pygame.image.load('button/button_hard.png').convert_alpha()
main_img = pygame.image.load('button/button_main.png').convert_alpha()
slaughter = pygame.image.load('images/slaughter.png')
slaughter_scaled = pygame.transform.scale(slaughter,(width, height))


#create button instances
resume_button = button.Button(0, 125, resume_img, 1)
quit_button = button.Button(width / 3, 250, quit_img, 1)
back_button = button.Button(width / 3, 450, back_img, 1)

main_button = button.Button(width / 3, 500, main_img, 1)

main_button2 = button.Button(width / 3, 375, main_img, 1)

start_button = button.Button(width / 3, 325, start_img, 1)
exit_button = button.Button(width / 3, 500, exit_img, 1)
easy_button = button.Button(0, 125, easy_img, 1)
medium_button = button.Button(width / 3, 250, medium_img, 1)
hard_button = button.Button(width / 3, 375, hard_img, 1)

# player's starting coordinates

player_x = width/2
player_y = height*0.8

# frame settings
clock = pygame.time.Clock()
fps = 120

# game settings
gameover = False

class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y, solo):
        pygame.sprite.Sprite.__init__(self)
        
        # scale the image down so it's not wider than the lane
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.solo = solo        
class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y, True)
        
# sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# create the player's car
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# load the vehicle images
image_filenames = ['pickup_truck.png','pickup_truck2.png', 'taxi.png', 'van.png','car2.png','police.png','ambulance.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('images/' + image_filename)
    vehicle_images.append(image)
    
# load the crash image
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()
#menu
menu = True
difficulty = False
menu_state = "main"
menu_music = False
color = green
# game loop
running = True
game_menu = True
Easter_egg_menu = False
pygame.mixer.music.set_volume(0.05)
blit = False

with open('data.json', 'r') as f:
    data = json.load(f)

while running:
    while menu:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        pygame.display.set_caption("Drive Rush")
        screen.fill(green)
        if menu_music == False:
            pygame.mixer.music.load('Main_menu.wav')
            pygame.mixer.music.play(-1,0.0)
            menu_music = True
        
        font_path = "BaiJamjuree-Bold.ttf"
        font_size = 70
        font = pygame.font.Font(font_path, font_size)

        # create a sine wave to animate the text
        wave_amplitude = 10
        wave_frequency = 0.01
        wave_offset = 0
        wave_motion = wave_amplitude * math.sin(wave_frequency * pygame.time.get_ticks() + wave_offset)

        # render the text with the wave motion applied to its y-coordinate
        text_outline = font.render('Drive Rush', True, (0, 0, 0))
        text_outline_rect = text_outline.get_rect()
        text_outline_rect.center = (width/2, 100 + wave_motion)

        text = font.render('Drive Rush', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width/2, 100 + wave_motion)

        # blit the text with outline
        outline_offset = 3.7
        screen.blit(text_outline, text_outline_rect.move(outline_offset, outline_offset))
        screen.blit(text_outline, text_outline_rect.move(-outline_offset, outline_offset))
        screen.blit(text_outline, text_outline_rect.move(outline_offset, -outline_offset))
        screen.blit(text_outline, text_outline_rect.move(-outline_offset, -outline_offset))

        screen.blit(text, text_rect)
        

        if start_button.draw(screen):
            difficulty = True
            game_menu = True
            menu_state = "difficulty"
        if exit_button.draw(screen):
                menu = False
                running = False
        if game_menu == True:
            if difficulty == True:
                screen.fill(green)
                if menu_state == "difficulty":
                    if easy_button.draw(screen):
                        menu = False
                        vehicle_gap = 50
                        menu_state = "main"
                        color = green
                        difficulty = 0.25
                        speed = 2
                        score_amount = 5
                        score = 0
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('Easy_diff.wav')
                        pygame.mixer.music.play(-1, 0.0)
                        pygame.display.set_caption("Drive Rush Easy")
                        difficulty_level = "easy"
                    if medium_button.draw(screen):
                        menu = False
                        vehicle_gap = 25
                        difficulty = 0.5
                        speed = 2
                        score_amount = 3
                        score = 0
                        menu_state = "main"
                        color = blue
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('Medium_diff.wav')
                        pygame.mixer.music.play(-1, 0.0)
                        pygame.display.set_caption("Drive Rush Medium")
                        difficulty_level = "medium"
                    if hard_button.draw(screen):
                        menu = False
                        vehicle_gap = 10
                        menu_state = "main"
                        difficulty = 1
                        speed = 2
                        score_amount = 2
                        score = 0
                        color = red
                        music = 'Hard_diff.wav'
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('Hard_diff.wav')
                        pygame.mixer.music.play(-1, 0.0)
                        pygame.display.set_caption("Drive Rush Hard")
                        difficulty_level = "hard"
                    if main_button.draw(screen):
                        game_menu = False


        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                menu = False
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # move the player's car using the left/right arrow keys
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                game_paused = True
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100
            elif event.key == pygame.K_1:
                # set the current key to 1
                current_key = 1
            elif event.key == pygame.K_9:
                # check if the current key is 1, and set it to 9 if it is
                if current_key == 1:
                    current_key = 9
                else:
                    current_key = None
            elif event.key == pygame.K_8:
                # check if the current key is 9, and set it to 8 if it is
                if current_key == 9:
                    current_key = 8
                else:
                    current_key = None
            elif event.key == pygame.K_3:
                if current_key == 8:
                    # Modify the "secret" value to "true"
                    data['secret'] = True
                    
                    # Write the updated JSON data back to the file
                    with open('data.json', 'w') as f:
                        json.dump(data, f)
                    
                    # Play the Easter egg sound
                    Easter_egg_menu = True
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Eggus.wav")
                    pygame.mixer.music.play()
                else:
                    current_key = None
                
            # check if there's a side swipe collision after changing lanes
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    pygame.mixer.Sound.play(crash_sound)
                    pygame.mixer.music.stop()
                    gameover = True
                    
                    # place the player's car next to other vehicle
                    # and determine where to position the crash image
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]                     

    
    menu_music = False
    if Easter_egg_menu == True:
        screen.fill((0,0,0))
        screen.blit(slaughter_scaled,(0 , 0))
              
    elif game_paused == True:
        screen.fill(green)
        
        #check menu state
        if menu_state == "main":
        #draw pause screen buttons
            if resume_button.draw(screen):
                game_paused = False
            if quit_button.draw(screen):
                running = False
            if main_button2.draw(screen):
                game_menu = False
                game_paused = False
                menu = True
                gameover = False
                score = 0
                vehicle_group.empty()
                player.rect.center = [player_x, player_y]
                pygame.mixer.music.play(-1)
            for event in pygame.event.get():
                    
                # move the player's car using the left/right arrow keys
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        game_paused = True
                        if event.key == pygame.K_1:
                            # set the current key to 1
                            current_key = 1
                        elif event.key == pygame.K_9:
                            # check if the current key is 1, and set it to 9 if it is
                            if current_key == 1:
                                current_key = 9
                            else:
                                current_key = None
                        elif event.key == pygame.K_8:
                            # check if the current key is 9, and set it to 8 if it is
                            if current_key == 9:
                                current_key = 8
                            else:
                                current_key = None
                        elif event.key == pygame.K_3:
                            if current_key == 8:
                                print("sus")
                            else:
                                current_key = None

    else:
        # draw the grass
        screen.fill(color)
        # draw the road
        pygame.draw.rect(screen, gray, road)
        
        # draw the edge markers
        pygame.draw.rect(screen, yellow, left_edge_marker)
        pygame.draw.rect(screen, yellow, right_edge_marker)
        
        # draw the lane markers
        lane_marker_move_y += speed * 2
        if lane_marker_move_y >= marker_height * 2:
            lane_marker_move_y = 0
        for y in range(marker_height * -2, height, marker_height * 2):
            pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
            pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
            
        # draw the player's car
        player_group.draw(screen)
        
        # add a vehicle
        if len(vehicle_group) < 2:
            
            # ensure there's enough gap between vehicles
            add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle_gap:
                    add_vehicle = False
                    
            if add_vehicle:
                
                # select a random lane
                lane = random.choice(lanes)
                lane2 = random.choice(lanes)
                # select a random vehicle image
                image = random.choice(vehicle_images)
                vehicle = Vehicle(image, lane, height / -2, True)
                vehicle_group.add(vehicle)
                
                if random.randint(0,1) == 0:
                    while True:
                        if lane == lane2:
                            lane2 = random.choice(lanes)
                        else:
                            break
                    image = random.choice(vehicle_images)
                    vehicle2 = Vehicle(image, lane2, height / -2, False)
                    vehicle_group.add(vehicle2)
                vehicle_gap += vehicle.rect.height + vehicle_gap
                
        
        # make the vehicles move
        for vehicle in vehicle_group:
            vehicle.rect.y += speed
            
            # remove vehicle once it goes off screen
            if vehicle.rect.top >= height:
                if vehicle.solo:
                    score += 1

                vehicle.kill()
                try:
                    if vehicle2.rect.top >= height:
                            vehicle2.kill()
                except NameError:
                    pass
                
                
                # speed up the game after passing 5 vehicles
                if score > 0 and score % score_amount == 0:
                    if vehicle.solo:
                        speed += difficulty
        
        # draw the vehicles
        vehicle_group.draw(screen)
        
        # display the score

        font_path = "BaiJamjuree-Bold.ttf"
        font_size = 20
        font = pygame.font.Font(font_path, font_size)

        text_outline = font.render('Score: ' + str(score), True, (0, 0, 0))
        text_outline_rect = text_outline.get_rect()
        text_outline_rect.center = (width/2, 60)

        # render the text on top of the outline
        text = font.render('Score: ' + str(score), True, white)
        text_rect = text.get_rect()
        text_rect.center = (width/2, 60)

        # draw the outline first and then the text
        screen.blit(text_outline, text_outline_rect.move(2, 2))
        screen.blit(text_outline, text_outline_rect.move(-2, 2))
        screen.blit(text_outline, text_outline_rect.move(2, -2))
        screen.blit(text_outline, text_outline_rect.move(-2, -2))

        #draw the text
        screen.blit(text, text_rect)

        # check if there's a head on collision
        if pygame.sprite.spritecollide(player, vehicle_group, True):
            pygame.mixer.Sound.play(crash_sound)
            pygame.mixer.music.stop()
            gameover = True
            crash_rect.center = [player.rect.center[0], player.rect.top]
                
        # display game over
        if gameover:
            screen.blit(crash, crash_rect)
            pygame.draw.rect(screen, red, (0, 50, width, 100))
            font_size = 18
            font = pygame.font.Font(font_path, font_size)
            text = font.render(fr'Game over. Return To the menu? (Enter Y or N). Final score: {score}', True, white)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 100)
            screen.blit(text, text_rect)

            # Load the existing high score from the file
            with open('high_scores.json', 'r+') as f:
                # load the existing high scores
                high_scores = json.load(f)

                # get the current high score for the difficulty level
                current_high_score = high_scores.get(difficulty_level, {}).get('high_score', 0)

                # compare the current score to the high score
                if score > current_high_score:
                    # update the high score for the difficulty level
                    high_scores[difficulty_level] = {'high_score': score}

                    # write the updated high scores to the file
                    f.seek(0)
                    json.dump(high_scores, f, indent=4)
                    f.truncate()

                    # Display the updated high score immediately
                    high_score_text = font.render(fr'New High Score ({difficulty_level}): {score}', True, white)
                    high_score_rect = high_score_text.get_rect()
                    high_score_rect.center = (width / 2, 75)
                    screen.blit(high_score_text, high_score_rect)
                else:
                    # Display the high score based on the difficulty level
                    high_score_text = font.render(fr'High Score ({difficulty_level}): {current_high_score}', True, white)
                    high_score_rect = high_score_text.get_rect()
                    high_score_rect.center = (width / 2, 75)
                    screen.blit(high_score_text, high_score_rect)
    

        pygame.display.update()

        # wait for user's input to play again or exit
        while gameover:
            
            clock.tick(fps)
            
            for event in pygame.event.get():
                
                if event.type == QUIT:
                    gameover = False
                    running = False
                    
                # get the user's input (y or n)
                if event.type == KEYDOWN:
                    if event.key == K_n:
                        # reset the game
                        gameover = False
                        speed = 2
                        score = 0
                        vehicle_group.empty()
                        pygame.mixer.music.play(-1, 0.0)
                        player.rect.center = [player_x, player_y]
                    elif event.key == K_y:
                        # exit the loops
                        game_menu = False
                        menu = True
                        gameover = False
                        score = 0
                        vehicle_group.empty()
                        player.rect.center = [player_x, player_y]
                        pygame.mixer.music.play(-1)

    pygame.display.update()
pygame.quit()
