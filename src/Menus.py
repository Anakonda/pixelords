# -*- coding: utf-8 -*-

import pygame

import Settings
import Game
import MenuSystem

class MainMenu(MenuSystem.Menu):
	def init(self):
		self.addWidget(self.Label((Settings.width/6,Settings.height/24),42,"War of Pixelords"))
		self.addWidget(self.Label((10,Settings.height-20),12,"Version: git-experimental"))

		self.addWidget(self.Button((Settings.width/6,Settings.height/6),(Settings.width/6,Settings.height/6),"Play!", self.startGame))
		self.addWidget(self.Button((3*Settings.width/6,Settings.height/6),(Settings.width/6,Settings.height/6),"Quit", self.quit))
		self.addWidget(self.Button((Settings.width/6,2.5*Settings.height/6),(3*Settings.width/6,Settings.height/6),"Options", self.gotoOptions))
		self.addWidget(self.Button((Settings.width/6,4*Settings.height/6),(3*Settings.width/6,Settings.height/12),"Test", self.test))

	def startGame(self,x,y):
		try:
			game = Game.Game(self.engine)
		except Exception as error:
			raise Exception(error)
		pygame.mouse.set_visible(True)
		self.engine.inGame = False

	def gotoOptions(self,x,y):
		optionsMenu = Options(self.engine)

	def test(self,x,y):
		self.engine.messageBox.addMessage("Test")

class Options(MenuSystem.Menu):
	def init(self):
		self.testEnabled = True
		self.testValue = 50

		self.addWidget(self.Label((Settings.width/6,Settings.height/24),36,"Options"))

		self.addWidget(self.CheckBox((Settings.width/6,2.5*Settings.height/6),(Settings.width/24,Settings.width/24), self.testEnabled, self.setTestEnabled))
		self.addWidget(self.Label((Settings.width/4.5,2.5*Settings.height/6),24,"Test enabled"))

		self.addWidget(self.Slider((Settings.width/6,3.4*Settings.height/6),(Settings.width/2,Settings.width/24), self.testValue, (50,150), self.setTestValue))
		self.addWidget(self.Label((Settings.width/6,3*Settings.height/6),24,"Test value"))

		self.addWidget(self.CheckBox((Settings.width/6,4*Settings.height/6),(Settings.width/24,Settings.width/24), Settings.showFPS, self.setShowFPS))
		self.addWidget(self.Label((Settings.width/4.5,4*Settings.height/6),24,"Show FPS"))

		self.addWidget(self.Slider((Settings.width/6,5*Settings.height/6),(Settings.width/2,Settings.width/24), 100*Settings.musicVolume, (0,100), self.setMusicVolume))
		self.addWidget(self.Label((Settings.width/6,4.5*Settings.height/6),24,"Music volume"))

		self.addWidget(self.Button((Settings.width/6,Settings.height/6),(Settings.width/6,Settings.height/6),"Test", self.test))
		self.addWidget(self.Button((3*Settings.width/6,Settings.height/6),(Settings.width/6,Settings.height/6),"OK", self.goBack))

	def setTestEnabled(self, value):
		self.testEnabled = value

	def setTestValue(self, value):
		self.testValue = value

	def setShowFPS(self, value):
		Settings.showFPS = value

	def setMusicVolume(self, value):
		Settings.musicVolume = value/100.0
		pygame.mixer.music.set_volume(Settings.musicVolume)

	def test(self,x,y):
		if self.testEnabled:
			self.engine.messageBox.addMessage("Test " + str(self.testValue))
		else:
			self.engine.messageBox.addMessage("No test")

	def goBack(self,x,y):
		self.quit()
