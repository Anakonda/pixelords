# -*- coding: utf-8 -*-

import pygame

import Settings
import Functions
import ShipTypes

class playerMenu:
	def __init__(self):
		self.done = False
		self.init()

	def draw(self, game, i): # Draw the menu
		pass

	def event(self, event, keys): # Take keyboard events
		pass

class shipChooser(playerMenu):
	def init(self):
		self.shipNum = 0

	def event(self, event, keys):
		if event.type == pygame.KEYDOWN and event.key == keys["shoot1"]:
			self.ship = Settings.settings["Ships"][self.shipNum]
			self.done = True
		elif event.type == pygame.KEYDOWN and event.key == keys["rotate1"]:
			if self.shipNum > 0:
				self.shipNum -= 1
			else:
				self.shipNum = len(Settings.settings["Ships"])-1
		elif event.type == pygame.KEYDOWN and event.key == keys["rotate2"]:
			if self.shipNum < len(Settings.settings["Ships"])-1:
				self.shipNum += 1
			else:
				self.shipNum = 0

	def draw(self, game, keys, i):
		if Settings.settings["Rules"]["playeramount"] == 3:
			if i == 0:
				i = 1
			elif i == 1:
				i = 0

		game.screen.fill((0,0,0), ((i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"],0),(Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"],Settings.settings["Screen"]["height"])))

		game.screen.blit(pygame.transform.scale(pygame.image.load(Functions.gfxPath(eval("ShipTypes." + Settings.settings["Ships"][self.shipNum])().image)), (200,150)),(i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+25,25))

		game.screen.blit(game.text2.render(eval("ShipTypes." + Settings.settings["Ships"][self.shipNum])().name, True, (0,255,0)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+25,190))

		game.screen.blit(game.text.render("Strength:", True, (255,255,255)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+50,245))
		for x in range(eval("ShipTypes." + Settings.settings["Ships"][self.shipNum])().strength):
			pygame.draw.rect(game.screen, (255,0,0), ((i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+x*15+75,270),(10,20)))

		game.screen.blit(game.text.render("Acceleration:", True, (255,255,255)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+50,295))
		for x in range(eval("ShipTypes." + Settings.settings["Ships"][self.shipNum])().acceleration):
			pygame.draw.rect(game.screen, (255,0,0), ((i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+x*15+75,320),(10,20)))

		game.screen.blit(game.text.render("Loading speed:", True, (255,255,255)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+50,345))
		for x in range(eval("ShipTypes." + Settings.settings["Ships"][self.shipNum])().loadingSpeed):
			pygame.draw.rect(game.screen, (255,0,0), ((i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+x*15+75,370),(10,20)))

		game.screen.blit(game.text3.render("Controls:", True, (0,255,0)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+25,400))

		game.screen.blit(game.text.render("Shoot / Select (menu)", True, (255,255,255)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+50,440))
		game.screen.blit(game.text.render(pygame.key.name(keys["shoot1"]).upper(), True, (255,0,0)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+75,460))

		game.screen.blit(game.text.render("Steer / Change item (menu)", True, (255,255,255)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+50,480))
		game.screen.blit(game.text.render(pygame.key.name(keys["rotate1"]).upper() + " + " + pygame.key.name(keys["rotate2"]).upper(), True, (255,0,0)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+75,500))

		game.screen.blit(game.text.render("Thrust", True, (255,255,255)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+50,520))
		game.screen.blit(game.text.render(pygame.key.name(keys["thrust"]).upper(), True, (255,0,0)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+75,540))

		game.screen.blit(game.text.render("Shoot heavy weapon", True, (255,255,255)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+50,560))
		game.screen.blit(game.text.render(pygame.key.name(keys["shoot2"]).upper(), True, (255,0,0)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+75,580))

		if self.done:
			game.screen.blit(game.text2.render("Ready!", True, (0,255,255)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+60,25))
