import pygame
import random
import os
from pygame.constants import QUIT, K_DOWN,K_UP,K_LEFT,K_RIGHT,K_ESCAPE, K_KP_ENTER
pygame.init()
HEIGHT = 680
WIDTH = 1100
FPS = pygame.time.Clock()
FONT = pygame.font.SysFont('Verdana', 25)
main_display=pygame.display.set_mode((WIDTH,HEIGHT))
bg = pygame.transform.scale(pygame.image.load('background.png'),(WIDTH,HEIGHT))
bg_x1=0
bg_x2=bg.get_width()
finish = 0

image_path = 'Goose_1'
player_images = os.listdir(image_path)
image_index = 0
player_size = (100,50)
player = pygame.transform.scale(pygame.image.load('player.png').convert_alpha(),player_size)
player_rect=player.get_rect(center=(player_size[0]/2,HEIGHT/2))

score = 0
def create_explosion(x,y,t_m):
    exp_size = (100,100)
    exp = pygame.transform.scale(pygame.image.load('explosion.png').convert_alpha(), exp_size)
    exp_rect = pygame.Rect(x, y, *exp_size)
    return [exp, exp_rect, t_m]

def create_enemy(x=0,y=0,id=0):
    enemy_size = (60,30)
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), enemy_size)
    if x>0 and y> 0:
        enemy_rect =pygame.Rect(x, y, *enemy_size)
        if id == 1: enemy = pygame.transform.rotate(enemy,45)
        elif id == 2: enemy = pygame.transform.rotate(enemy,-45)
    else:
        enemy_rect =pygame.Rect(WIDTH, random.randint(0+enemy_size[1]/2,HEIGHT-enemy_size[1]/2), *enemy_size)
    return [enemy, enemy_rect, id]

def create_bonus():
    bonus_size = (50,100)
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(),bonus_size)
    bonus_rect = pygame.Rect(random.randint(0+bonus_size[0]/2,WIDTH-bonus_size[0]/2), 0, *bonus_size)
    return [bonus, bonus_rect]

enemies = []
bonuses = []
explosions = []
ENEMY_TIME = pygame.USEREVENT+1
BONUS_TIME = pygame.USEREVENT+2
CHANGE_IMAGE = pygame.USEREVENT +3
pygame.time.set_timer(ENEMY_TIME,5500-score*10)
pygame.time.set_timer(BONUS_TIME,750)
pygame.time.set_timer(CHANGE_IMAGE,200)

move_down = [0,18]
move_right = [18,0]
move_up = [0,-18]
move_left=[-18,0]
enemy_move = [random.randint(-6,-3),0]
enemy_move_1 = [-3,-3]
enemy_move_2 = [-3,3]
bonus_move = [0,random.randint(3,6)]
bg_move = 2.5
exp_move = [-bg_move,0]

playing= True
while playing:
    FPS.tick(20)
    keys=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keys[K_ESCAPE]: playing = False
        if event.type == ENEMY_TIME: enemies.append(create_enemy())
        if event.type == BONUS_TIME: bonuses.append(create_bonus())
        if finish==0 and event.type == CHANGE_IMAGE: 
            player = pygame.transform.scale(pygame.image.load(os.path.join(image_path, player_images[image_index])),player_size)
            image_index +=1
            if image_index >=len(player_images):
                image_index = 0

    bg_x1-=bg_move
    bg_x2 -= bg_move
    if bg_x1 < -bg.get_width(): bg_x1 = bg.get_width()
    if bg_x2 < -bg.get_width(): bg_x2 = bg.get_width()
    main_display.blit(bg,(bg_x1,0)) 
    main_display.blit(bg,(bg_x2,0)) 
    # read the botton pressed
    main_display.blit(player,player_rect)    
    main_display.blit(FONT.render(str(score), True,'blue'),(WIDTH-50,30))

    if keys[K_LEFT] and player_rect.left>0:
        player_rect=player_rect.move(move_left)
    if keys[K_DOWN] and player_rect.bottom<HEIGHT:
        player_rect=player_rect.move(move_down)
    if keys[K_UP] and player_rect.top>0:
        player_rect=player_rect.move(move_up)
    if keys[K_RIGHT] and player_rect.right<WIDTH:
        player_rect=player_rect.move(move_right)

    for enemy in enemies:
        main_display.blit(enemy[0],enemy[1])
        if enemy[2]==0:
            enemy[1]=enemy[1].move(enemy_move)
        elif enemy[2]==1:
            enemy[1]=enemy[1].move(enemy_move_1)
        else:
            enemy[1]=enemy[1].move(enemy_move_2)
        if enemy[1].left<-30: enemies.pop(enemies.index(enemy))
        for bonus in bonuses:
            if enemy[1].colliderect(bonus[1]):
                explosions.append(create_explosion(enemy[1][0],enemy[1][1],pygame.time.get_ticks()))
                enemies.append(create_enemy(enemy[1][0],enemy[1][1],1))
                enemies.append(create_enemy(enemy[1][0],enemy[1][1],2))
                if score < 20: enemies.pop(enemies.index(enemy))
                bonuses.pop(bonuses.index(bonus))
                
        if player_rect.colliderect(enemy[1]):
            explosions.append(create_explosion(enemy[1][0],enemy[1][1],pygame.time.get_ticks()))
            finish+=1
            player=pygame.transform.rotate(player,180)

    for exp in explosions:
        main_display.blit(exp[0],exp[1]) 
        exp[1]=exp[1].move(exp_move)
        if (pygame.time.get_ticks()-exp[2])>600:
            explosions.pop(explosions.index(exp))

    for bonus in bonuses:
        main_display.blit(bonus[0],bonus[1])
        bonus[1]=bonus[1].move(bonus_move)
        if bonus[1].top>HEIGHT: bonuses.pop(bonuses.index(bonus))
        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score+=1
    
    if finish >0:
            main_display.blit(FONT.render('GAME OVER', True,'red'),(WIDTH/2,HEIGHT/2))
            finish+=1
            player_rect=player_rect.move([3,3])
    if finish >120: playing = False
    pygame.display.flip()
    
        
    

