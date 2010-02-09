# -*- coding: utf-8 -*-

import pygame
import os

import Settings
import Messages
import Menus

class Engine:
	def __init__(self):
		self.initScreen()
		
		self.clock = pygame.time.Clock()

		pygame.font.init()

		self.font = os.path.join("resources","LiberationSans-Bold.ttf")

		self.text = pygame.font.Font(self.font, 16)
		self.text2 = pygame.font.Font(self.font, 42)
		self.text3 = pygame.font.Font(self.font, 32)
		self.text4 = pygame.font.Font(self.font, 12)

		self.messageBox = Messages.MessageBox()
		self.infoOverlay = Messages.InfoOverlay()

		if Settings.settings["Sound"]["enabled"]:
			self.sound = Sound.Sound(self)
		
		self.inGame = False

		self.mainMenu = Menus.MainMenu(self)

	def globalEvent(self, event): # Handle global events
		# General events:
		if event.type == pygame.constants.USEREVENT:
			self.sound.loadMusic()

		# Global keys:
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
			path = Functions.saveNameIncrement("screenshots", "screen", "png")
			pygame.image.save(self.screen, path)
			self.messageBox.addMessage("Screenshot saved to " + path + ".")
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
			self.messageBox.showForce = True
			self.infoOverlay.show = True
		elif event.type == pygame.KEYUP and event.key == pygame.K_F1:
			self.messageBox.showForce = False
			self.infoOverlay.show = False
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
			if Settings.settings["Sound"]["enabled"]:
				if Settings.settings["Sound"]["music"]:
					Settings.settings["Sound"]["music"] = False
					pygame.mixer.music.stop()
				else:
					Settings.settings["Sound"]["music"] = True
					self.sound.loadMusic()
			else:
				print "Warning: Can't enable music (sounds are not enabled)"
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT:
			if Settings.settings["Screen"]["fullscreen"]:
				Settings.settings["Screen"]["fullscreen"] = False
			elif not(Settings.settings["Screen"]["fullscreen"]):
				Settings.settings["Screen"]["fullscreen"] = True
			self.initScreen()

	def initScreen(self): # Create the screen
		screenFlags = []

		if Settings.settings["Screen"]["fullscreen"] and Settings.settings["Screen"]["fullscreenconstrain"]:
			screenFlags.append(pygame.FULLSCREEN)
		elif Settings.settings["Screen"]["fullscreen"]:
			screenFlags.append(pygame.NOFRAME)

		if Settings.settings["Screen"]["hwacceleration"]:
			screenFlags.append(pygame.HWSURFACE)

		if Settings.settings["Screen"]["doublebuffering"]:
			screenFlags.append(pygame.DOUBLEBUF)

		screenFlagsCombined = 0
		for flag in screenFlags:
			screenFlagsCombined |= flag

		pygame.display.init()

		pygame.display.set_caption("War of Pixelords")
		pygame.display.set_icon(pygame.image.load(os.path.join("gfx","default","ship2.png")))

		if Settings.settings["Screen"]["scalefactor"] != 1:
			if Settings.scaleType == 2:
				Settings.scale = 2**int(math.log(Settings.scale,2))
			self.scaled = pygame.display.set_mode((int(Settings.scale*Settings.settings["Screen"]["width"]), int(Settings.scale*Settings.settings["Screen"]["height"])), screenFlagsCombined)
			self.screen = pygame.transform.scale(self.scaled, (Settings.settings["Screen"]["width"], Settings.settings["Screen"]["height"]))
		else:
			self.screen = pygame.display.set_mode((Settings.settings["Screen"]["width"], Settings.settings["Screen"]["height"]), screenFlagsCombined)

	def scale(self): # Scale the screen
		if Settings.scaleType == 1:
			pygame.transform.smoothscale(self.screen, (Settings.scale*Settings.settings["Screen"]["width"], Settings.scale*Settings.settings["Screen"]["height"]), self.scaled)
		elif Settings.scaleType == 2:
			tempscaler = []
			tempscaler.append(self.screen)
			for i in range(1,int(math.log(Settings.scale,2))):
				tempscaler.append(pygame.transform.scale2x(tempscaler[i-1]))
			pygame.transform.scale2x(tempscaler.pop(), self.scaled)
		else:
			pygame.transform.scale(self.screen, (int(Settings.scale*Settings.settings["Screen"]["width"]), int(Settings.scale*Settings.settings["Screen"]["height"])), self.scaled)
