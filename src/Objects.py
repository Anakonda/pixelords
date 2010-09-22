# -*- coding: utf-8 -*-

import pygame
import colorsys
import math
import random

import Settings
import Functions
import Sound
import Weapons

class Object(pygame.sprite.Sprite):
	def __init__(self, game, owner, x=0,y=0, dx=0,dy=0, color=(176,176,176,255)):
		self.game = game
		self.color = color
		self.owner = owner

		self.x = x
		self.y = y
		self.oldx = x
		self.oldy = y
		self.dx = dx
		self.dy = dy
		self.angle = -math.pi/2
		self.active = True

		self.color = color
		self.isSprite = False
		self.rotateWithSpeed = False
		self.colorize = False

		self.explosionCollision = True
		self.isShip = False

		self.hp = 2
		self.airResistance = 10
		self.gravity = True
		self.checkCollisions = True
		self.onGroundExplode = True
		self.onShipCollision = True
		self.onShipDamage = 0
		self.onShipExplode = True
		self.bounce = False
		self.hitsWater = False
		self.floats = False
		
		self.objectCollision = False
		self.objectCollisionDelay = 0
		self.objectCollisionExplode = False

		self.thrust = False
		self.rotate = 0

		self.init()

	def sprite(self, image): # Sprite creation
		self.isSprite = True

		pygame.sprite.Sprite.__init__(self)

		self.baseImage = pygame.image.load(Functions.gfxPath(image)).convert_alpha()
		self.image = self.baseImage
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)

		if self.colorize:
			for x in range(self.baseImage.get_width()):
				for y in range(self.baseImage.get_height()):
					ownhue = colorsys.rgb_to_hls(self.owner.color[0]/255.0, self.owner.color[1]/255.0, self.owner.color[2]/255.0)[0]
					color = colorsys.rgb_to_hls(self.baseImage.get_at((x,y))[0]/255.0, self.baseImage.get_at((x,y))[1]/255.0, self.baseImage.get_at((x,y))[2]/255.0)

					newcolor = colorsys.hls_to_rgb(ownhue, color[1], color[2])

					self.baseImage.set_at((x,y), (newcolor[0]*255, newcolor[1]*255, newcolor[2]*255, self.baseImage.get_at((x,y))[3]))

	def spriteDraw(self, map): # Sprite drawing
		if self.angle != 0:
			self.rect.center = (self.x, self.y)

			oldCenter = self.rect.center
			self.image = pygame.transform.rotate(self.baseImage, math.degrees(-self.angle+3*math.pi/2))
			self.rect = self.image.get_rect()
			self.rect.center = oldCenter

			self.redraw(map, self.rect.width/2)

			self.rect.center = (self.x, self.y)
			map.screenImage.blit(self.image, self.rect)

	def draw(self, map): # General drawing
		if self.isSprite:
			self.spriteDraw(map)
		else:
			pygame.draw.circle(map.screenImage, self.color, (int(self.x),int(self.y)), int(self.size))
			self.redraw(map, self.size)

	def redraw(self, map, size): # Redraw
		map.redraw((int(self.x-size-1),int(self.y-size-1)),(2*size+2,2*size+2))

	def run(self, map): # Process
		if self.active:
			if self.hp <= 0:
				self.explode(map)

			self.angle = Functions.returnAngle(self.angle)

			self.check(map)
			if self.active:
				if self.checkCollisions:
					self.collision(map)
				self.move()
				self.draw(map)

	def check(self,map): # Custom per-frame actions
		pass

	def onGroundHit(self,map,x,y): # Triggered on ground hit
		self.x = x
		self.y = y

		if self.bounce:
			size = 10

			xsum = 0
			ysum = 0
			points = 0

			if int(self.x+size) > map.width:
				right = map.width
			else:
				right = int(self.x+size)

			if int(self.x-size) < 0:
				left = 0
			else:
				left = int(self.x-size)

			for x in range(left, right):
				if (x-self.x)/(size+0.01) >= -1:
					for y in range(int((-math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y), int((math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y)):
						if y < map.height and y >= 0:
							maskValue = map.mask[x][y]
							if maskValue != map.maskimage.map_rgb((0,0,0, 255)):
								xsum += x
								ysum += y
								points += 1

			if points > 0 and points < 0.95*math.pi*size**2:
				hitx = float(xsum)/points
				hity = float(ysum)/points

				if hitx-self.x == 0 and hity-self.y != 0:
					normalAngle = math.pi/2
				elif hitx-self.x == 0 and hity-self.y == 0:
					normalAngle = None
				else:
					normalAngle = math.atan((hity-self.y)/(hitx-self.x))
			else:
				normalAngle = None

			if normalAngle != None:
				if self.dx == 0:
					collisionAngle = math.pi/2
				else:
					collisionAngle = math.atan(self.dy/self.dx)

				if Functions.returnAngle(normalAngle) < Functions.returnAngle(collisionAngle):
					if (self.dy > 0 and self.dx > 0) or (self.dy > 0 and self.dx < 0) or (self.dy < 0 and self.dx < 0):
						resultAngle = 2*normalAngle - collisionAngle
					else:
						resultAngle = 2*normalAngle - collisionAngle + math.pi
				else:
					if (self.dy < 0 and self.dx < 0) or (self.dy > 0 and self.dx < 0):
						resultAngle = 2*normalAngle - collisionAngle
					else:
						resultAngle = 2*normalAngle - collisionAngle + math.pi

				self.dx = math.sqrt(self.dx**2+self.dy**2)*math.cos(resultAngle)
				self.dy = math.sqrt(self.dx**2+self.dy**2)*math.sin(resultAngle)
			else:
				self.explode(map)
		elif self.onGroundExplode:
			self.explode(map)
			
			
			
	def onObjectHit(self,map,object):
		if self.objectCollisionDelay == 0:
			self.dx,self.dy,object.dx,object.dy = object.dx,object.dy,self.dx,self.dy #expecting same mass and alvays elastic collision
			self.objectCollisionDelay = 1
			object.objectCollisionDelay = 1
			if self.objectCollisionExplode:
				self.explode(map)
			if object.objectCollisionExplode:
				object.explode(map)

		else:
			self.objectCollisionDelay -= 1



	def onWaterHit(self,map,x,y): # Triggered on water hit
		if self.hitsWater:
			self.onGroundHit(map,x,y)
		else:
			self.dx -= self.dx/75
			self.dy -= self.dy/75 + 0.01

			self.rotate -= self.rotate/40.0

			if self.floats:
				self.dy -= 0.025

	def onBorderHit(self,map,x,y): # Triggered on map border hit
		self.onGroundHit(map,x,y)

	def onShipHit(self,map,ship):  # Triggered on ship hip
		if self.onShipCollision:
			ship.hp -= self.onShipDamage

			ship.lastHitter = self.owner

			if self.onShipExplode:
				self.onGroundHit(map,self.x,self.y)
			else:
				self.destroy(map)

	def collision(self, map): # Detect collisions
		if self.isShip:
			step = 1
		else:
			step = int(self.explosionSizeFactor*self.size/2-1)

		xrange = []
		if self.dx > 0:
			xrange = range(int(self.x)+1, int(self.x+self.dx+1.414213562373095*self.dx/math.sqrt(self.dx**2+self.dy**2+0.01))+1, 1)
		elif self.dx < 0:
			xrange = range(int(self.x)-1, int(self.x+self.dx+1.414213562373095*self.dx/math.sqrt(self.dx**2+self.dy**2+0.01))-1, -step)
		if len(xrange) == 0:
			xrange = [int(self.x)]

		yrange = []
		if self.dy > 0:
			yrange = range(int(self.y)+1, int(self.y+self.dy+1.414213562373095*self.dy/math.sqrt(self.dx**2+self.dy**2+0.01))+1, step)
		elif self.dy < 0:
			yrange = range(int(self.y)-1, int(self.y+self.dy+1.414213562373095*self.dy/math.sqrt(self.dx**2+self.dy**2+0.01))-1, -step)
		if len(yrange) == 0:
			yrange = [int(self.y)]

		groundHit = False
		shipHit = False
		for x in xrange:
			for y in yrange:
				if not(groundHit):
					if x >= map.width or x < 0 or y >= map.height or y < 0:
						groundHit = True
						self.onBorderHit(map,x,y)
					else:
						maskValue = map.mask[x][y]
						if maskValue == map.maskimage.map_rgb((0, 0, 255, 255)):
							groundHit = True
							self.onWaterHit(map,x,y)
						elif maskValue != map.maskimage.map_rgb((0, 0, 0, 255)):
							groundHit = True
							self.onGroundHit(map,x,y)

				if not(shipHit) and not(self.isShip):
					for player in self.game.players:
						object = player.ship
						if object.active:
							distance = (player.ship.x-self.x)**2 + (player.ship.y-self.y)**2
							if distance < (self.size + player.ship.size)**2:
								shipHit = True
								self.onShipHit(map,player.ship)
								
				if self.objectCollision and not(self.isShip):
					for object in self.game.objects:
						if object.objectCollision:
							if self != object:
								distance = (object.x-self.x)**2 + (object.y-self.y)**2
								if distance < (self.size + object.size)**2:
									self.onObjectHit(map,object)

	def move(self): # Move
		self.oldx = self.x # Save old location
		self.oldy = self.y

		self.x += self.dx # Calculate new location with speed
		self.y += self.dy

		if self.gravity:
			self.dy += 0.025 # Gravity

		self.dx -= self.airResistance*0.0002*self.dx**3/math.fabs(self.dx+0.0001) # Air resistance
		self.dy -= self.airResistance*0.0002*self.dy**3/math.fabs(self.dy+0.0001)

		if self.thrust: # Thrusters
			self.dx += self.acceleration*math.cos(self.angle)
			self.dy += self.acceleration*math.sin(self.angle)

		if self.rotate != 0: # Rotation
			self.angle += self.rotate*0.07+random.uniform(-0.008, 0.008)

		if self.rotateWithSpeed:
			if self.dx >= 0:
				self.angle = math.atan(self.dy/self.dx)
			else:
				self.angle = math.atan(self.dy/self.dx)+2*math.pi/2

	def explode(self,map): # Explode
		size = self.explosionSizeFactor*self.size

		if size > 10:
			Sound.playSound(self.game.engine, 0, False)

		if int(self.x+size) > map.width:
			right = map.width
		else:
			right = int(self.x+size)

		if int(self.x-size) < 0:
			left = 0
		else:
			left = int(self.x-size)

		for x in range(left, right):
			if (x-self.x)/(size+0.01) >= -1:
				for y in range(int((-math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y), int((math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y)):
					if y < map.height and y >= 0:
						maskValue = map.mask[x][y]
						if maskValue != map.maskimage.map_rgb((127, 127, 127, 255)) and maskValue != map.maskimage.map_rgb((255, 0, 0, 255)) and maskValue != map.maskimage.map_rgb((0, 0, 0, 255)) and maskValue != map.maskimage.map_rgb((0, 0, 255, 255)):
							map.mask[x][y] = (0, 0, 0)
							map.visual.set_at((x,y),map.background[x][y])
							map.screenImage.set_at((x,y), map.background[x][y])

		for object in self.game.objects:
			distance = (object.x-self.x)**2+(object.y-self.y)**2
			if object != self and object.explosionCollision and distance < size**2:
				object.hp -= math.sqrt((1.5*size)**2-distance)
				if object.isShip:
					object.lastHitter = self.owner

				object.dx += 0.01*(size**2-distance)*(object.x-self.x)/math.sqrt((object.x-self.x+0.01)**2+(object.y-self.y)**2)
				object.dy += 0.01*(size**2-distance)*(object.y-self.y)/math.sqrt((object.x-self.x+0.01)**2+(object.y-self.y)**2)

		for i in range(self.explosionParticleFactor*int(self.size)):
			angle = random.uniform(0,2*math.pi)
			speed = random.uniform(0.1,3.5)
			dx = speed*math.cos(angle)
			dy = speed*math.sin(angle)

			self.game.objects.append(Shard(self.game, self.owner, self.x+5*dx,self.y+5*dy, dx+self.dx/2, dy+self.dy/2))

		self.destroy(map)

	def destroy(self, map): # Delete the object
		if self.active:
			self.active = False

			self.game.objects.remove(self)

	def randomizeLocation(self, map): # Move to a random location with no ground
		while True:
			x = random.randint(1,map.width-1)
			y = random.randint(1,map.height-1)

			if map.mask[x][y] == map.maskimage.map_rgb((0,0,0, 255)):
				break

		self.x = x
		self.y = y

	def redrawLine(self, map, x,y, targetx,targety):
		if x > targetx:
			x1 = targetx-3
			x2 = x+3
		else:
			x1 = x-3
			x2 = targetx+3

		if y > targety:
			y1 = targety-3
			y2 = y+3
		else:
			y1 = y-3
			y2 = targety+3
		map.redraw((x1,y1),(x2-x1,y2-y1))

	def getClosestShip(self, maxRange):
		minDistance = -1
		closestShip = None
		for player in self.game.players:
			object = player.ship
			if object.active and object != self.owner.ship:
				distance = (object.x-self.x)**2 + (object.y-self.y)**2
				if distance < maxRange**2 and (distance < minDistance or minDistance == -1):
					minDistance = distance
					closestShip = object
		return closestShip

class RepairKit(Object):
	def init(self):
		self.gravity = False
		self.explosionCollision = False
		self.explosionSizeFactor = 2
		self.explosionParticleFactor = 2
		self.size = 10

		self.randomizeLocation(self.game.map)

		self.sprite("repairkit.png")

	def onShipHit(self,map,ship):
		if ship.hp > 3*ship.shipModel.hp/4:
			ship.hp = ship.shipModel.hp
		else:
			ship.hp += ship.shipModel.hp/4

		self.destroy(map)

class WeaponChanger(Object):
	def init(self):
		self.gravity = False
		self.explosionSizeFactor = 2
		self.explosionParticleFactor = 2
		self.size = 10

		self.heavy = random.randint(0,1)
		if self.heavy:
			self.newWeapon = eval("Weapons." + Settings.settings["Weapons"]["heavy"][random.randint(0,len(Settings.settings["Weapons"]["heavy"])-1)])(self.game)
		else:
			self.newWeapon = eval("Weapons." + Settings.settings["Weapons"]["light"][random.randint(0,len(Settings.settings["Weapons"]["light"])-1)])(self.game)

		self.randomizeLocation(self.game.map)

		self.sprite("weaponbox.png")

	def onShipHit(self,map,ship):
		if self.heavy:
			ship.heavyWeapon = self.newWeapon
		else:
			ship.lightWeapon = self.newWeapon

		self.destroy(map)

	def draw(self, map):
		self.spriteDraw(map)

		self.text = self.game.engine.text4.render(self.newWeapon.name, True, (255,255,255))

		self.game.map.screenImage.blit(self.text, (self.x-self.text.get_width()/2-1,self.y-23))
		self.game.map.redraw((int(self.x-self.text.get_width()/2-1),int(self.y-23)),(self.text.get_width(), self.text.get_height()))

class ThrustFlame(Object):
	def init(self):
		self.airResistance = 60
		self.lifetime = 7

		self.explosionSizeFactor = 50
		self.hitsWater = True

		self.checkCollisions = False
		self.explosionCollision = False
		self.onGroundExplode = False
		self.onShipCollision = False

		self.red = random.randint(170,255)
		self.green = self.red
		self.color = (self.red, self.green, 0)
		self.size = random.randint(3,4)

	def check(self, map):
		self.size += 0.1

		self.green -= self.green/5
		self.color = (self.red, int(self.green), 0)

		if self.lifetime <= 0:
			self.destroy(map)
		else:
			self.lifetime -= 1

class Smoke(Object):
	def init(self):
		self.airResistance = 60
		self.lifetime = 12

		self.explosionSizeFactor = 50

		self.checkCollisions = False
		self.onGroundExplode = False
		self.onShipCollision = False
		self.explosionCollision = False
		self.floats = True

		self.lightness = random.randint(170,255)
		self.color = (self.lightness, self.lightness, self.lightness)
		self.size = random.randint(3,4)

	def check(self, map):
		self.size += 0.2

		self.lightness -= self.lightness/10
		self.color = (self.lightness, self.lightness, self.lightness)

		if self.lifetime <= 0:
			self.destroy(map)
		else:
			self.lifetime -= 1

		self.dy -= 0.1

class Eraser(Object):
	def init(self):
		self.size = 15
		self.gravity = False
		self.explosionSizeFactor = 0
		self.explosionParticleFactor = 0
		self.checkCollisions = False
		self.explosionCollision = False
		self.onGroundExplode = False
		self.onShipCollision = False

		self.lifetime = 300
		self.counter = 0

		self.airResistance = 0

	def check(self, map):
		if self.lifetime <= 0 or not(self.owner.active):
			self.destroy(map)
		else:
			self.lifetime -= 1

		self.x = self.owner.x+self.owner.dx
		self.y = self.owner.y+self.owner.dy

		if self.counter <= 0:
			self.counter = 2

			size = self.size

			if int(self.x+size) > map.width:
				right = map.width
			else:
				right = int(self.x+size)

			if int(self.x-size) < 0:
				left = 0
			else:
				left = int(self.x-size)

			for x in range(left, right):
				if (x-self.x)/(size+0.01) >= -1:
					for y in range(int((-math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y), int((math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y)):
						if y < map.height and y >= 0:
							maskValue = map.mask[x][y]
							if maskValue != map.maskimage.map_rgb((127, 127, 127, 255)) and maskValue != map.maskimage.map_rgb((255, 0, 0, 255)) and maskValue != map.maskimage.map_rgb((0, 0, 0, 255)):
								map.mask[x][y] = (0, 0, 0)
								map.visual.set_at((x,y),map.background[x][y])
		else:
			self.counter -= 1

	def draw(self,map):
		if self.lifetime > 90:
			color = (random.randint(200,255),random.randint(0,100),0,255)
		else:
			color = (0,random.randint(0,100),random.randint(200,255),255)

		pygame.draw.circle(map.screenImage, color, (int(self.x),int(self.y)), self.size, 2)
		self.redraw(map, self.size+10)

class Flame(Object):
	def init(self):
		self.airResistance = 60
		self.lifetime = 12

		self.explosionSizeFactor = 50
		self.checkCollisions = True
		self.onGroundExplode = False
		self.onShipCollision = True
		self.onShipDamage = 1.00
		self.onShipExplode = False
		self.explosionCollision = False
		self.hitsWater = True

		self.red = random.randint(170,255)
		self.green = self.red
		self.color = (self.red, self.green, 0)
		self.size = random.randint(3,4)

	def check(self, map):
		self.size += 0.3

		self.green -= self.green/8
		self.color = (self.red, int(self.green), 0)

		if self.lifetime <= 0:
			self.destroy(map)
		else:
			self.lifetime -= 1

	def onGroundHit(self,map,x,y):
		self.x = x
		self.y = y
		self.destroy(map)

	def onWaterHit(self,map,x,y):
		self.game.objects.append(Smoke(self.game, self.owner, self.x+self.dx, self.y+self.dy))
		self.onGroundHit(map,x,y)

class Laser(Object):
	def init(self):
		self.size = 0
		self.explosionSizeFactor = 0
		self.explosionParticleFactor = 0
		self.airResistance = 0
		self.checkCollisions = False
		self.onShipDamage = 0.6
		self.onShipExplode = False
		self.explosionCollision = False

	def draw(self, map):
		x = self.x
		y = self.y

		Hit = False
		while not(Hit):
			x += 5*self.dx
			y += 5*self.dy

			for player in self.game.players:
				object = player.ship
				if not(Hit) and object.active:
					distance = (player.ship.x-x)**2 + (player.ship.y-y)**2
					if distance < (player.ship.size + 2)**2:
						Hit = True
						self.onShipHit(map,player.ship)

			if x >= map.width-1 or x < 0 or y >= map.height-1 or y < 0 or map.mask[int(x)][int(y)] != map.maskimage.map_rgb((0, 0, 0, 255)):
				Hit = True

		pygame.draw.line(map.screenImage, (255,0,0,255), (self.x,self.y), (x,y))
		self.redrawLine(map,self.x,self.y,x,y)

		self.destroy(map)

class InstaRail(Object):
	def init(self):
		self.size = 0
		self.explosionSizeFactor = 0
		self.explosionParticleFactor = 0
		self.airResistance = 0
		self.checkCollisions = False
		self.onShipDamage = 500
		self.onShipExplode = True
		self.onGroundExplode = False
		self.explosionCollision = False
		self.gravity = False

		self.color = self.owner.color
		self.lifetime = 60

		self.targetx = self.dx
		self.targety = self.dy

		self.dx = 0
		self.dy = 0

	def draw(self, map):
		if self.lifetime == 60:
			x = self.x
			y = self.y

			Hit = False
			while not(Hit):
				x += 5*self.targetx
				y += 5*self.targety

				for player in self.game.players:
					object = player.ship
					if not(Hit) and object.active:
						distance = (player.ship.x-x)**2 + (player.ship.y-y)**2
						if distance < (player.ship.size + 2)**2:
							Hit = True
							self.onShipHit(map,player.ship)

				if x >= map.width-1 or x < 0 or y >= map.height-1 or y < 0 or map.mask[int(x)][int(y)] != map.maskimage.map_rgb((0, 0, 0, 255)):
					Hit = True

			self.targetx = x
			self.targety = y
		elif self.lifetime == 0:
			self.destroy(map)

		self.lifetime -= 1

		pygame.draw.line(map.screenImage, self.color, (self.x,self.y), (self.targetx,self.targety), int(4*self.lifetime/100.0))
		pygame.draw.line(map.screenImage, (255-(255-self.color[0])/1.75,255-(255-self.color[1])/1.75,255-(255-self.color[2])/1.75,255), (self.x,self.y), (self.targetx,self.targety), int(2*self.lifetime/100.0))
		self.redrawLine(map,self.x,self.y,self.targetx,self.targety)

class Mine(Object):
	def init(self):
		self.gravity = False
		self.explosionSizeFactor = 2.5
		self.explosionParticleFactor = 2
		self.size = 10
		self.floats = True
		self.objectCollision =True
		self.objectCollisionExplode = True

		self.sprite("mine.png")

	def check(self, map):
		self.dx -= self.dx/20.0
		self.dy -= self.dy/20.0

class Cannonball(Object):
	def init(self):
		self.size = 4
		self.explosionSizeFactor = 3
		self.explosionParticleFactor = 3
		self.objectCollision =True

		self.airResistance = 5

class Missile(Object):
	def init(self):
		self.size = 4
		self.explosionSizeFactor = 3
		self.explosionParticleFactor = 1
		self.airResistance = 10
		self.angle = self.owner.ship.angle

		self.activationTime = 30
		self.fuel = 300
		self.target = None

		self.acceleration = 0.085
		self.objectCollision =True
		self.objectCollisionExplode = True

		self.sprite("missile.png")

	def check(self, map):
		if self.activationTime > 0:
			self.activationTime -= 1
		else:
			if self.fuel < 1:
				self.thrust = False
				if random.uniform(0,1) < 0.1:
					self.game.objects.append(Smoke(self.game, self.owner, self.x, self.y))
			else:
				target = self.getClosestShip(300)
				if target != None:
					if self.target == None:
						self.target = target
						Sound.playSound(self.game.engine, 6, False)
					elif target == self.target:
						predictedTargetX = target.x - 5*self.dx
						predictedTargetY = target.y - 5*self.dy
						predictedSelfX = self.x + 5*self.dx
						predictedSelfY = self.y + 5*self.dy + 5

						if predictedTargetX > predictedSelfX and predictedTargetY > predictedSelfY:
							targetAngle = math.atan((predictedSelfY-predictedTargetY)/(self.x+2*self.dx-predictedTargetX))
						elif predictedTargetX < predictedSelfX and predictedTargetY > predictedSelfY:
							targetAngle = math.atan((predictedSelfY-predictedTargetY)/(self.x+2*self.dx-predictedTargetX)) + math.pi
						elif predictedTargetX < predictedSelfX and predictedTargetY < predictedSelfY:
							targetAngle = Functions.returnAngle(math.atan((predictedSelfY-predictedTargetY)/(self.x+2*self.dx-predictedTargetX))) + math.pi
						elif predictedTargetX > predictedSelfX and predictedTargetY < predictedSelfY:
							targetAngle = Functions.returnAngle(math.atan((predictedSelfY-predictedTargetY)/(self.x+2*self.dx-predictedTargetX)) + math.pi) + math.pi
						else:
							targetAngle = math.pi/2

						if predictedTargetY > predictedSelfY:
							if Functions.returnAngle(self.angle) < Functions.returnAngle(targetAngle) or Functions.returnAngle(self.angle) > Functions.returnAngle(targetAngle + math.pi):
								self.angle += 0.1275
							else:
								self.angle -= 0.1275
						elif predictedTargetY < predictedSelfY:
							if Functions.returnAngle(self.angle) < Functions.returnAngle(targetAngle + math.pi) or Functions.returnAngle(self.angle) > Functions.returnAngle(targetAngle):
								self.angle -= 0.1275
							else:
								self.angle += 0.1275

						if math.fabs(Functions.returnAngle(self.angle) - targetAngle) < math.pi/8:
							self.fuel -= 1
							self.thrust = True
							if random.uniform(0,1) < 0.3:
								self.game.objects.append(ThrustFlame(self.game, self.owner, self.x-2*self.dx-5*math.cos(self.angle), self.y-2*self.dy-5*math.sin(self.angle), self.dx-1*math.cos(self.angle), self.dy-1*math.sin(self.angle)))

				else:
					self.thrust = False
					self.activationTime = 10
					self.target = None

class Bolt(Object):
	def init(self):
		self.size = 4
		self.explosionSizeFactor = 1.25
		self.explosionParticleFactor = 0
		self.onShipDamage = 15
		self.explosionCollision = False

		self.airResistance = 20
		self.rotateWithSpeed = True

		self.activationTime = 5
		self.target = None

		self.acceleration = 0.1

		self.sprite("bolt.png")

	def check(self, map):
		if self.activationTime > 0:
			self.activationTime -= 1
		else:
			target = self.getClosestShip(500)
			if target != None:
				if self.target == None:
					self.target = target
				elif target == self.target:
					if target.y > self.y:
						self.dy += self.acceleration
					else:
						self.dy -= self.acceleration

					if target.x > self.x:
						self.dx += self.acceleration
					else:
						self.dx -= self.acceleration

			else:
				self.activationTime = 10
				self.target = None

class Bomb(Object):
	def init(self):
		self.size = 6
		self.explosionSizeFactor = 3
		self.explosionParticleFactor = 2

		self.airResistance = 10
		self.explosionCollision = False
		
		self.objectCollision =True
		self.objectCollisionExplode = True
		
		self.sprite("bomb.png")
		self.rotateWithSpeed = True

		self.dx += random.uniform(-0.1,0.1)

class Dirtball(Object):
	def init(self):
		self.size = 6
		self.explosionSizeFactor = 3
		self.explosionCollision = False

		self.airResistance = 5
		self.rotate = random.uniform(-3,3)
		
		self.objectCollision = True
		self.objectCollisionExplode = True

		self.sprite("dirt.png")

	def explode(self,map): # Make dirt
		size = self.explosionSizeFactor*self.size

		if int(self.x+size) > map.width:
			right = map.width
		else:
			right = int(self.x+size)

		if int(self.x-size) < 0:
			left = 0
		else:
			left = int(self.x-size)

		for x in range(left, right):
			if (x-self.x)/(size+0.01) >= -1:
				for y in range(int((-math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y), int((math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y)):
					if y < map.height and y > 0:
						maskValue = map.mask[x][y]
						if maskValue == map.maskimage.map_rgb((0,0,0,255)) or maskValue == map.maskimage.map_rgb((0,0,255,255)):
							rand = random.randint(-20,20)

							map.mask[x][y] = (150,90,20,255)
							map.visual.set_at((x,y),(145+rand,95+rand,20+rand,255))
							map.screenImage.set_at((x,y),(145+rand,95+rand,20+rand,255))

		Sound.playSound(self.game.engine, 5, False)

		self.destroy(map)

class Disruptionball(Object):
	def init(self):
		self.size = 8
		self.explosionSizeFactor = 4
		self.explosionParticleFactor = 2
		self.explosionCollision = False

		self.color = (50,200,50,255)

		self.airResistance = 5

	def onGroundHit(self,map,x,y):
		self.destroy(map)

	def onShipHit(self,map,ship):
		ship.disruption = 1000

class Larpa(Object):
	def init(self):
		self.airResistance = 5
		self.size = 8
		self.drop = 0
		self.explosionSizeFactor = 1.5
		self.explosionParticleFactor = 0
		self.bounce = True
		
		self.objectCollision =True

	def check(self, map):
		if self.drop == 4:
			self.drop = 0
			self.game.objects.append(Shard(self.game,self.owner,self.x+random.uniform(-self.size,self.size),self.y+random.uniform(-self.size,self.size), 0, 0))
			if self.size > 5:
				self.size -= 0.1
		else:
			self.drop += 1

class Radiation(Object):
	def init(self):
		self.airResistance = 0
 		self.size = 14
		self.explosionSizeFactor = 1
		self.explosionParticleFactor = 0
		self.explosionCollision = False
   		self.gravity = False
		self.onShipDamage = 3

	def onGroundHit(self, map, x, y):
		if self.x <= 0 or self.y <= 0 or self.x >= map.width or self.y >= map.height:
			self.destroy(map)

class Banana(Object):
	def init(self):
		self.explosionSizeFactor = 4
		self.explosionParticleFactor = 0
		self.onShipDamage = 10

		self.airResistance = 5

		self.explosionCollision = False
		self.onShipExplode = False
		
		self.objectCollision =True

		self.size = 2

		self.rotate = random.uniform(-4,4)

		self.sprite("banana.png")

class Bullet(Object):
	def init(self):
		self.explosionSizeFactor = 2
		self.explosionParticleFactor = 0
		self.airResistance = 5

		self.explosionCollision = False
		self.onShipExplode = False
		
		self.objectCollision =True

		self.size = 2
		self.onShipDamage = 6

class Shard(Object):
	def init(self):
		self.explosionSizeFactor = 2
		self.explosionParticleFactor = 0
		self.airResistance = 20

		self.explosionCollision = False
		self.onShipExplode = False

		self.size = random.randint(2,3)
		self.onShipDamage = 2*self.size

class RifleBullet(Object):
	def init(self):
		self.explosionSizeFactor = 5
		self.explosionParticleFactor = 0
		self.airResistance = 2

		self.explosionCollision = False
		self.onShipExplode = False
		
		self.objectCollision =True
		self.objectCollisionExplode = True

		self.size = 2
		self.onShipDamage = 50

class WaterBall(Object):
	def init(self):
		self.size = 3
		self.explosionSizeFactor = 5
		self.explosionCollision = False
		self.airResistance = 5
		self.hitsWater = True
		
		self.objectCollision =True
		self.objectCollisionExplode = True

		self.sprite("waterball.png")

	def explode(self,map): # Make water
		size = self.explosionSizeFactor*self.size

		if int(self.x+size) > map.width:
			right = map.width
		else:
			right = int(self.x+size)

		if int(self.x-size) < 0:
			left = 0
		else:
			left = int(self.x-size)

		for x in range(left, right):
			if (x-self.x)/(size+0.01) >= -1:
				for y in range(int((-math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y), int((math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y)):
					if y < map.height and y > 0:
						if map.mask[x][y] == map.maskimage.map_rgb((0,0,0,255)):
							map.mask[x][y] = (0,0,255,255)
							map.visual.set_at((x,y),(0,0,255,255))
							map.screenImage.set_at((x,y),(0,0,255,255))
							self.game.map.waters.append((x,y))

		self.destroy(map)

class Grenade(Object):
	def init(self):
		self.size = 4
		self.explosionSizeFactor = 3
		self.explosionParticleFactor = 5
		self.lifetime = 150
		self.bounce = True
		
		self.objectCollision =True

	def check(self, map):
		if self.lifetime == 0:
			self.explode(map)
		else:
			self.lifetime -= 1
