import pygame
from random import randint
from sys import exit
def gracz_animacja():
    global gracz_surf, gracz_index
    if gracz_rect.bottom < 525:
        gracz_surf= gracz_skacze
    else:
        gracz_index+=0.1
        if gracz_index>=len(gracz_idzie):
            gracz_index=0
        gracz_surf= gracz_idzie[int(gracz_index)]
def display_score():
   current_time = int(pygame.time.get_ticks()/1000) - start_time
   score_surf= font.render(f'Your score is: {current_time}',False,(0,0,0))
   score_rect= score_surf.get_rect(center=(400,100))
   window.blit(score_surf,score_rect) 
   return current_time
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True
def obstacle_movement(obstacle_list,obstacle_speed):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -=obstacle_speed
            if obstacle_rect.bottom == 520:
                window.blit(obstacle_surf,obstacle_rect)
            elif obstacle_rect.bottom>=300 and obstacle_rect.bottom<=400:
                window.blit(obstacle2_surf,obstacle_rect)
        obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x >-100]
        return obstacle_list
    else:
        return []
pygame.init()
clock=pygame.time.Clock()
window=pygame.display.set_mode((800, 600))
bg_music=pygame.mixer.Sound('muzyka/music.wav')
bg_music.play(loops=-1)
font= pygame.font.Font('grafiki/czcionka/vanguardian.ttf', 60)
font1= pygame.font.Font('grafiki/czcionka/vanguardian.ttf', 40)
font2= pygame.font.Font('grafiki/czcionka/vanguardian.ttf', 15)
font3=pygame.font.Font('grafiki/czcionka/Cyber City.otf',60)
icon= pygame.image.load('grafiki/icon_ye.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Running Ye')

menu_font= font3.render('RUNNING YE',True,(255,255,255))
studio= font2.render('@GOOFY AHH STUDIOS',True,(255,255,255))
menu_font_rect=menu_font.get_rect(center=(400,200))
play_button=font.render('CLICK START',True,(255,255,255),(0,0,0))
play_button_rect=play_button.get_rect(center=(420,369))
menu=pygame.image.load('grafiki/menu.png')

score = 0
high_score=0
gravity= 0
start_time=0
game_active= False
start= False
restart = pygame.image.load('grafiki/restart.png')
restart_font = font1.render('You died ! Press Spacebar', True, (255,255,255))
restart_font_rect=restart_font.get_rect(center=(400,50))

surface_sky= pygame.image.load('grafiki/tło/tlo.png')
surface_gr= pygame.image.load('grafiki/tło/ground.png')

speed_obstacle=10
obstacle_surf= pygame.image.load('grafiki/kamera/cameramen.png')
obstacle2_surf= pygame.image.load('grafiki/dron/drone3.png')
obstacle_rect_list=[]
obstacle_timer= pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

speed=4
gracz_idzie1 = pygame.image.load('grafiki/gracz/ye_idzie1.png').convert_alpha()
gracz_idzie2 = pygame.image.load('grafiki/gracz/ye_skacze.png').convert_alpha()
gracz_idzie= [gracz_idzie1,gracz_idzie2]
gracz_index=0
gracz_skacze=pygame.image.load('grafiki/gracz/ye_skacze.png').convert_alpha()
gracz_surf= gracz_idzie[gracz_index]
gracz_rect= gracz_surf.get_rect(topleft=(0,425))

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and gracz_rect.bottom>=525:
                    gravity= -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and gracz_rect.bottom>=525:
                    gravity= -20
        else:
            if event.type==pygame.MOUSEBUTTONDOWN and start == True:
                start_time=int(pygame.time.get_ticks()/1000)
                score-=start_time
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and score>0:
                game_active= True
                speed_obstacle=10
                start_time= int(pygame.time.get_ticks()/1000)        
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(obstacle_surf.get_rect(bottomright=(randint(900,1100),520)))
            else:
                if score>=10:
                    obstacle_rect_list.append(obstacle2_surf.get_rect(bottomright=(randint(900,1100),randint(300,400))))

    if game_active:
        keys= pygame.key.get_pressed()
        gracz_rect.y+= gravity
        if keys[pygame.K_d]:
            gracz_rect.x+=speed
        if keys[pygame.K_s]:
            gracz_rect.y+=5
        if keys[pygame.K_a]:
            gracz_rect.x-=speed
        if keys[pygame.K_RIGHT]:
            gracz_rect.x+=speed
        if keys[pygame.K_DOWN]: 
            gracz_rect.y+=5
        if keys[pygame.K_LEFT]:
            gracz_rect.x-=speed
        window.blit(surface_sky,(0,0))
        score = display_score()
        gravity+=1
        if gracz_rect.bottom >=525:
            gracz_rect.bottom = 525
        gracz_animacja()
        window.blit(gracz_surf,gracz_rect)
        obstacle_rect_list=obstacle_movement(obstacle_rect_list,speed_obstacle)
        game_active=collisions(gracz_rect,obstacle_rect_list)
        if gracz_rect.x>=700:
            gracz_rect.x=700
        if gracz_rect.x<=0:
            gracz_rect.x=0
        pygame.display.update()
        clock.tick(60)

    else:
        if score==0:
            mouse_pos= pygame.mouse.get_pos()
            window.blit(menu,(0,0))
            window.blit(menu_font,menu_font_rect)
            window.blit(studio,(600,580))
            window.blit(play_button,play_button_rect)
            start=True
        if play_button_rect.collidepoint(mouse_pos) and event.type==pygame.MOUSEBUTTONDOWN:
            game_active=True
            start=False
            play_button_rect.x=-400
        gracz_rect.x= 0
        gracz_rect.y= 400
        gravity= 0
        speed_obstacle=10
        obstacle_rect_list.clear()
        score_message= font1.render(f'Your score: {score}',False,(11,196,190))
        score_message_rect= score_message.get_rect(center=(400,100))
        if score>0:
            time_since_last_acceleration=0
            if high_score<=score:
                high_score=score
            high_score_message=font1.render(f'Your highscore: {high_score}',False,(11,196,169))
            high_score_message_rect=high_score_message.get_rect(center=(400,150))
            window.blit(restart,(0,0))
            window.blit(score_message,score_message_rect)
            window.blit(high_score_message,high_score_message_rect)
            window.blit(restart_font,restart_font_rect)
        pygame.display.update()
    pygame.display.update()
    clock.tick(60)