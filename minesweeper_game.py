import pygame
import random
import time
import numpy
light_back_colour = [229,194,159]
dark_back_colour = [215,184,153]
light_front_colour = [170,215,81]
dark_front_colour = [162,209,73]
number_colours = [
	[80,139,196],[56,142,60],
	[211,47,47],[123,31,162],
	[255,143,1],[0,151,167],
	[66,66,66],[170,156,145]
]
mine_colours = [
	[219,50,54],[244,132,13],
	[244,194,13],[0,135,68],
	[72,230,241],[72,133,237],
	[237,68,181],[182,72,242]
]
pygame.init()
info_bar = 50
width = 400
hight = 400
wp = 10 # width proportion
hp = 10 # hight proportion
rw = width/wp
rh = hight/hp
tm = 10 # total amount of mines
screen = pygame.display.set_mode((width,hight+info_bar))
screen.fill([74,117,44])
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

mine_placing_list = [['mine','NoFlag']]*tm+[[0,'NoFlag']]*(wp*hp-tm)
random.shuffle(mine_placing_list)
b = [(0,None)] # boundary
outer_grid = [b*(wp+2)]+[b+mine_placing_list[i*wp:(i+1)*wp]+b for i in range(hp)]+[b*(wp+2)]
inner_grid = [mine_placing_list[i*wp:(i+1)*wp] for i in range(hp)]

#Function for counting mines around node
def mine_counter(x,y,g=outer_grid):
	mines = 0
	for i in range(y,y+3):
		for j in range(x,x+3):
			if g[i][j][0] == 'mine':
				mines += 1
	return mines
# for i in inner_grid:
# 	print(i)
# print(mine_counter(1,1))
# print(mine_counter(2,2))
# print(mine_counter(3,3))
# print(mine_counter(4,4))


for i in range(hp):
	for j in range(wp):
		if inner_grid[i][j][0] != 'mine':
			inner_grid[i][j][0] = mine_counter(i,j)
for i in inner_grid:
	print(i)



#Function for drawing chess pattern grid.
def surface_griding(c1,c2,speed=0):
	for y in range(hp):
		for x in range(wp):
			if speed:
				time.sleep(speed)
				pygame.display.update()
			pygame.draw.rect(screen,[c1,c2][int((x+y)%2==0)],pygame.Rect(x*rw,y*rh+info_bar,rw,rh))
surface_griding(light_back_colour,dark_back_colour)
# surface_griding(light_front_colour,dark_front_colour,speed=0.01)

#Flags
light_flag = pygame.image.load("C:\\Users\\User\\Desktop\\repo\\minesweeper\\light_flag.png")
light_flag = pygame.transform.scale(light_flag,(rw,rh))
dark_flag = pygame.image.load("C:\\Users\\User\\Desktop\\repo\\minesweeper\\dark_flag.png")
dark_flag = pygame.transform.scale(dark_flag,(rw,rh))
#Function for rendering flags
def render_flag(x,y):
	if (x+y) % 2 == 0:
		screen.blit(dark_flag,(x*rw,y*rh+info_bar))
	else:
		screen.blit(light_flag,(x*rw,y*rh+info_bar))
render_flag(0,2)

#Function for rendering numbers
number_font = pygame.font.Font(None,int(rw))
def render_number(x,y,number):
	num = number_font.render(str(number),True,number_colours[number-1])
	screen.blit(num,num.get_rect(center=((2*x+1)*rw/2,info_bar+(2*y+1)*rh/2)))
render_number(0,0,1)

#Function for rendering mine
def render_mine(x,y):
	mine_rect_colour = random.choice(mine_colours)
	mine_circle_colour = [i/2 for i in mine_rect_colour]
	pygame.draw.rect(screen,mine_rect_colour,pygame.Rect(x*rw,y*rh+info_bar,rw,rh))
	pygame.draw.circle(screen,mine_circle_colour,((2*x+1)*rw/2,info_bar+(2*y+1)*rh/2),int(rw/4))
render_mine(0,1)

info_bar_font = pygame.font.Font(None,info_bar)
# def timer_function():
# 	pygame.draw.rect(screen,[74,117,44],pygame.Rect(0,0,width,info_bar))
# 	seconds = int(pygame.time.get_ticks()/1000)
# 	timer = info_bar_font.render(str(seconds),True,(10,10,10))
# 	screen.blit(timer,(0,0))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
	pygame.display.update()
	clock.tick(30)