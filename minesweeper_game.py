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

#Building grid
mines_list,not_mines_list = [],[]
for i in range(tm):
    mines_list.append(['mine','NoFlag','close'])
for i in range(wp*hp-tm):
    not_mines_list.append([0,'NoFlag','close'])
mine_placing_list = mines_list+not_mines_list
random.shuffle(mine_placing_list)
b = [0,'NoFlag','close'] # border 
outer_grid = [[b]*(wp+2)]+[[b]+mine_placing_list[i*wp:(i+1)*wp]+[b] for i in range(hp)]+[[b]*(wp+2)]
grid = [mine_placing_list[i*wp:(i+1)*wp] for i in range(hp)]
def mine_counter(x,y,g=outer_grid): # function for counting mines around node
    mines = 0
    for i in range(y,y+3):
        for j in range(x,x+3):
            if outer_grid[i][j][0] == 'mine':
                mines += 1
    return mines
for u in range(hp):
    for v in range(wp):
        if grid[u][v][0] != 'mine':
            grid[u][v][0] = mine_counter(v,u)

#Function for drawing chess pattern grid.
def surface_griding(c1,c2,speed=0):
	for y in range(hp):
		for x in range(wp):
			if speed:
				time.sleep(speed)
				pygame.display.update()
			pygame.draw.rect(screen,[c1,c2][int((x+y)%2==0)],pygame.Rect(x*rw,y*rh+info_bar,rw,rh))
# surface_griding(light_back_colour,dark_back_colour)
surface_griding(light_front_colour,dark_front_colour)

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

#Function for rendering square
def render_square(x,y,c1,c2):
	pygame.draw.rect(screen,[c1,c2][int((x+y)%2==0)],pygame.Rect(x*rw,y*rh+info_bar,rw,rh))

#Function for rendering numbers
number_font = pygame.font.Font(None,int(rw))
def render_number(x,y,number):
	num = number_font.render(str(number),True,number_colours[number-1])
	render_square(x,y,light_back_colour,dark_back_colour)
	screen.blit(num,num.get_rect(center=((2*x+1)*rw/2,info_bar+(2*y+1)*rh/2)))
render_number(0,0,1)

#Function for rendering mine
def render_mine(x,y):
	mine_rect_colour = random.choice(mine_colours)
	mine_circle_colour = [i/2 for i in mine_rect_colour]
	pygame.draw.rect(screen,mine_rect_colour,pygame.Rect(x*rw,y*rh+info_bar,rw,rh))
	pygame.draw.circle(screen,mine_circle_colour,((2*x+1)*rw/2,info_bar+(2*y+1)*rh/2),int(rw/4))
render_mine(0,1)

#Function for opening one square
def opender(x,y):
	if grid[y][x][0] == 'mine':
		render_mine(x,y)
	elif grid[y][x][0] == 0:
		render_square(x,y,light_back_colour,dark_back_colour)
	else:
		render_number(x,y,grid[y][x][0])
# def chain_reaction(x,y):
# 	for u in range(y,y+3):
# 		for v in range(x,x+3):
# 			if outer_grid[u][v][0] != 0 and u!=y and v!=x and outer_grid[u][v][2] == 'close':
# 				opender(v,u)
# 				outer_grid[u][v][2] = 'open'
# 			elif outer_grid[u][v] == 0 and outer_grid[u][v][2] == 'close':
# 				outer_grid[u][v] = 'open'
# 				render_square(v,u,light_back_colour,dark_back_colour)
# 				chain_reaction(v,u)



# info_bar_font = pygame.font.Font(None,info_bar)
# def timer_function():
# 	pygame.draw.rect(screen,[74,117,44],pygame.Rect(0,0,width,info_bar))
# 	seconds = int(pygame.time.get_ticks()/1000)
# 	timer = info_bar_font.render(str(seconds),True,(10,10,10))
# 	screen.blit(timer,(0,0))
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

		elif event.type == pygame.MOUSEBUTTONDOWN:
			x = int(pygame.mouse.get_pos()[0]//rw)
			y = int((pygame.mouse.get_pos()[1]-info_bar)//rh)
			print(x,y)
			if event.button == 1 and y>=0:
					if grid[y][x][1] == 'NoFlag':
						opender(x,y)
					elif grid[y][x][1] == 'Flag':
						render_square(x,y,light_front_colour,dark_front_colour)
						grid[y][x][1] = 'NoFlag'
			elif event.button == 3 and y>=0:
				if grid[y][x][1] == 'Flag':
					render_square(x,y,light_front_colour,dark_front_colour)
					grid[y][x][1] = 'NoFlag'
				elif grid[y][x][1] == 'NoFlag':
					render_flag(x,y)
					grid[y][x][1] = 'Flag'

	pygame.display.update()
	clock.tick(60)