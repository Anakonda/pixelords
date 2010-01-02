# -*- coding: utf-8 -*-

import pygame

import Settings
import Init
import Game
import Functions

class Menu:
	def __init__(self, engine):
		self.engine = engine
		self.buttons = []

		self.running = True
		self.init()
		while self.running:
			self.event()
			self.draw()
			pygame.display.update()
			self.engine.clock.tick(100)
	
	def event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.quit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				x,y = pygame.mouse.get_pos()
				for button in self.buttons:
					if x > button.x and x < button.x+button.sizex and y > button.y and y < button.y+button.sizey:
						button.action()

	def addButton(self, location, size, text, action):
		self.buttons.append(self.Button(self,location, size, text, action))

	def draw(self):
		self.engine.screen.fill((0,0,0))

		for button in self.buttons:
			button.draw()

	def quit(self):
		self.running = False

	def gotoMenu(self, menu):
		self.quit()
		self.engine.menu = menu(self.engine)

	class Button:
		def __init__(self, menu, location, size, text, action):
			self.menu = menu
			self.x, self.y = location
			self.sizex, self.sizey = size
			self.text = text
			self.action = action
			
		def draw(self):
			self.menu.engine.screen.fill((0,128,0),((self.x,self.y),(self.sizex,self.sizey)))

			text = self.menu.engine.text2.render(self.text, True, (255,255,255))
			self.menu.engine.screen.blit(text, (((2*self.x+self.sizex)-text.get_width())/2,((2*self.y+self.sizey)-text.get_height())/2))

class MainMenu(Menu):
	def init(self):
		self.addButton((Settings.width/6,Settings.height/6),(Settings.width/6,Settings.height/6),"Play!", self.startGame)
		self.addButton((3*Settings.width/6,Settings.height/6),(Settings.width/6,Settings.height/6),"Quit", self.quit)
		self.addButton((Settings.width/6,2.5*Settings.height/6),(3*Settings.width/6,Settings.height/6),"Options", self.gotoOptions)
		self.addButton((Settings.width/6,4*Settings.height/6),(3*Settings.width/6,Settings.height/6),"Test", self.test)

	def startGame(self):
		game = Game.Game(self.engine)
		pygame.mouse.set_visible(True)

	def gotoOptions(self):
		self.gotoMenu(Options)

	def test(self):
		print "Test"

class Options(Menu):
	def init(self):
		self.addButton((Settings.width/6,Settings.height/6),(Settings.width/6,Settings.height/6),"Test", self.test)
		self.addButton((3*Settings.width/6,Settings.height/6),(Settings.width/6,Settings.height/6),"OK", self.gotoMainMenu)

	def test(self):
		print "Test"

	def gotoMainMenu(self):
		self.gotoMenu(MainMenu)
