# -*- coding: utf-8 -*-

import math
import random

import Settings
import ShipTypes
import Objects
import Weapons

class Ship(Objects.Object):
	def init(self):
		self.size = 7
		self.explosionSizeFactor = 1.5
		self.explosionParticleFactor = 5

		self.lastHitter = None

		self.airResistance = 10

		self.thrust = False
		self.rotation = 0

		self.disruption = 0

		self.isSprite = True
		self.isShip = True
		self.floats = True
		self.colorize = True

		self.resetWeapons()

	def setShipType(self, shipType): # Load the specific ship
		self.shipModel = eval("ShipTypes." + shipType)()

		self.shipModel.hp = (13*self.shipModel.strength+60)*(Settings.settings["Rules"]["shipstrength"]/100.0)
		self.shipModel.acceleration = 0.009*self.shipModel.acceleration+0.055
		self.shipModel.loadingSpeed = 15*self.shipModel.loadingSpeed+40

		self.sprite(self.shipModel.image)

	def spawn(self): # Respawn the ship
		self.randomizeLocation(self.game.map)

		self.dx = 0
		self.dy = 0
		self.angle = 3*math.pi/2

		self.thrust = False
		self.rotation = 0

		self.disruption = 0

		self.active = True

		self.hp = self.shipModel.hp
		self.acceleration = self.shipModel.acceleration
		self.loadingSpeed = self.shipModel.loadingSpeed

	def resetWeapons(self):
		if Settings.settings["Rules"]["insta"]:
			self.lightWeapon = Weapons.InstaGun(self.game)
			self.heavyWeapon = Weapons.Reverse(self.game)
		else:
			self.lightWeapon = eval("Weapons." + Settings.settings["Weapons"]["light"][random.randint(0,len(Settings.settings["Weapons"]["light"])-1)])(self.game)
			self.heavyWeapon = eval("Weapons." + Settings.settings["Weapons"]["heavy"][random.randint(0,len(Settings.settings["Weapons"]["heavy"])-1)])(self.game)

	def draw(self, map): # Drawing
		if self.thrust:
			if random.uniform(0,1) < 0.5:
				self.game.objects.append(Objects.ThrustFlame(self.game, self.owner, self.x-2*self.dx-12*math.cos(self.angle), self.y-2*self.dy-12*math.sin(self.angle), self.dx-1*math.cos(self.angle), self.dy-1*math.sin(self.angle)))

		if self.hp < self.shipModel.hp/6:
			if random.uniform(0,1) < 0.2:
				self.game.objects.append(Objects.Smoke(self.game, self.owner, self.x, self.y))

		self.spriteDraw(map)
		self.redraw(map, self.size)

	def destroy(self, map): # Destroy the ship
		if self.active:
			self.active = False

	def check(self, map): # Check for actions
		self.rotate = self.rotation

		if self.hp < self.shipModel.hp/6:
			self.hp -= self.shipModel.hp/10000.0

		if self.disruption > 0:
			self.disruption -= 1

		self.lightWeapon.check(self)
		self.heavyWeapon.check(self)

	def onGroundHit(self,map,x,y):
		pixel = map.mask[x][y]
		if pixel == map.maskimage.map_rgb((150,90,20,255)): # Dirt
			self.dx -= self.dx/5
			self.dy -= self.dy/5 + 0.02
		elif pixel == map.maskimage.map_rgb((255,0,0,255)): # Insta death area
			self.explode(map)
		else:
			if self.y-self.oldy != 0 or self.x-self.oldx != 0:
				impact = 5*math.sqrt(self.dx**2 + self.dy**2)
				if impact > 5:
					self.hp -= impact
			self.dx = 0
			self.dy = 0

	def onBorderHit(self,map,x,y): # Stop the ship when colliding with map border
		self.dx = 0
		self.dy = 0
