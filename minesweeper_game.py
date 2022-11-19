import pygame
import random
import time
import sys
#Colours
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

#Game initializer
def game_init(info_bar_p,width_p,hight_p,wp_p,hp_p,tm_p,fill_speed_p):
	global info_bar,width,hight,wp,hp,rw,rh,tm,screen,clock,fill_speed
	pygame.init()
	info_bar = info_bar_p
	width = width_p
	hight = hight_p
	wp = wp_p # width proportion
	hp = hp_p # hight proportion
	rw = width_p/wp_p
	rh = hight_p/hp_p
	tm = tm_p # total amount of mines
	fill_speed = fill_speed_p
	screen = pygame.display.set_mode((width_p,hight_p+info_bar_p))
	screen.fill([74,117,44])
	pygame.display.set_caption("Minesweeper")
	clock = pygame.time.Clock()
game_init(50,500,400,10,8,10,0.01)

#Building grid function and restarting the game
def start_game():
	global info_bar,width,hight,wp,hp,rw,rh,tm,screen
	global flag_count
	global inner_grid
	global outer_grid
	global click
	click = 0
	flag_count = tm
	mines_list,not_mines_list = [],[]
	for i in range(tm):
		mines_list.append(['mine','NoFlag','close'])
	for i in range(wp*hp-tm):
		not_mines_list.append([0,'NoFlag','close'])
	mine_placing_list = mines_list+not_mines_list
	random.shuffle(mine_placing_list)
	b = ['=','NoFlag','close'] # border 
	outer_grid = [[b]*(wp+2)]+[[b]+mine_placing_list[i*wp:(i+1)*wp]+[b] for i in range(hp)]+[[b]*(wp+2)]
	inner_grid = [mine_placing_list[i*wp:(i+1)*wp] for i in range(hp)]
	def mine_counter(x,y,g=outer_grid): # function for counting mines around node
		mines = 0
		for i in range(y,y+3):
			for j in range(x,x+3):
				if outer_grid[i][j][0] == 'mine':
					mines += 1
		return mines
	for u in range(hp):
		for v in range(wp):
			if inner_grid[u][v][0] != 'mine':
				inner_grid[u][v][0] = mine_counter(v,u)
start_game()

#Function for drawing chess pattern grid.
def surface_griding(c1,c2,speed=0):
	global info_bar,wp,hp,rw,rh,screen
	for y in range(hp):
		for x in range(wp):
			if speed:
				time.sleep(speed)
				pygame.display.update()
			pygame.draw.rect(screen,[c1,c2][int((x+y)%2==0)],pygame.Rect(x*rw,y*rh+info_bar,rw,rh))
surface_griding(light_front_colour,dark_front_colour)

#Function for setting flag sizes
def flag_init():
	global rw,rh
	global light_flag,dark_flag 
	light_flag = pygame.image.load("C:\\Users\\User\\Desktop\\repo\\minesweeper\\light_flag.png")
	light_flag = pygame.transform.scale(light_flag,(rw,rh))
	dark_flag = pygame.image.load("C:\\Users\\User\\Desktop\\repo\\minesweeper\\dark_flag.png")
	dark_flag = pygame.transform.scale(dark_flag,(rw,rh))
flag_init()

#Function for rendering flags
def render_flag(x,y):
	global info_bar,rw,rh,screen
	global inner_grid,outer_grid
	global light_flag,dark_flag
	if (x+y) % 2 == 0:
		screen.blit(dark_flag,(x*rw,y*rh+info_bar))
	else:
		screen.blit(light_flag,(x*rw,y*rh+info_bar))
	inner_grid[y][x][1] = 'Flag'

#Function for rendering square
def render_square(x,y,c1,c2):
	global info_bar,rw,rh,screen
	pygame.draw.rect(screen,[c1,c2][int((x+y)%2==0)],pygame.Rect(x*rw,y*rh+info_bar,rw,rh))

#Function for rendering numbers
def render_number(x,y,number):
	global info_bar,rw,rh,screen
	global inner_grid,outer_grid
	number_font = pygame.font.Font(None,int(rw))
	num = number_font.render(str(number),True,number_colours[number-1])
	render_square(x,y,light_back_colour,dark_back_colour)
	screen.blit(num,num.get_rect(center=((2*x+1)*rw/2,info_bar+(2*y+1)*rh/2)))
	inner_grid[y][x][2] = 'open'

#Function for rendering mine
def render_mine(x,y):
	global info_bar,rw,rh,screen
	global inner_grid,outer_grid
	mine_rect_colour = random.choice(mine_colours)
	mine_circle_colour = [i/2 for i in mine_rect_colour]
	pygame.draw.rect(screen,mine_rect_colour,pygame.Rect(x*rw,y*rh+info_bar,rw,rh))
	pygame.draw.circle(screen,mine_circle_colour,((2*x+1)*rw/2,info_bar+(2*y+1)*rh/2),int(rw/4))
	inner_grid[y][x][2] = 'open'

#Function for opening one square
def opender(x,y):
	global flag_count
	global inner_grid,outer_grid
	if inner_grid[y][x][0] == 'mine':
		inner_grid[y][x][2] = 'close'
		render_mine(x,y)
	elif inner_grid[y][x][0] == 0:
		if inner_grid[y][x][1] == 'Flag':
			flag_count += 1
		inner_grid[y][x][2] = 'open'
		render_square(x,y,light_back_colour,dark_back_colour)
	else:
		if inner_grid[y][x][1] == 'Flag':
			flag_count += 1
		render_number(x,y,inner_grid[y][x][0])
def chain_reaction(x,y): # chain reaction for opening empty square
	global flag_count
	global outer_grid
	for u in range(y,y+3):
		for v in range(x,x+3):
			if outer_grid[u][v][0] != 0 and outer_grid[u][v][2] == 'close' and outer_grid[u][v][0] != '=':
				opender(v-1,u-1)
			elif outer_grid[u][v][0] == 0 and outer_grid[u][v][2] == 'close':
				if outer_grid[u][v][1] == 'Flag':
					flag_count +=1
				outer_grid[u][v][2] = 'open'
				render_square(v-1,u-1,light_back_colour,dark_back_colour)
				chain_reaction(v-1,u-1)

#Function for mine explosion
def reveler():
	global wp,hp
	for u in range(hp):
		for v in range(wp):
			opender(v,u)

#Function for checking if game is over
def game_over_checker():
	global inner_grid
	g = [len([1 for j in i if j[2]=='close']) for i in inner_grid]
	return sum(g)

#Info bar
info_bar_flag = pygame.image.load("C:\\Users\\User\\Desktop\\repo\\minesweeper\\info_bar_flag.png")
info_bar_flag = pygame.transform.scale(info_bar_flag,(info_bar,info_bar))
screen.blit(info_bar_flag,(width/1.7,0))
info_bar_font = pygame.font.SysFont(None,int(info_bar/1.1))

#Function for counting flags
def flag_count_update(f):
	global info_bar,width,hight
	pygame.draw.rect(screen,(74,117,44),pygame.Rect(width/1.4,info_bar/10,info_bar*2,info_bar/1.2))
	flags = info_bar_font.render(str(f),True,(50,50,50))
	screen.blit(flags,(width/1.4,info_bar/5))
flag_count_update(flag_count)

#Function for initializing level buttons
def level_init():
	global info_bar,screen
	global easy_rect,medium_rect,hard_rect
	level_font = pygame.font.SysFont(None,int(info_bar/2.5))
	easy_rect = pygame.draw.rect(screen,(0,0,0),(0,0,info_bar*1.5,info_bar/2),2,2)
	easy_text = level_font.render('Easy',True,'black')
	medium_rect = pygame.draw.rect(screen,(0,0,0),(info_bar*1.5,0,info_bar*1.5,info_bar/2),2,2)
	medium_text = level_font.render('Medium',True,'black')
	hard_rect= pygame.draw.rect(screen,(0,0,0),(info_bar*3,0,info_bar*1.5,info_bar/2),2,2)
	hard_text = level_font.render('Hard',True,'black')
	screen.blit(easy_text,easy_text.get_rect(center=easy_rect.center))
	screen.blit(medium_text,medium_text.get_rect(center=medium_rect.center))
	screen.blit(hard_text,hard_text.get_rect(center=hard_rect.center))
	level_font = pygame.font.SysFont(None,int(info_bar/2.5))
level_init()

#Main loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if game_over_checker() == tm or click == 2:
			start_game()
			flag_count_update(tm)
			surface_griding(light_front_colour,dark_front_colour,speed=fill_speed)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			x = int(pygame.mouse.get_pos()[0]//rw)
			y = int((pygame.mouse.get_pos()[1]-info_bar)//rh)
			if easy_rect.collidepoint(pygame.mouse.get_pos()):
				pygame.display.quit()
				game_init(50,500,400,10,8,10,0.01)
				flag_init()
				level_init()
				start_game()
				flag_count_update(flag_count)
				screen.blit(info_bar_flag,(width/1.7,0))
				surface_griding(light_front_colour,dark_front_colour)
			elif medium_rect.collidepoint(pygame.mouse.get_pos()):
				pygame.display.quit()
				game_init(50,720,560,18,14,40,0.0000001)
				flag_init()
				level_init()
				start_game()
				flag_count_update(flag_count)
				screen.blit(info_bar_flag,(width/1.7,0))
				surface_griding(light_front_colour,dark_front_colour)
			elif hard_rect.collidepoint(pygame.mouse.get_pos()):
				pygame.display.quit()
				game_init(50,720,600,24,20,70,0.0000001)
				flag_init()
				level_init()
				start_game()
				flag_count_update(flag_count)
				screen.blit(info_bar_flag,(width/1.7,0))
				surface_griding(light_front_colour,dark_front_colour)
			elif event.button == 1 and y>=0:
					if inner_grid[y][x][1] == 'NoFlag':
						if inner_grid[y][x][0] == 'mine':
							click += 1
							reveler()
							flag_count_update(tm)
						elif inner_grid[y][x][0] == 0:
							chain_reaction(x,y)
							flag_count_update(flag_count)
						else:
							opender(x,y)
					elif inner_grid[y][x][1] == 'Flag':
						render_square(x,y,light_front_colour,dark_front_colour)
						inner_grid[y][x][1] = 'NoFlag'
						flag_count += 1
						flag_count_update(flag_count)
			elif event.button == 3 and y>=0:
				if inner_grid[y][x][1] == 'Flag':
					render_square(x,y,light_front_colour,dark_front_colour)
					inner_grid[y][x][1] = 'NoFlag'
					flag_count += 1
					flag_count_update(flag_count)
				elif inner_grid[y][x][1] == 'NoFlag'and inner_grid[y][x][2] == 'close':
					render_flag(x,y)
					inner_grid[y][x][1] = 'Flag'
					flag_count -= 1
					flag_count_update(flag_count)
	pygame.display.update()
	clock.tick(100)