import pygame
import random
import sys
pygame.init()
pygame.display.set_caption("Square Dodging")
pygame.display.set_icon(pygame.image.load('icon.png'))
game_running=True
game_start=False
player_position=[325,600]
enemy_position=[random.randint(0,650),0]
screen=pygame.display.set_mode((700,700))
speed=10
score=0
enemy_list=[enemy_position]

#Make enemy drop down and delete enemy
def update_enemy_positions(enemy_list,score):
	for idx,enemy_position in enumerate(enemy_list):
		if enemy_position[1]>=-50 and enemy_position[1]<652 and game_start:
			enemy_position[1]+=speed
		else:
			enemy_list.pop(idx)
			score+=1
	return score

#Check collision between 1 enemy and player
def detect_collision(player_position,enemy_position):
	if (enemy_position[0]>=player_position[0]and enemy_position[0]<(player_position[0]+50))or(player_position[0]>=enemy_position[0]and player_position[0]<(enemy_position[0]+50)):
		if (enemy_position[1]>=player_position[1]and enemy_position[1]<(player_position[1]+50))or(player_position[1]>=enemy_position[1]and player_position[1]<(enemy_position[1]+50)):
			return True
	return False

#Check collision between all enemy and player
def collision_check(enemy_list,player_position):
	for enemy_position in enemy_list:
		if detect_collision(enemy_position,player_position) and game_start:
			return True
	return False

#Main loop
while game_running:
	pygame.time.Clock().tick(60)
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
	if not game_start:
		score=0
	
	#Player controll
	if event.type==pygame.KEYDOWN:
		if event.key==pygame.K_LEFT and not player_position[0]==0:
			player_position[0]-=12.5
			if not game_start:
				game_start=True
		if event.key==pygame.K_RIGHT and not player_position[0]==650:
			player_position[0]+=12.5
			if not game_start:
				game_start=True
	
	#Enemy
	if len(enemy_list)< 10 and random.random()<0.1 and game_start:
		x_pos=random.randint(0,650)
		y_pos=-50
		enemy_list.append([x_pos,y_pos])
	score=update_enemy_positions(enemy_list,score)
	speed=score/40+10
	
	#Graphic
	screen.fill((0,0,0))
	for enemy_position in enemy_list:
		pygame.draw.rect(screen,(0,0,255),(enemy_position[0],enemy_position[1],50,50))
	pygame.draw.rect(screen,(255,0,0),(player_position[0],player_position[1],50,50))
	pygame.draw.rect(screen,(0,0,0),([0,650],(700,240)))
	pygame.draw.rect(screen,(0,255,0),([0,650],(700,2)))
	pygame.draw.rect(screen,(0,0,0),([0,650],(700,0)))
	pygame.draw.rect(screen,(0,255,0),([0,652],(700,0)))
	screen.blit(pygame.font.SysFont("monospace",35).render("Score:"+str(score),1,[255,255,255]),(25,655))
	
	#Game not start
	if not game_start:
		screen.blit(pygame.font.SysFont("monospace",25).render("press ← to go left",1,[255,255,255]),(20,605))
		screen.blit(pygame.font.SysFont("monospace",25).render("press → to go right",1,[255,255,255]),(410,605))
	
	pygame.display.update()
	
	#Game over
	while collision_check(enemy_list,player_position):
		pygame.time.Clock().tick(10)
		screen.blit(pygame.font.SysFont("monospace",60).render("Game over",1,[255,0,0]),(200,280))
		screen.blit(pygame.font.SysFont("monospace",30).render("press ↑ to continue and ↓ to quit",1,[255,255,255]),(50,370))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type==pygame.QUIT or event.type==pygame.KEYDOWN and event.key==pygame.K_DOWN:
				sys.exit()
			if event.type==pygame.KEYDOWN and event.key==pygame.K_UP:
				game_running=True
				player_position=[325,600]
				game_start=False