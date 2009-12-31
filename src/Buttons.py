# -*- coding: utf-8 -*-

import pygame

import Settings
import Game


class Button:
	def __init__(self):
		pass
	def event(self):
		pass
	
	def draw(self):
		pass
		
class StartButton(Button):
	def __init__(self, init):
		self.init = init
		self.x = Settings.width/6
		self.y = Settings.height/6
		self.sizex = Settings.width/6
		self.sizey = Settings.height/6
		self.draw(self.init)
		
	def event(self, init):
		pygame.mouse.set_visible(False)
		game=Game.Game(init)
		pygame.mouse.set_visible(True)
		pygame.display.update()
	
	def draw(self, init):
		self.init.screen.blit(self.init.text.render("Start game", True, (255,255,255)),(self.x,self.y))
	