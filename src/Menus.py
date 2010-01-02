# -*- coding: utf-8 -*-

import pygame

import Buttons
import Init
import Game
import Functions

class Menu:
	def __init__(self, init):
		self.initiation = init
		self.draw(self.initiation)
		self.Buttons = []

		self.running = True
		self.init()
		while self.running:
			self.event(self.initiation)
			self.draw(self.initiation)
			for button in self.Buttons:
				button.draw(self.initiation)
			pygame.display.update()

	
	def event(self, init):
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				for Button in self.Buttons:
					for x in range(Button.x, Button.x + Button.sizex):
						for y in range(Button.y, Button.y + Button.sizey):
							if pygame.mouse.get_pos() == (x,y):
								Button.event(init)

	def draw(self):
		pass
	
	
class MainMenu(Menu):
	def init(self):
		self.Buttons.append(Buttons.StartButton(self.initiation))

	def draw(self, init):
		init.screen.fill((0,0,0))
		
		
	