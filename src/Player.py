# -*- coding: utf-8 -*-

import pygame
import random

import Settings
import PlayerMenus
import Objects
import Ship

class Player:
	def __init__(self, game, keys, name, color):

		self.game = game
		self.keys = keys
		self.name = name
		self.color = color

		self.lives = Settings.lives
		self.kills = 0

		self.active = True
		self.winner = False

		self.shoot1 = False
		self.shoot2 = False

		self.respawnWait = 200

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
					self.respawnWait = 300
					self.spawnMessage = False

					self.ship.spawn()
				else:
					self.respawnWait -= 1

					if self.respawnWait == 299:
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
		if Settings.playerAmount == 3:
			if i == 0:
				i = 1
			elif i == 1:
				i = 0

		if self.ship.x-Settings.width/(2*Settings.playerAmount) < 0 or Settings.width > Settings.playerAmount*map.width:
			left = 0
		elif self.ship.x > map.width-Settings.width/(2*Settings.playerAmount):
			left = map.width-Settings.width/Settings.playerAmount
		else:
			left = self.ship.x-Settings.width/(2*Settings.playerAmount)

		if Settings.height > map.height:
			top = (map.height-(Settings.height-20))/2
			self.game.screen.fill((0,0,0),((i*Settings.width/Settings.playerAmount,0),(Settings.width/Settings.playerAmount,-top)))
		elif self.ship.y-(Settings.height-20)/2 < 0:
			top = 0
		elif self.ship.y > map.height-(Settings.height-20)/2:
			top = map.height-Settings.height+20
		else:
			top = self.ship.y-(Settings.height-20)/2

		if self.ship.disruption > 0:
			if random.randint(0,10) == 0:
				self.game.screen.blit(map.screenImage, (int(i*Settings.width/Settings.playerAmount),0), ((int(left),int(top)), (Settings.width/Settings.playerAmount+1,Settings.height-20)))
		else:
			self.game.engine.screen.blit(map.screenImage, (int(i*Settings.width/Settings.playerAmount),0), ((int(left),int(top)), (Settings.width/Settings.playerAmount+1,Settings.height-20)))

		self.game.engine.screen.fill((0,0,0),((i*Settings.width/Settings.playerAmount,Settings.height-20),(Settings.width/Settings.playerAmount+1,20)))

		self.game.engine.screen.blit(self.ship.lightWeapon.image, (i*Settings.width/Settings.playerAmount+28,Settings.height-19))
		self.game.engine.screen.blit(self.ship.heavyWeapon.image, (i*Settings.width/Settings.playerAmount+48,Settings.height-19))

		self.game.engine.screen.blit(self.game.engine.text4.render(str(self.kills) + " / " + str(self.lives), True, (0,255,0)), (i*Settings.width/Settings.playerAmount+3,Settings.height-17))

		if self.ship.active:
			if self.ship.hp > self.ship.shipModel.hp/2:
				hpcolor = (0,255,0)
			elif self.ship.hp > self.ship.shipModel.hp/6:
				hpcolor = (255,255,0)
			else:
				hpcolor = (255,0,0)
			pygame.draw.rect(self.game.engine.screen, hpcolor, ((i*Settings.width/Settings.playerAmount+70,Settings.height-7),(int((self.ship.hp/self.ship.shipModel.hp)*(Settings.width/Settings.playerAmount-70)),7)))

			for a,weapon in enumerate((self.ship.lightWeapon, self.ship.heavyWeapon)):
				if weapon.loaded >= 100 or not(weapon.loading):
					loadColor = (0,0,255)
				else:
					loadColor = (0,255,255)

				pygame.draw.rect(self.game.engine.screen, loadColor, ((i*Settings.width/Settings.playerAmount+70,Settings.height-19+a*6),(int(((weapon.loaded)/100)*(Settings.width/Settings.playerAmount-70)),5)))

		if i > 0:
			if Settings.playerAmount == 3 and i == 2:
				pygame.draw.line(self.game.engine.screen, (0,0,0), (int((i-1)*Settings.width/Settings.playerAmount),0), (int((i-1)*Settings.width/Settings.playerAmount),Settings.height))
			pygame.draw.line(self.game.engine.screen, (0,0,0), (int(i*Settings.width/Settings.playerAmount),0), (int(i*Settings.width/Settings.playerAmount),Settings.height))

		if self.spawnMessage and not(self.winner):
			self.game.engine.screen.blit(self.game.engine.text.render("Spawning with " + str(self.ship.lightWeapon.name) + " and " + str(self.ship.heavyWeapon.name), True, (255,0,0)), (i*Settings.width/Settings.playerAmount+50,50))
			if self.lives > 1:
				self.game.engine.screen.blit(self.game.engine.text.render(str(self.lives) + " lives left.", True, (0,255,0)), (i*Settings.width/Settings.playerAmount+50,70))
			else:
				self.game.engine.screen.blit(self.game.engine.text.render("You got no extra lives!", True, (0,255,0)), (i*Settings.width/Settings.playerAmount+50,70))

		if not(self.active):
			self.game.engine.screen.blit(self.game.engine.text.render("You are out!", True, (255,0,0)), (i*Settings.width/Settings.playerAmount+50,50))
		elif self.winner:
			self.game.engine.screen.blit(self.game.engine.text2.render("You are the winner!", True, (0,255,0)), (i*Settings.width/Settings.playerAmount+50,50))
			self.game.engine.screen.blit(self.game.engine.text.render("Press ESCAPE to continue...", True, (0,255,255)), (i*Settings.width/Settings.playerAmount+70,100))

	def event(self, event): # Take keyboard events
		if self.game.inMenu:
			if self.menuStage > 0:
				self.menu.event(event, self.keys)
		else:
			if event.type == pygame.KEYDOWN and event.key == self.keys[0]:
				self.ship.thrust = True
			elif event.type == pygame.KEYUP and event.key == self.keys[0]:
				self.ship.thrust = False
			elif event.type == pygame.KEYDOWN and event.key == self.keys[1]:
				self.ship.rotate = -1
			elif event.type == pygame.KEYUP and event.key == self.keys[1] and self.ship.rotate == -1:
				self.ship.rotate = 0
			elif event.type == pygame.KEYDOWN and event.key == self.keys[2]:
				self.ship.rotate = 1
			elif event.type == pygame.KEYUP and event.key == self.keys[2] and self.ship.rotate == 1:
				self.ship.rotate = 0
			elif event.type == pygame.KEYDOWN and event.key == self.keys[4]:
				self.shoot1 = True
			elif event.type == pygame.KEYUP and event.key == self.keys[4]:
				self.shoot1 = False
			elif event.type == pygame.KEYDOWN and event.key == self.keys[3]:
				self.shoot2 = True
			elif event.type == pygame.KEYUP and event.key == self.keys[3]:
				self.shoot2 = False
