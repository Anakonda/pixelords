# -*- coding: utf-8 -*-

import pygame

import Settings
import Functions
import Game
import MenuSystem

class MainMenu(MenuSystem.Menu):
	def init(self):
		pass
		
	def addWidgets(self):
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24),42,"War of Pixelords"))
		self.addWidget(self.Label((10,Settings.settings["Screen"]["height"]-20),12,"Version: git-experimental"))

		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),"Play!", self.startGame))
		self.addWidget(self.Button((3*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),"Quit", self.quit))
		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/6,2.5*Settings.settings["Screen"]["height"]/6),(3*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),"Options", self.gotoOptions))

	def startGame(self, menu, x,y):
		try:
			game = Game.Game(self.engine)
		except Exception as error:
			Functions.formatException(self.engine, error)

		pygame.mouse.set_visible(True)
		self.engine.inGame = False

	def gotoOptions(self, menu, x,y):
		optionsMenu = Options(self.engine)
		self.widgets = []
		self.addWidgets()

class Options(MenuSystem.Menu):
	def init(self):
		pass
		
	def addWidgets(self):
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24),36,"Options"))
	
		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),(3*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"Players",self.gotoPlayersMenu))
		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/6,2.5*Settings.settings["Screen"]["height"]/6),(3*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"Graphics",self.gotoGraphicsMenu))

		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/12,5*Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"Back", self.goBack))
		self.addWidget(self.Button((9*Settings.settings["Screen"]["width"]/12,5*Settings.settings["Screen"]["height"]/6), (Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"Save", self.Save))

	def gotoPlayersMenu(self, menu, x,y):
		try:
			PlayersMenu = Players(self.engine)
		except Exception as error:
			Functions.formatException(self.engine, error)
		
		self.widgets = []
		self.addWidgets()
		
	def gotoGraphicsMenu(self, menu, x,y):
		try:
			GraphicsMenu = Graphics(self.engine)
		except Exception as error:
			Functions.formatException(self.engine, error)

		self.widgets = []
		self.addWidgets()

	def Save(self, menu, x,y):
		Settings.config.save(Settings.settings)
		self.engine.messageBox.addMessage("Settings saved to file.")

	def goBack(self, menu, x,y):
		self.quit()

class Players(MenuSystem.Menu):
	def init(self):
		pass
		
	def addWidgets(self):
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24),36,"Player Options"))
		self.addWidget(self.Label((3*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),24,"Player Amount"))
		self.addWidget(self.Slider((4.5*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),
			(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24),Settings.settings["Rules"]["playeramount"], (2,4), self.setPlayerAmount))
		for playerId in range(0,Settings.settings["Rules"]["playeramount"]):
			self.addWidget(self.InputBox((Settings.settings["Screen"]["width"]/8,(1.5+playerId)*Settings.settings["Screen"]["height"]/6),
				(2*Settings.settings["Screen"]["width"]/8,Settings.settings["Screen"]["height"]/24), Settings.settings["Players"][playerId]["name"], self.setPlayerName, playerId))
			self.addWidget(self.Slider((3.5*Settings.settings["Screen"]["width"]/6,(1.5+playerId)*Settings.settings["Screen"]["height"]/6),
				(2*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24),Settings.settings["Players"][playerId]["color"]["red"],(0,255),self.setPlayerColor, (playerId, "red")))
			self.addWidget(self.Slider((3.5*Settings.settings["Screen"]["width"]/6,(1.5+playerId)*Settings.settings["Screen"]["height"]/6+Settings.settings["Screen"]["height"]/22),
				(2*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24),Settings.settings["Players"][playerId]["color"]["green"],(0,255),self.setPlayerColor, (playerId, "green")))
			self.addWidget(self.Slider((3.5*Settings.settings["Screen"]["width"]/6,(1.5+playerId)*Settings.settings["Screen"]["height"]/6+2*Settings.settings["Screen"]["height"]/22),
				(2*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24),Settings.settings["Players"][playerId]["color"]["blue"],(0,255),self.setPlayerColor, (playerId, "blue")))
		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/12,5*Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"OK", self.goBack))

	def setPlayerAmount(self, value, parameters):
		Settings.settings["Rules"]["playeramount"] = value
		self.widgets = []
		self.addWidgets()

	def setPlayerColor(self, value, (playerId, color)):
		Settings.settings["Players"][playerId]["color"][color] = value
	
	def setPlayerName(self, value, playerId):
		Settings.settings["Players"][playerId]["name"] = value

	def goBack(self, menu, x,y):
		self.quit()
		
class Graphics(MenuSystem.Menu):
	def init(self):
		pass
		
	def addWidgets(self):
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24), 36,"Graphics Options"))
		self.addWidget(self.CheckBox((3*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),
			(Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["width"]/24), Settings.settings["Screen"]["fullscreen"], self.setFullscreen))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),24,"Fullscreen"))
		self.addWidget(self.CheckBox((3*Settings.settings["Screen"]["width"]/6,1.5*Settings.settings["Screen"]["height"]/6),
			(Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["width"]/24), Settings.settings["Screen"]["showfps"], self.setFPS))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/6,1.5*Settings.settings["Screen"]["height"]/6), 24,"Show FPS"))
		self.addWidget(self.DropMenu((3*Settings.settings["Screen"]["width"]/6,2*Settings.settings["Screen"]["height"]/6),
			(2*Settings.settings["Screen"]["width"]/12,Settings.settings["Screen"]["width"]/32), (Settings.settings["Screen"]["width"],Settings.settings["Screen"]["height"]), pygame.display.list_modes(), self.setResolution))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/6,2*Settings.settings["Screen"]["height"]/6), 24,"Resolution"))
		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/12,5*Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"OK", self.goBack))
		
	def setFullscreen(self, value):
		Settings.settings["Screen"]["fullscreen"] = value
		self.engine.initScreen()
		
	def setFPS(self, value):
		Settings.settings["Screen"]["showfps"] = value
		
	def setResolution(self, value, parameters):
		Settings.settings["Screen"]["width"] = value[0]
		Settings.settings["Screen"]["height"] = value[1]
		self.widgets = []
		self.addWidgets()
		self.engine.initScreen()
		
	def goBack(self, menu, x,y):
		self.quit()
