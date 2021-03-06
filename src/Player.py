# -*- coding: utf-8 -*-

import pygame
import random

import Settings
import PlayerMenus
import Ship

class Player:
	def __init__(self, game, keys, name, color):

		self.game = game
		self.keys = keys
		self.name = name
		self.color = color

		self.lives = Settings.settings["Rules"]["lives"]
		self.kills = 0

		self.active = True
		self.winner = False

		self.shoot1 = False
		self.shoot2 = False

		self.respawnWait = 125

		self.menuStage = 1
		self.menu = PlayerMenus.shipChooser()

	def menuCheck(self): # Check menu actions
		if self.menuStage == 1:
			if self.menu.done:
				self.menuStage = 0
				self.shipType = self.menu.ship
				del self.menu

	def menuDraw(self, i):
		self.menu.draw(self.game.engine, self.keys, i)

	def createShip(self): # Create a ship
		self.spawnMessage = True
		self.ship = Ship.Ship(self.game, self, 0,0,0,0, self.color)
		self.ship.setShipType(self.shipType)
		self.ship.active = False
		self.game.objects.append(self.ship)

	def check(self, game): # Check events
		if self.lives > 0:
			if not(self.ship.active):
				if self.respawnWait <= 0:
					self.respawnWait = 150
					self.spawnMessage = False

					self.ship.spawn()
				else:
					self.respawnWait -= 1

					if self.respawnWait == 149:
						self.lives -= 1

						if self == self.ship.lastHitter:
							self.game.engine.messageBox.addMessage(self.name + " killed himself.")
						else:
							try:
								self.ship.lastHitter.kills += 1
								self.game.engine.messageBox.addMessage(self.name + " was killed by " + self.ship.lastHitter.name + ".")
							except AttributeError:
								self.game.engine.messageBox.addMessage(self.name + " died. ")

						self.ship.lastHitter = None

						self.spawnMessage = True
						self.shoot1 = False
						self.shoot2 = False
						if Settings.settings["Rules"]["resetweaponsondeath"]:
							self.ship.resetWeapons()

			else:
				self.shoot()
		elif self.active:
			self.active = False
			self.spawnMessage = False
			self.game.engine.messageBox.addMessage(self.name + " is out!")

	def shoot(self):
		if self.shoot1: # Light weapon
			self.ship.lightWeapon.activate(self.ship, self.game.engine)

		if self.shoot2: # Heavy weapon
			self.ship.heavyWeapon.activate(self.ship, self.game.engine)

	def drawHUD(self, map, i): # Draw the HUD
		if Settings.settings["Rules"]["playeramount"] == 3:
			if i == 0:
				i = 1
			elif i == 1:
				i = 0

		if self.ship.x-Settings.settings["Screen"]["width"]/(2*Settings.settings["Rules"]["playeramount"]) < 0 or Settings.settings["Screen"]["width"] > Settings.settings["Rules"]["playeramount"]*map.width:
			left = 0
		elif self.ship.x > map.width-Settings.settings["Screen"]["width"]/(2*Settings.settings["Rules"]["playeramount"]):
			left = map.width-Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]
		else:
			left = self.ship.x-Settings.settings["Screen"]["width"]/(2*Settings.settings["Rules"]["playeramount"])

		if Settings.settings["Screen"]["height"] > map.height:
			top = (map.height-(Settings.settings["Screen"]["height"]-20))/2
			self.game.engine.screen.fill((0,0,0),((i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"],0),(Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"],-top)))
		elif self.ship.y-(Settings.settings["Screen"]["height"]-20)/2 < 0:
			top = 0
		elif self.ship.y > map.height-(Settings.settings["Screen"]["height"]-20)/2:
			top = map.height-Settings.settings["Screen"]["height"]+20
		else:
			top = self.ship.y-(Settings.settings["Screen"]["height"]-20)/2

		if self.ship.disruption > 0:
			if random.randint(0,10) == 0:
				self.game.engine.screen.blit(map.screenImage, (int(i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]),0), ((int(left),int(top)), (Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+1,Settings.settings["Screen"]["height"]-20)))
		else:
			self.game.engine.screen.blit(map.screenImage, (int(i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]),0), ((int(left),int(top)), (Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+1,Settings.settings["Screen"]["height"]-20)))

		self.game.engine.screen.fill((0,0,0),((i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"],Settings.settings["Screen"]["height"]-20),(Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+1,20)))

		self.game.engine.screen.blit(self.ship.lightWeapon.image, (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+28,Settings.settings["Screen"]["height"]-19))
		self.game.engine.screen.blit(self.ship.heavyWeapon.image, (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+48,Settings.settings["Screen"]["height"]-19))

		self.game.engine.screen.blit(self.game.engine.text4.render(str(self.kills) + " / " + str(self.lives), True, (0,255,0)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+3,Settings.settings["Screen"]["height"]-17))

		if self.ship.active:
			if self.ship.hp > self.ship.shipModel.hp/2:
				hpcolor = (0,255,0)
			elif self.ship.hp > self.ship.shipModel.hp/6:
				hpcolor = (255,255,0)
			else:
				hpcolor = (255,0,0)
			pygame.draw.rect(self.game.engine.screen, hpcolor, ((i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+70,Settings.settings["Screen"]["height"]-7),(int((self.ship.hp/self.ship.shipModel.hp)*(Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]-70)),7)))

			for a,weapon in enumerate((self.ship.lightWeapon, self.ship.heavyWeapon)):
				if weapon.loaded >= 100 or not(weapon.loading):
					loadColor = (0,0,255)
				else:
					loadColor = (0,255,255)

				pygame.draw.rect(self.game.engine.screen, loadColor, ((i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+70,Settings.settings["Screen"]["height"]-19+a*6),(int(((weapon.loaded)/100)*(Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]-70)),5)))

		if i > 0:
			if Settings.settings["Rules"]["playeramount"] == 3 and i == 2:
				pygame.draw.line(self.game.engine.screen, (0,0,0), (int((i-1)*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]),0), (int((i-1)*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]),Settings.settings["Screen"]["height"]))
			pygame.draw.line(self.game.engine.screen, (0,0,0), (int(i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]),0), (int(i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]),Settings.settings["Screen"]["height"]))

		if self.spawnMessage and not(self.winner):
			self.game.engine.screen.blit(self.game.engine.text.render("Spawning with " + str(self.ship.lightWeapon.name) + " and " + str(self.ship.heavyWeapon.name), True, (255,0,0)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+50,50))
			if self.lives > 1:
				self.game.engine.screen.blit(self.game.engine.text.render(str(self.lives) + " lives left.", True, (0,255,0)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+50,70))
			else:
				self.game.engine.screen.blit(self.game.engine.text.render("You got no extra lives!", True, (0,255,0)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+50,70))

		if not(self.active):
			self.game.engine.screen.blit(self.game.engine.text.render("You are out!", True, (255,0,0)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+50,50))
		elif self.winner:
			self.game.engine.screen.blit(self.game.engine.text2.render("You are the winner!", True, (0,255,0)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+50,50))
			self.game.engine.screen.blit(self.game.engine.text.render("Press ESCAPE to continue...", True, (0,255,255)), (i*Settings.settings["Screen"]["width"]/Settings.settings["Rules"]["playeramount"]+70,100))

	def event(self, event): # Take keyboard events
		if self.game.inMenu:
			if self.menuStage > 0:
				self.menu.event(event, self.keys)
		else:
			if event.type == pygame.KEYDOWN and event.key == self.keys["thrust"]:
				self.ship.thrust = True
			elif event.type == pygame.KEYUP and event.key == self.keys["thrust"]:
				self.ship.thrust = False
			elif event.type == pygame.KEYDOWN and event.key == self.keys["rotate1"]:
				self.ship.rotation = -1
			elif event.type == pygame.KEYUP and event.key == self.keys["rotate1"] and self.ship.rotation == -1:
				self.ship.rotation = 0
			elif event.type == pygame.KEYDOWN and event.key == self.keys["rotate2"]:
				self.ship.rotation = 1
			elif event.type == pygame.KEYUP and event.key == self.keys["rotate2"] and self.ship.rotation == 1:
				self.ship.rotation = 0
			elif event.type == pygame.KEYDOWN and event.key == self.keys["shoot1"]:
				self.shoot1 = True
			elif event.type == pygame.KEYUP and event.key == self.keys["shoot1"]:
				self.shoot1 = False
			elif event.type == pygame.KEYDOWN and event.key == self.keys["shoot2"]:
				self.shoot2 = True
			elif event.type == pygame.KEYUP and event.key == self.keys["shoot2"]:
				self.shoot2 = False
