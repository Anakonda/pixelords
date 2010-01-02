# -*- coding: utf-8 -*-

import pygame
import os

import Settings
import Messages
import Sound
import Menus

class Engine:
	def __init__(self):
		self.initScreen()
		
		self.clock = pygame.time.Clock()

		pygame.font.init()

		self.text = pygame.font.Font(os.path.join("resources","LiberationSans-Bold.ttf"), 16)
		self.text2 = pygame.font.Font(os.path.join("resources","LiberationSans-Bold.ttf"), 42)
		self.text3 = pygame.font.Font(os.path.join("resources","LiberationSans-Bold.ttf"), 32)
		self.text4 = pygame.font.Font(os.path.join("resources","LiberationSans-Bold.ttf"), 12)

		self.messageBox = Messages.MessageBox()

		if Settings.sound:
			self.sound = Sound.Sound(self)
		
		self.menu = Menus.MainMenu(self)

	def initScreen(self): # Create the screen
		screenFlags = []

		if Settings.fullscreen == 1:
			screenFlags.append(pygame.FULLSCREEN)
		elif Settings.fullscreen == 2:
			screenFlags.append(pygame.NOFRAME)

		if Settings.hwAcceleration:
			screenFlags.append(pygame.HWSURFACE)

		if Settings.doubleBuffering:
			screenFlags.append(pygame.DOUBLEBUF)

		screenFlagsCombined = 0
		for flag in screenFlags:
			screenFlagsCombined |= flag

		pygame.display.init()

		pygame.display.set_caption("War of Pixelords")
		pygame.display.set_icon(pygame.image.load(os.path.join("gfx","default","ship2.png")))

		if Settings.scale != 1:
			if Settings.scaleType == 2:
				Settings.scale = 2**int(math.log(Settings.scale,2))
			self.scaled = pygame.display.set_mode((int(Settings.scale*Settings.width), int(Settings.scale*Settings.height)), screenFlagsCombined)
			self.screen = pygame.transform.scale(self.scaled, (Settings.width, Settings.height))
		else:
			self.screen = pygame.display.set_mode((Settings.width, Settings.height), screenFlagsCombined)

	def scale(self): # Scale the screen
		if Settings.scaleType == 1:
			pygame.transform.smoothscale(self.screen, (Settings.scale*Settings.width, Settings.scale*Settings.height), self.scaled)
		elif Settings.scaleType == 2:
			tempscaler = []
			tempscaler.append(self.screen)
			for i in range(1,int(math.log(Settings.scale,2))):
				tempscaler.append(pygame.transform.scale2x(tempscaler[i-1]))
			pygame.transform.scale2x(tempscaler.pop(), self.scaled)
		else:
			pygame.transform.scale(self.screen, (int(Settings.scale*Settings.width), int(Settings.scale*Settings.height)), self.scaled)
