#import libraries
import os
import random
import sys
import pygame
from pygame.locals import *
from pygame.constants import QUIT
from os import path

#window
length = 1600
height = 900
window = pygame.display.set_mode((length, height))
elevation = height * 0.8	
fps = 60

#import image
img={}
ground_image = "images/ground.png"
sky_image = "images/sky.png"
plane_image = "images/plane.png"
building_image = "images/building.png"

#import sound
pygame.init()
pygame.mixer.init()
game_folder= path.dirname(__file__)
sounds_folder= path.join(game_folder, "sounds")
explode_sound= pygame.mixer.Sound(os.path.join(sounds_folder, "explode.wav"))
point_sound= pygame.mixer.Sound(os.path.join(sounds_folder, "point.wav"))
bgm_sound= pygame.mixer.music.load(os.path.join(sounds_folder, "bgm.wav"))
bgm_sound= pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

def planegame():
	your_score = 0
	vertical = int(length/5)
	horizontal = int(height/2)
	ground = 0
	mytempheight = 100

	# Generating two buildings for blitting on window
	first_building =createBuilding()
	second_building =createBuilding()

	# List containing lower buildings
	down_buildings = [
		{'x': length+300-mytempheight,
		'y': first_building[1]['y']},
		{'x': length+300-mytempheight+(length/2),
		'y': second_building[1]['y']},
	]

	# List Containing upper buildings
	up_buildings = [
		{'x': length+300-mytempheight,
		'y': first_building[0]['y']},
		{'x': length+200-mytempheight+(length/2),
		'y': second_building[0]['y']},
	]

	# building speed along x
	BuildingSpeed = -4

	# plane speed
	plane_speed_y = -9
	plane_Max_Speed_Y = 10
	plane_Min_Speed_Y = -8
	planeAccY = 1

	plane_boost_speed = -8
	plane_boosted = False
	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
				if vertical > 0:
					plane_speed_y = plane_boost_speed
					plane_boosted = True

		# This function will return true
		# if the plane is crashed
		game_over = isGameOver(horizontal,
							vertical,
							up_buildings,
							down_buildings)
			
		if game_over:
			explode_sound.play()
			
			return

		# Score
		playerMidPos = horizontal + img['plane'].get_width()/2
		for buildings in up_buildings:
			buildingsMidPos = buildings['x'] + img['building'][0].get_width()/2
			if buildingsMidPos <= playerMidPos < buildingsMidPos + 4:
				pygame.mixer.Sound.play(point_sound)
				your_score += 1
				print(f"Your your_score is {your_score}")

		if plane_speed_y < plane_Max_Speed_Y and not plane_boosted:
			plane_speed_y += planeAccY

		if plane_boosted:
			plane_boosted = False
		playerHeight = img['plane'].get_height()
		vertical = vertical + \
			min(plane_speed_y, elevation - vertical - playerHeight)

		# move buildingss from right to the left
		for upperbuildings, lowerbuildings in zip(up_buildings, down_buildings):
			upperbuildings['x'] += BuildingSpeed
			lowerbuildings['x'] += BuildingSpeed

		# Add new buildings
		if 0 < up_buildings[0]['x'] < 5:
			newBuilding =createBuilding()
			up_buildings.append(newBuilding[0])
			down_buildings.append(newBuilding[1])

		# Remove building that out of frame
		if up_buildings[0]['x'] < -img['building'][0].get_width():
			up_buildings.pop(0)
			down_buildings.pop(0)

		# Games images blit
		window.blit(img['sky'], (0, 0))
		for upperbuildings, lowerbuildings in zip(up_buildings, down_buildings):
			window.blit(img['building'][0],
						(upperbuildings['x'], upperbuildings['y']))
			window.blit(img['building'][1],
						(lowerbuildings['x'], lowerbuildings['y']))

		window.blit(img['ground'], (ground, elevation))
		window.blit(img['plane'], (horizontal, vertical))

	    # Fetching the digits of score.
		numbers = [int(x) for x in list(str(your_score))]
		width = 0

		# finding the width of score images from numbers.
		for num in numbers:
			width += img['scoreimages'][num].get_width()
		Xoffset = (length - width)/1.1

		# Blitting the images on the window.
		for num in numbers:
			window.blit(img['scoreimages'][num],
						(Xoffset, length*0.02))
			Xoffset += img['scoreimages'][num].get_width()

		# Refreshing the game window and displaying the score.
		pygame.display.update()
		fps_clock.tick(fps)


def isGameOver(horizontal, vertical, up_buildings, down_buildings):
	if vertical > elevation - 25 or vertical < 0:
		return True

	for buildings in up_buildings:
		buildingsHeight = img['building'][0].get_height()
		if(vertical < buildingsHeight + buildings['y'] and\
		abs(horizontal - buildings['x']) < img['building'][0].get_width()):
			return True

	for buildings in down_buildings:
		if (vertical + img['plane'].get_height() > buildings['y']) and\
		abs(horizontal - buildings['x']) < img['building'][0].get_width():
			return True
	return False


def createBuilding():
	offset = height/3
	buildingsHeight = img['building'][0].get_height()
	y2 = offset + \
		random.randrange(
			0, int(height - img['ground'].get_height() - 1.2 * offset))
	buildingsX = length + 10
	y1 = buildingsHeight - y2 + offset
	buildings = [
		# upper buildings
		{'x': buildingsX, 'y': -y1},

		# lower buildings
		{'x': buildingsX, 'y': y2}
	]
	return buildings

if __name__ == "__main__":
    pygame.init()
    fps_clock=pygame.time.Clock()

    #Title for the game
    pygame.display.set_caption("Plany Plane")

    #images for score
    img["scoreimages"] = (
        pygame.image.load("images/0.png").convert_alpha(),
        pygame.image.load("images/1.png").convert_alpha(),
        pygame.image.load("images/2.png").convert_alpha(),
        pygame.image.load("images/3.png").convert_alpha(),
        pygame.image.load("images/4.png").convert_alpha(),        
        pygame.image.load("images/5.png").convert_alpha(),
        pygame.image.load("images/6.png").convert_alpha(),
        pygame.image.load("images/7.png").convert_alpha(),
        pygame.image.load("images/8.png").convert_alpha(),
        pygame.image.load("images/9.png").convert_alpha()
    )
    img["plane"] = pygame.image.load(plane_image).convert_alpha()                
    img["ground"] = pygame.image.load(ground_image).convert_alpha()
    img["sky"] = pygame.image.load(sky_image).convert_alpha()
    img["building"] = (pygame.transform.rotate(pygame.image.load(building_image).convert_alpha(),180),pygame.image.load(building_image).convert_alpha())

    #Main Menu
    print("HI PILOT")
    print("Press Space to start the game")

    #Plane positioning
    while True:
        horizontal = int(length/3)
        vertical = int((height - img["plane"].get_height())/2)

        #Ground
        ground = 0
        while True:
            for event in pygame.event.get():
                
                #Closing the game
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                #Starting the game
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    planegame()

                #AFK
                else:
                    window.blit(img["sky"],(0,0))
                    window.blit(img["plane"],(horizontal, vertical))
                    window.blit(img["ground"],(ground, elevation))
                    pygame.display.update()
                    fps_clock.tick(fps)