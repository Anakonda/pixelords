# -*- coding: utf-8 -*-

import Settings

class MessageBox:
	def __init__(self):
		self.show = 0
		self.showForce = False
		self.messages = []

	def addMessage(self, message): # Add a new message to the box
		if len(self.messages) > 4:
			self.messages.pop(0)

		self.messages.append(message)
		self.show = 600

		print ":: " + message

	def draw(self, game): # Show the messages
		if self.show > 0 or self.showForce:
			self.show -= 1
			for i,message in enumerate(self.messages):
				game.screen.blit(game.text4.render(message, True, (255,255,255)), (5,5+i*15))

class InfoOverlay:
	def __init__(self):
		self.show = False

	def draw(self, engine):
		if self.show:
			if engine.inGame:
				engine.screen.fill((64,64,64),((Settings.settings["Screen"]["width"]-300,20),(275,180)))

				engine.screen.blit(engine.text.render("F10 - Save map", True, (255,255,255)), (Settings.settings["Screen"]["width"]-280,160))
				engine.screen.blit(engine.text.render("F11 - Take a full map screenshot", True, (255,255,255)), (Settings.settings["Screen"]["width"]-280,180))
			else:
				engine.screen.fill((64,64,64),((Settings.settings["Screen"]["width"]-300,20),(275,120)))

			engine.screen.blit(engine.text3.render("Hotkeys", True, (255,255,255)), (Settings.settings["Screen"]["width"]-290,20))
			engine.screen.blit(engine.text.render("ESC - Exit the game", True, (255,255,255)), (Settings.settings["Screen"]["width"]-280,60))
			engine.screen.blit(engine.text.render("F1 - Show this help", True, (255,255,255)), (Settings.settings["Screen"]["width"]-280,80))
			engine.screen.blit(engine.text.render("F5 - Toggle music", True, (255,255,255)), (Settings.settings["Screen"]["width"]-280,100))
			engine.screen.blit(engine.text.render("F12 - Take a screenshot", True, (255,255,255)), (Settings.settings["Screen"]["width"]-280,120))
