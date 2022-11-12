import pygame
import random
import time
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
width = 500
hight = 500
wp = 10 # width proportion
hp = 10 # hight proportion
rw = width/wp
rh = hight/hp
screen = pygame.display.set_mode((width,hight+info_bar))
screen.fill([74,117,44])
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

#Function for drawing chess pattern grid.
def surface_griding(c1,c2,speed=0):
	for y in range(hp):
		for x in range(wp):
			if speed:
				time.sleep(speed)
				pygame.display.update()
			pygame.draw.rect(screen,[c1,c2][int((x+y)%2==0)],pygame.Rect(x*rw,y*rh+info_bar,rw,rh))
# surface_griding(light_back_colour,dark_back_colour)
# surface_griding(light_front_colour,dark_front_colour,speed=0.01)
#Flags
light_flag = pygame.image.load("C:\\Users\\User\\Desktop\\repo\\minesweeper\\light_flag.png")
light_flag = pygame.transform.scale(light_flag,(rw,rh))
dark_flag = pygame.image.load("C:\\Users\\User\\Desktop\\repo\\minesweeper\\dark_flag.png")
dark_flag = pygame.transform.scale(dark_flag,(rw,rh))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
	pygame.display.update()
	clock.tick(30)