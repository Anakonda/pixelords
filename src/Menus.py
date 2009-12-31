# -*- coding: utf-8 -*-

import pygame

import Buttons
import Init
import Game
import Functions

class Menu:
	def __init__(self):
		self.init
	
	def event(self):
		pass
	
	def draw(self):
		pass
	
	
class MainMenu(Menu):
	def __init__(self, init):
		self.init = init
		self.draw(self.init)
		self.Buttons = []
		self.Buttons.append(Buttons.StartButton(self.init))
		self.running = True
		while self.running:
			self.event(self.init)
			pygame.display.update()
			
			
	def event(self,init):
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.running = False
				print "Terminating..."
			elif event.type == pygame.MOUSEBUTTONDOWN:
				for Button in self.Buttons:
					for x in range(Button.x, Button.x + Button.sizex):
						for y in range(Button.y, Button.y + Button.sizey):
							if pygame.mouse.get_pos() == (x,y):
								Button.event(init)
			
				
	
	def draw(self, init):
		init.screen.fill((0,0,0))
		
		
	