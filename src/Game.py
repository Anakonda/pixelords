# -*- coding: utf-8 -*-

import pygame
import os
import random

import Settings
import Functions
import Objects
import Player

class Game:
	def __init__(self, engine):
		self.gameOver = False
		self.engine = engine

		pygame.mouse.set_visible(False)
		self.engine.inGame = True

		self.map = Map()

		self.objects = []
		self.players = []

		for i in range(Settings.playerAmount-1,-1,-1):
			self.players.append(Player.Player(self, Settings.keys[i], Settings.names[i], Settings.colors[i]))

		self.bonusTimer = Settings.bonusDelay

		self.run()

	def event(self): # Handle keyboard events
		for event in pygame.event.get():
			self.engine.globalEvent(event)

			# Menu keys:
			if self.inMenu:
				if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					self.running = False
				elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
					for player in self.players:
						player.event(event)

			# In-game keys
			else:
				if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					self.running = False
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_F10:
					path = os.path.join("maps", "saved")
					try:
						os.mkdir(path)
					except:
						pass
					pygame.image.save(self.map.mask.make_surface(), os.path.join(path, "mask.png"))
					pygame.image.save(self.map.visual, os.path.join(path, "visual.png"))
					pygame.image.save(self.map.background.make_surface(), os.path.join(path, "background.png"))
					self.engine.messageBox.addMessage("Current map saved to " + path + ".")
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
					path = Functions.saveNameIncrement("screenshots", "fullmap", "png")
					pygame.image.save(self.map.screenImage, path)
					self.engine.messageBox.addMessage("Screenshot saved to " + path + ".")
				elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and not(self.gameOver):
					for player in self.players:
						if player.ship.active:
							player.event(event)

	def checkBonusSpawn(self): # Check spawn timer for repair kits and weapon changers
		if Settings.bonusDelay > 0:
			if self.bonusTimer <= 0:
				self.bonusTimer = Settings.bonusDelay
				if random.randint(0,1):
					self.objects.append(Objects.RepairKit(self, None, self.engine))
					self.engine.messageBox.addMessage("Repair kit spawned.")
				else:
					self.objects.append(Objects.WeaponChanger(self, None, self.engine))
					self.engine.messageBox.addMessage("Weapon changer spawned.")
			else:
				self.bonusTimer -= 1

	def run(self): # Main loop
		self.running = True
		self.inMenu = True

		while self.running:
			if self.inMenu:
				menuPlayers = Settings.playerAmount
				for i,player in enumerate(self.players):
					if player.menuStage == 0:
						menuPlayers -= 1
					else:
						player.menuDraw(i)
					player.menuCheck()
				if menuPlayers <= 0:
					self.inMenu = False
					self.engine.screen.fill((0,0,0), ((0,0),(Settings.width,Settings.height)))

					self.engine.messageBox.addMessage("Round started!")

					for player in self.players:
						player.createShip()
			else:
				self.map.water(self.engine)
				for object in self.objects: # Process objects
					object.run(self.map)

				if not(self.gameOver):
					activePlayers = Settings.playerAmount
					killLimitReached = False

					for player in self.players:
						if not(player.active):
							activePlayers -= 1
						if player.kills >= Settings.killLimit:
							killLimitReached = True
							self.engine.messageBox.addMessage(player.name + " reached the kill limit!")

						player.check(self)

					if not(Settings.insta):
						self.checkBonusSpawn()

					if activePlayers < 2 or killLimitReached:
						self.gameOver = True
						for i,player in enumerate(self.players):
							if killLimitReached and player.kills < Settings.killLimit:
								player.ship.explode(self.map)
							elif player.active:
								player.winner = True
								self.engine.messageBox.addMessage(player.name + " is the winner!")

								player.ship.thrust = False
								player.ship.rotate = 0

				for i,player2 in enumerate(self.players): # Draw screens for each player
					player2.drawHUD(self.map, i)

			self.engine.messageBox.draw(self.engine)
			self.engine.infoOverlay.draw(self.engine)

			self.event()

			if Settings.showFPS:
				self.engine.screen.blit(self.engine.text.render(str(int(self.engine.clock.get_fps())), True, (255,0,0)), (Settings.width-40,10))

			if Settings.scale != 1:
				self.engine.scale()

			# Redraw the screen
			pygame.display.update()
			self.map.draw()

			if self.inMenu:
				self.engine.clock.tick(20)
			else:
				self.engine.clock.tick(60)

class Map:
	def __init__(self): # Load the map
		tempvisual = pygame.image.load(os.path.join("maps",Settings.map,"visual.png")).convert_alpha()
		self.maskimage = pygame.image.load(os.path.join("maps",Settings.map,"mask.png")).convert()
		self.mask = pygame.PixelArray(self.maskimage)
		self.backgroundimage = pygame.image.load(os.path.join("maps",Settings.map,"background.jpg")).convert()
		self.background = pygame.PixelArray(self.backgroundimage)

		self.width = self.maskimage.get_width()
		self.height = self.maskimage.get_height()

		self.visual = self.backgroundimage.convert()
		self.visual.blit(tempvisual, (0,0))

		self.screenImage = self.visual.convert()

		self.redrawAreas = []
		self.waters = []
		self.waterId = 0
		self.waterRandomizeDelay = 0

		waterColor = self.maskimage.map_rgb((0,0,255,255))
		for x in range(0,self.width):
			for y in range(0,self.height):
				if self.mask[x][y] == waterColor:
					self.waters.append((x,y))

	def draw(self): # Draw screenImage
		for area in self.redrawAreas:
			self.screenImage.blit(self.visual, area[0], (area[0], area[1]))
		self.redrawAreas = []

	def redraw(self, start, end): # Collect areas that need redrawing
		self.redrawAreas.append((start, end))

	def water(self, engine):
		if Settings.waterSpeed > 0:
			if self.waterRandomizeDelay == 0:
				self.waterRandomizeDelay = 200
				random.shuffle(self.waters)
				"""if Settings.waterSpeed > 25 and engine.clock.get_fps() < 50:
					Settings.waterSpeed -= Settings.waterSpeed/20
					engine.messageBox.addMessage("Decreasing water speed for better performance (" + str(Settings.waterSpeed) + ")")"""
			else:
				self.waterRandomizeDelay -= 1
			emptyColor = self.maskimage.map_rgb((0,0,0,255))
			if Settings.waterSpeed > len(self.waters):
				rounds = len(self.waters)
			else:
				rounds = Settings.waterSpeed
			for i in range(rounds):
				self.waterId += 1
				if self.waterId >= len(self.waters):
					self.waterId = 0
				water = self.waters[self.waterId]
				ox,oy = water
				if ox != None:
					x,y = (ox,oy)

					try:
						for repeat in range(2):
							if x < 0 or y < 0:
								raise IndexError
							mask2l = self.mask[x-1][y]
							mask2r = self.mask[x+1][y]
							mask2d = self.mask[x][y+1]
							if mask2d != emptyColor and mask2l == emptyColor and mask2r == emptyColor:
								if random.randint(0,1):
									x -= 1
								else:
									x += 1
							elif mask2l == emptyColor and mask2r != emptyColor:
								x -= 1
							elif mask2l != emptyColor and mask2r == emptyColor:
								x += 1

							if self.mask[x][y+1] == emptyColor:
								y += 1
					except IndexError:
						self.waters[self.waterId] = (None,None)
						backgroundColor = self.background[ox][oy]
						self.mask[ox][oy] = (0,0,0)
						self.visual.set_at((ox,oy),backgroundColor)
						self.screenImage.set_at((ox,oy), backgroundColor)
						self.waters[self.waterId] = (x,y)
					else:
						if x != ox or y != oy:
							visualColor = self.visual.get_at((ox,oy))
							backgroundColor = self.background[ox][oy]
							self.mask[ox][oy] = (0,0,0)
							self.mask[x][y] = (0,0,255)
							self.visual.set_at((ox,oy),backgroundColor)
							self.visual.set_at((x,y),visualColor)
							self.screenImage.set_at((ox,oy), backgroundColor)
							self.screenImage.set_at((x,y), visualColor)
							self.waters[self.waterId] = (x,y)
