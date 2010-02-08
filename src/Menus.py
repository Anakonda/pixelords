# -*- coding: utf-8 -*-

import pygame
import traceback

import Settings
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

	def startGame(self,x,y):
		try:
			game = Game.Game(self.engine)
		except Exception as error:
			print
			print "#"*80
			self.engine.messageBox.addMessage("Error: " + str(error))
			print "#"*80
			traceback.print_exc()
			print "#"*80
			print

		pygame.mouse.set_visible(True)
		self.engine.inGame = False

	def gotoOptions(self,x,y):
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


	def gotoPlayersMenu(self,x,y):
		PlayersMenu = Players(self.engine)
		self.widgets = []
		self.addWidgets()
		
	def gotoGraphicsMenu(self,x,y):
		GraphicsMenu = Graphics(self.engine)
		self.widgets = []
		self.addWidgets()
		
	def goBack(self,x,y):
		self.quit()

class Players(MenuSystem.Menu):
	def init(self):
		self.playerAmount = Settings.settings["Rules"]["playeramount"]
		self.playerNames = []
		self.colors = []
		for i in range(0,self.playerAmount):
			self.playerNames.append(Settings.settings["Players"][i]["name"]) 
			self.colors.append(Settings.settings["Players"][i]["color"]["red"])
			self.colors.append(Settings.settings["Players"][i]["color"]["green"])
			self.colors.append(Settings.settings["Players"][i]["color"]["blue"])

		self.addWidgets()
		
	def addWidgets(self):
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24),36,"Player Options"))
		self.addWidget(self.Label((3*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),24,"Player Amount"))
		self.addWidget(self.Slider((4.5*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24),self.playerAmount,(2,4),self.setPlayerAmount,None))
		for playerId in range(0,self.playerAmount):
			self.addWidget(self.InputBox((Settings.settings["Screen"]["width"]/8,(1.5+playerId)*Settings.settings["Screen"]["height"]/6),(2*Settings.settings["Screen"]["width"]/8,Settings.settings["Screen"]["height"]/24),"Name", self.setPlayerName,self,playerId))
			self.addWidget(self.Label((2*Settings.settings["Screen"]["width"]/6,(1.5+playerId)*Settings.settings["Screen"]["height"]/6),24,"player "+str(playerId+1)+" color"))
			self.addWidget(self.Slider((3.5*Settings.settings["Screen"]["width"]/6,(1.5+playerId)*Settings.settings["Screen"]["height"]/6),(2*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24),self.colors[3*playerId],(0,255),self.setPlayerColor,playerId*3))
			self.addWidget(self.Slider((3.5*Settings.settings["Screen"]["width"]/6,(1.5+playerId)*Settings.settings["Screen"]["height"]/6+Settings.settings["Screen"]["height"]/22),(2*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24),self.colors[3*playerId+1],(0,255),self.setPlayerColor,playerId*3+1))
			self.addWidget(self.Slider((3.5*Settings.settings["Screen"]["width"]/6,(1.5+playerId)*Settings.settings["Screen"]["height"]/6+2*Settings.settings["Screen"]["height"]/22),(2*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24),self.colors[3*playerId+2],(0,255),self.setPlayerColor,playerId*3+2))
		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/12,5*Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"Back", self.goBack))
		self.addWidget(self.Button((9*Settings.settings["Screen"]["width"]/12,5*Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"Save", self.Save))

	def Save(self,x,y):
		Settings.settings["Rules"]["playeramount"] = self.playerAmount
		for i in range(0,Settings.settings["Rules"]["playeramount"]):

			Settings.settings["Players"][i]["color"]["red"],Settings.settings["Players"][i]["color"]["green"],Settings.settings["Players"][i]["color"]["blue"] = self.colors[i*3],self.colors[i*3+1],self.colors[i*3+2]
			(Settings.settings["Players"][i]["name"]  = self.playerNames[i]
		self.quit()

	def setPlayerAmount(self,value):
		self.playerAmount = value
		self.widgets = []
		self.addWidgets()

	def setPlayerColor(self,value,colorId):
		self.colors[colorId] = value
	
	def setPlayerName(self,value,playerId):
		self.playerNames[playerId] = pygame.string.join(value,"")

	def goBack(self,x,y):
		self.quit()
		
class Graphics(MenuSystem.Menu):
	def init(self):
		self.fullscreen = Settings.fullscreen
		self.showFPS = Settings.showFPS
		self.resolution = Settings.settings["Screen"]["width"],Settings.settings["Screen"]["height"]
		
	def addWidgets(self):
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/24),36,"Graphics Options"))
		
		self.addWidget(self.CheckBox((3*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["width"]/24), self.fullscreen, self.setfullscreen))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/6),24,"Full screen"))
	
		self.addWidget(self.CheckBox((3*Settings.settings["Screen"]["width"]/6,1.5*Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["width"]/24), self.fullscreen, self.setFPS))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/6,1.5*Settings.settings["Screen"]["height"]/6),24,"Show FPS"))
		
		self.addWidget(self.DropMenu((3*Settings.settings["Screen"]["width"]/6,2*Settings.settings["Screen"]["height"]/6),(2*Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["width"]/18),self.setResolution,pygame.display.list_modes(),self.resolution))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/6,6*Settings.settings["Screen"]["height"]/6),24,"Resolution"))

		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/12,5*Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"Back", self.goBack))
		self.addWidget(self.Button((9*Settings.settings["Screen"]["width"]/12,5*Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"Save", self.Save))
		
	def setfullscreen(self, value):
		self.fullscreen = value
		
	def setFPS(self, value):
		self.showFPS = value
		
	def setResolution(self, value):
		self.resolution = value
		
	def Save(self,x,y):
		Settings.settings["Screen"]["width"],Settings.settings["Screen"]["height"]=self.resolution
		Settings.showFPS = self.showFPS
		Settings.fullscreen = self.fullscreen
		self.engine.initScreen()
		self.quit()
		
	def goBack(self,x,y):
		self.quit()