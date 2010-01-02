# -*- coding: utf-8 -*-

import pygame

import Settings
import Game


class Button:
	def __init__(self, init):
		self.initiation = init
		self.init()
		
	def event(self):
		pass
	
	def draw(self):
		pass
		
class StartButton(Button):
	def init(self):
		self.x = Settings.width/6
		self.y = Settings.height/6
		self.sizex = Settings.width/6
		self.sizey = Settings.height/6
		self.draw(self.initiation)
		
	def event(self, init):
		pygame.mouse.set_visible(False)
		game=Game.Game(init)
		pygame.mouse.set_visible(True)
		pygame.display.update()
	
	def draw(self, init):
		init.screen.blit(self.initiation.text.render("Start game", True, (255,255,255)),(self.x,self.y))
	