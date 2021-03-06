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
		self.addWidget(self.Label((10,Settings.settings["Screen"]["height"]-20),12,"Version: 0.2.0-alpha"))

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
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/4,Settings.settings["Screen"]["height"]/24),36,"Options"))
	
		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/8,1.5*Settings.settings["Screen"]["height"]/8),
			(4*Settings.settings["Screen"]["width"]/12,Settings.settings["Screen"]["height"]/10),"Players",self.gotoPlayersMenu))
		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/8,3*Settings.settings["Screen"]["height"]/8),
			(4*Settings.settings["Screen"]["width"]/12,Settings.settings["Screen"]["height"]/10),"Graphics",self.gotoGraphicsMenu))
		self.addWidget(self.Button((4.5*Settings.settings["Screen"]["width"]/8,1.5*Settings.settings["Screen"]["height"]/8),
			(4*Settings.settings["Screen"]["width"]/12,Settings.settings["Screen"]["height"]/10),"Game rules",self.gotoRulesMenu))
		self.addWidget(self.Button((4.5*Settings.settings["Screen"]["width"]/8,3*Settings.settings["Screen"]["height"]/8),
			(4*Settings.settings["Screen"]["width"]/12,Settings.settings["Screen"]["height"]/10),"Controls",self.gotoControlsMenu))
		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/8,4.5*Settings.settings["Screen"]["height"]/8),
			(4*Settings.settings["Screen"]["width"]/12,Settings.settings["Screen"]["height"]/10),"Audio",self.gotoSoundMenu))

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
		
	def gotoControlsMenu(self, menu, x,y):
		try:
			ControlsMenu = Controls(self.engine)
		except Exception as error:
			Functions.formatException(self.engine, error)

		self.widgets = []
		self.addWidgets()

	def gotoRulesMenu(self, menu, x,y):
		try:
			RulesMenu = Rules(self.engine)
		except Exception as error:
			Functions.formatException(self.engine, error)

		self.widgets = []
		self.addWidgets()

	def gotoSoundMenu(self, menu, x,y):
		try:
			SoundMenu = Sound(self.engine)
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
		self.gfxlist = []
		for gfx in Functions.getFolders("gfx"):	
			self.gfxlist.append((gfx, gfx))

		self.displayModes = []
		for mode in pygame.display.list_modes():	
			self.displayModes.append((mode,str(mode[0]) + "x" + str(mode[1])))
		
	def addWidgets(self):
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/8,Settings.settings["Screen"]["height"]/24), 36,"Graphics Options"))
		self.addWidget(self.CheckBox((3*Settings.settings["Screen"]["width"]/8,Settings.settings["Screen"]["height"]/6),
			(Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["width"]/24), Settings.settings["Screen"]["fullscreen"], self.setFullscreen))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/8,Settings.settings["Screen"]["height"]/6),24,"Fullscreen"))
		self.addWidget(self.CheckBox((3*Settings.settings["Screen"]["width"]/8,1.5*Settings.settings["Screen"]["height"]/6),
			(Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["width"]/24), Settings.settings["Screen"]["showfps"], self.setFPS))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/8,1.5*Settings.settings["Screen"]["height"]/6), 24,"Show FPS"))
		self.addWidget(self.DropMenu((3*Settings.settings["Screen"]["width"]/8,2*Settings.settings["Screen"]["height"]/6),
			(2*Settings.settings["Screen"]["width"]/12,Settings.settings["Screen"]["width"]/32), ((Settings.settings["Screen"]["width"],Settings.settings["Screen"]["height"]),
			str(Settings.settings["Screen"]["width"])+"x"+str(Settings.settings["Screen"]["height"])), self.displayModes, self.setResolution))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/8,2*Settings.settings["Screen"]["height"]/6), 24,"Resolution"))
		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/12,5*Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"OK", self.goBack))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/8,2.5*Settings.settings["Screen"]["height"]/6), 24,"Graphics theme"))
		self.addWidget(self.DropMenu((3*Settings.settings["Screen"]["width"]/8,2.5*Settings.settings["Screen"]["height"]/6),
			(2*Settings.settings["Screen"]["width"]/12,Settings.settings["Screen"]["width"]/32), (Settings.settings["Rules"]["gfxtheme"],Settings.settings["Rules"]["gfxtheme"]), self.gfxlist, self.setGfxTheme))
		
	def setGfxTheme(self, value, parameters):
		Settings.settings["Rules"]["gfxtheme"] = value[0]
		
	def setFullscreen(self, value):
		Settings.settings["Screen"]["fullscreen"] = value
		self.engine.initScreen()
		
	def setFPS(self, value):
		Settings.settings["Screen"]["showfps"] = value
		
	def setResolution(self, value, parameters):
		Settings.settings["Screen"]["width"] = value[0][0]
		Settings.settings["Screen"]["height"] = value[0][1]
		self.widgets = []
		self.addWidgets()
		self.engine.initScreen()
		
	def goBack(self, menu, x,y):
		self.quit()

class Rules(MenuSystem.Menu):
	def init(self):
		self.maplist = []
		for map in Functions.getFolders("maps"):
			metadata = Settings.getMapMetadata(map)
			if metadata != None:
				self.maplist.append((map, metadata["name"]))

	def addWidgets(self):
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/5,Settings.settings["Screen"]["height"]/24), 36,"Game rules"))

		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/20,Settings.settings["Screen"]["height"]/6), 24,"Map"))
		self.addWidget(self.DropMenu((3.6*Settings.settings["Screen"]["width"]/9,Settings.settings["Screen"]["height"]/6),
			(2*Settings.settings["Screen"]["width"]/12,Settings.settings["Screen"]["width"]/32), (Settings.settings["Rules"]["map"],Settings.settings["Rules"]["map"]), self.maplist, self.setMap, None))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/20,1.5*Settings.settings["Screen"]["height"]/6), 24,"Loading speed"))		
		self.addWidget(self.Slider((3.6*Settings.settings["Screen"]["width"]/9,1.5*Settings.settings["Screen"]["height"]/6),
			(2*Settings.settings["Screen"]["width"]/8,Settings.settings["Screen"]["height"]/24),Settings.settings["Rules"]["loadingspeed"],(0,1000),self.setLoadingSpeed))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/20,2*Settings.settings["Screen"]["height"]/6), 24,"Reset weapons on death"))
		self.addWidget(self.CheckBox((3.6*Settings.settings["Screen"]["width"]/9,2*Settings.settings["Screen"]["height"]/6),
			(Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["width"]/24), Settings.settings["Rules"]["resetweaponsondeath"], self.setResetWeaponsOnDeath))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/20,2.5*Settings.settings["Screen"]["height"]/6), 24,"Insta mode"))
		self.addWidget(self.CheckBox((3.6*Settings.settings["Screen"]["width"]/9,2.5*Settings.settings["Screen"]["height"]/6),
			(Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["width"]/24), Settings.settings["Rules"]["insta"], self.setInsta))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/20,3*Settings.settings["Screen"]["height"]/6), 24,"Ship strength"))
		self.addWidget(self.Slider((3.6*Settings.settings["Screen"]["width"]/9,3*Settings.settings["Screen"]["height"]/6),
			(2*Settings.settings["Screen"]["width"]/8,Settings.settings["Screen"]["height"]/24),Settings.settings["Rules"]["shipstrength"],(1,1000),self.setShipStrength))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/20,3.5*Settings.settings["Screen"]["height"]/6), 24,"Lives"))		
		self.addWidget(self.Slider((3.6*Settings.settings["Screen"]["width"]/9,3.5*Settings.settings["Screen"]["height"]/6),
			(2*Settings.settings["Screen"]["width"]/8,Settings.settings["Screen"]["height"]/24),Settings.settings["Rules"]["lives"],(1,50),self.setLives))

		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/12,5*Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"OK", self.goBack))

	def goBack(self, menu, x,y):
		self.quit()

	def setResetWeaponsOnDeath(self, value):
		Settings.settings["Rules"]["resetweaponsondeath"] = value

	def setShipStrength(self, value, parameters):
		Settings.settings["Rules"]["shipstrength"] = value

	def setLoadingSpeed(self, value, parameters):
		Settings.settings["Rules"]["loadingspeed"] = value

	def setLives(self, value, parameters):
		Settings.settings["Rules"]["lives"] = value

	def setInsta(self, value):
		Settings.settings["Rules"]["insta"] = value

	def setMap(self, value, parameters):
		self.mapSettings = Settings.getMapMetadata(value[0])
		if self.mapSettings != None:
			Settings.settings["Rules"]["map"] = value[0]
		else:
			self.engine.messageBox.addMessage("Unable to load the selected map!")

class Controls(MenuSystem.Menu):
	def init(self):
		pass		
		
	def addWidgets(self):
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/5,Settings.settings["Screen"]["height"]/24), 36,"Controls"))
		self.addWidget(self.Label((2*Settings.settings["Screen"]["width"]/7+10,Settings.settings["Screen"]["height"]/4), 20,"Left"))
		self.addWidget(self.Label((3*Settings.settings["Screen"]["width"]/7+10,Settings.settings["Screen"]["height"]/4), 20,"Right"))
		self.addWidget(self.Label((4*Settings.settings["Screen"]["width"]/7-10,Settings.settings["Screen"]["height"]/4), 20,"Shoot 1st"))
		self.addWidget(self.Label((5*Settings.settings["Screen"]["width"]/7-10,Settings.settings["Screen"]["height"]/4), 20,"Shoot 2nd"))
		self.addWidget(self.Label((6*Settings.settings["Screen"]["width"]/7-5,Settings.settings["Screen"]["height"]/4), 20,"Trusters"))
		for playerId in range(0,Settings.settings["Rules"]["playeramount"]):
			self.addWidget(self.Label((Settings.settings["Screen"]["width"]/16,(playerId+2.5)*Settings.settings["Screen"]["height"]/8), 24,Settings.settings["Players"][playerId]["name"]))
			self.addWidget(self.GetKey((2*Settings.settings["Screen"]["width"]/7,(2.5+playerId)*Settings.settings["Screen"]["height"]/8),
				(2*Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["height"]/24), Settings.settings["Players"][playerId]["controls"]["rotate1"], self.setPlayerKeys, (playerId,"rotate1")))
			self.addWidget(self.GetKey((3*Settings.settings["Screen"]["width"]/7,(2.5+playerId)*Settings.settings["Screen"]["height"]/8),
				(2*Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["height"]/24), Settings.settings["Players"][playerId]["controls"]["rotate2"], self.setPlayerKeys, (playerId,"rotate2")))
			self.addWidget(self.GetKey((4*Settings.settings["Screen"]["width"]/7,(2.5+playerId)*Settings.settings["Screen"]["height"]/8),
				(2*Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["height"]/24), Settings.settings["Players"][playerId]["controls"]["shoot1"], self.setPlayerKeys, (playerId,"shoot1")))
			self.addWidget(self.GetKey((5*Settings.settings["Screen"]["width"]/7,(2.5+playerId)*Settings.settings["Screen"]["height"]/8),
				(2*Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["height"]/24), Settings.settings["Players"][playerId]["controls"]["shoot2"], self.setPlayerKeys, (playerId,"shoot2")))
			self.addWidget(self.GetKey((6*Settings.settings["Screen"]["width"]/7,(2.5+playerId)*Settings.settings["Screen"]["height"]/8),
				(2*Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["height"]/24), Settings.settings["Players"][playerId]["controls"]["thrust"], self.setPlayerKeys, (playerId,"thrust")))

		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/12,5*Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"OK", self.goBack))

	def goBack(self, menu, x,y):
		self.quit()
		
	def setPlayerKeys(self, value, (playerId,Key)):
		Settings.settings["Players"][playerId]["controls"][Key] = value

class Sound(MenuSystem.Menu):
	def init(self):
		pass

	def addWidgets(self):
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/8,Settings.settings["Screen"]["height"]/24), 36,"Audio Options"))
		self.addWidget(self.CheckBox((3*Settings.settings["Screen"]["width"]/8,Settings.settings["Screen"]["height"]/6),
			(Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["width"]/24), Settings.settings["Sound"]["enabled"], self.setSoundEnabled))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/8,Settings.settings["Screen"]["height"]/6),24,"Sound enabled"))
		self.addWidget(self.CheckBox((3*Settings.settings["Screen"]["width"]/8,1.5*Settings.settings["Screen"]["height"]/6),
			(Settings.settings["Screen"]["width"]/24,Settings.settings["Screen"]["width"]/24), Settings.settings["Sound"]["music"], self.setMusic))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/8,1.5*Settings.settings["Screen"]["height"]/6), 24,"Music"))
		self.addWidget(self.Label((Settings.settings["Screen"]["width"]/20,3.5*Settings.settings["Screen"]["height"]/6), 24,"Music volume"))		
		self.addWidget(self.Slider((3.6*Settings.settings["Screen"]["width"]/9,3.5*Settings.settings["Screen"]["height"]/6),
			(2*Settings.settings["Screen"]["width"]/8,Settings.settings["Screen"]["height"]/24),100*Settings.settings["Sound"]["musicvolume"],(1,100),self.setMusicVolume))

		self.addWidget(self.Button((Settings.settings["Screen"]["width"]/12,5*Settings.settings["Screen"]["height"]/6),(Settings.settings["Screen"]["width"]/6,Settings.settings["Screen"]["height"]/8),"OK", self.goBack))

	def setSoundEnabled(self, value):
		Settings.settings["Sound"]["enabled"] = value
		if Settings.settings["Sound"]["music"]:
			if Settings.settings["Sound"]["enabled"]:
				self.engine.sound.loadMusic()
			else:
				pygame.mixer.music.stop()
		
	def setMusic(self, value):
		Settings.settings["Sound"]["music"] = value
		if Settings.settings["Sound"]["enabled"]:
			if Settings.settings["Sound"]["music"]:
				self.engine.sound.loadMusic()
			else:
				pygame.mixer.music.stop()
		
	def setMusicVolume(self, value, parameters):
		Settings.settings["Sound"]["musicvolume"] = value/100.0
		pygame.mixer.music.set_volume(Settings.settings["Sound"]["musicvolume"])
		
	def goBack(self, menu, x,y):
		self.quit()
