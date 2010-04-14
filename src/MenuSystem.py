# -*- coding: utf-8 -*-

import pygame

import Settings

class Menu:
	def __init__(self, engine):
		self.engine = engine
		self.widgets = []

		self.dragging = None

		self.running = True
		self.init()
		self.addWidgets()
		self.draw()

		while self.running:
			self.event()

			if Settings.settings["Screen"]["showfps"]:
				self.engine.screen.blit(self.engine.text.render(str(int(self.engine.clock.get_fps())), True, (255,0,0)), (Settings.settings["Screen"]["width"]-40,10))

			if Settings.settings["Screen"]["scalefactor"] != 1:
				self.engine.scale()

			pygame.display.update()
			self.engine.clock.tick(30)

	def event(self):
		needRedraw = False
		for event in pygame.event.get():
			self.engine.globalEvent(event)

			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.quit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				needRedraw = True
				x = pygame.mouse.get_pos()[0]/Settings.settings["Screen"]["scalefactor"]
				y = pygame.mouse.get_pos()[1]/Settings.settings["Screen"]["scalefactor"]
				for widget in self.widgets:
					try:
						if x > widget.x and x < widget.x+widget.sizex and y > widget.y and y < widget.y+widget.sizey:
							widget.action(self, x,y)
							if widget.isDraggable:
								self.dragging = widget
					except AttributeError:
						pass
			elif self.dragging != None:
				if event.type == pygame.MOUSEMOTION:
					x = pygame.mouse.get_pos()[0]/Settings.settings["Screen"]["scalefactor"]
					y = pygame.mouse.get_pos()[1]/Settings.settings["Screen"]["scalefactor"]
					self.dragging.action(self, x,y)
					needRedraw = True
				elif event.type == pygame.MOUSEBUTTONUP:
					self.dragging = None

		if needRedraw:
			self.draw()
			
	def addWidgets(self):
		pass

	def addWidget(self, widget):
		self.widgets.append(widget)

	def draw(self):
		self.engine.screen.fill((0,0,0))

		for widget in self.widgets:
			widget.draw(self)

		self.engine.messageBox.draw(self.engine)
		self.engine.infoOverlay.draw(self.engine)

	def quit(self, menu=None, x=0,y=0):
		self.running = False

	class Label:
		def __init__(self, location, size, text):
			self.x, self.y = location
			self.size = size
			self.text = text

		def draw(self, menu):
			text = pygame.font.Font(menu.engine.font, self.size).render(self.text, True, (255,255,255))
			menu.engine.screen.blit(text, (self.x, self.y))

	class Button:
		def __init__(self, location, size, text, action):
			self.x, self.y = location
			self.sizex, self.sizey = size
			self.text = text
			self.action = action

		def draw(self, menu):
			menu.engine.screen.fill((0,128,0),((self.x,self.y),(self.sizex,self.sizey)))

			text = menu.engine.text2.render(self.text, True, (255,255,255))
			menu.engine.screen.blit(text, (((2*self.x+self.sizex)-text.get_width())/2,((2*self.y+self.sizey)-text.get_height())/2))

	class CheckBox:
		def __init__(self, location, size, variable, returnValue):
			self.x, self.y = location
			self.sizex, self.sizey = size
			self.variable = variable
			self.returnValue = returnValue

		def draw(self, menu):
			if self.variable:
				menu.engine.screen.fill((0,128,0),((self.x,self.y),(self.sizex,self.sizey)))
			else:
				menu.engine.screen.fill((128,0,0),((self.x,self.y),(self.sizex,self.sizey)))

		def action(self, menu, x,y):
			if self.variable:
				self.variable  = False
			else:
				self.variable  = True
			self.returnValue(self.variable)

	class Slider:
		def __init__(self, location, size, variable, valueRange, returnFunction, parameters=None):
			self.x, self.y = location
			self.x=float(self.x)
			self.sizex, self.sizey = size
			self.sizex=float(self.sizex)
			self.variable = variable
			self.valueRange = valueRange
			self.returnFunction = returnFunction
			self.parameters = parameters
			self.isDraggable = True

		def draw(self, menu):
			menu.engine.screen.fill((0,128,0),((self.x,self.y),(self.sizex,self.sizey)))
			menu.engine.screen.fill((255,255,255),((self.x-self.sizex/20+(self.variable-self.valueRange[0])*(self.sizex/(self.valueRange[1]-self.valueRange[0])),self.y-0.1*self.sizey),(self.sizex/10,1.2*self.sizey)))
			text = menu.engine.text3.render(str(int(round(self.variable))), True, (128,0,0))
			menu.engine.screen.blit(text, (self.x,self.y-0.05*self.sizey))

		def action(self, menu, x,y):
			if x < self.x:
				self.variable = self.valueRange[0]
			elif x > self.x+self.sizex:
				self.variable = self.valueRange[1]
			else:
				self.variable = (x-self.x)*((self.valueRange[1]-self.valueRange[0])/float(self.sizex))+self.valueRange[0]

			self.returnFunction(int(round(self.variable)), self.parameters)
				
	class InputBox:
		def __init__(self, location, size, variable, returnFunction, parameters=None, maxlength=0):
			self.x,self.y = location
			self.sizex,self.sizey = size
			self.variable = variable
			self.returnFunction = returnFunction
			self.maxlength = maxlength
			self.parameters = parameters
			self.cursor = ""
			self.running = False

		def redraw(self, menu):
			menu.engine.screen.fill((0,0,0), ((self.x,self.y),(self.sizex,self.sizey)))
			self.cursor = "|"
			self.draw(menu)
			pygame.display.update()

		def draw(self, menu):
			if self.running:
				pygame.draw.rect(menu.engine.screen, (255,0,0),(self.x,self.y, self.sizex,self.sizey), 1)
			else:
				pygame.draw.rect(menu.engine.screen, (255,255,255),(self.x,self.y, self.sizex,self.sizey), 1)
			menu.engine.screen.blit(menu.engine.text.render(self.variable + self.cursor, 1, (255,255,255)),((self.x+5,self.y+2,self.sizex,self.sizey)))

		def action(self, menu, x,y):
			self.running = True
			while True:
				self.redraw(menu)
				while True:
					event = pygame.event.poll()
					if event.type == pygame.KEYDOWN:
						inkey = event.unicode
						break

				if inkey == "\b": # Backspace
					self.variable = self.variable[0:-1]
				elif inkey == "\r" or inkey == "\x1B": # Return or escape
					self.cursor = ""
					self.returnFunction(self.variable, self.parameters)
					self.running = False
					break
				else:
					if self.maxlength !=0 and not(len(self.variable) == self.maxlength):
						self.variable = self.variable[(self.maxlength-len(self.variable)-1):len(self.variable)]
					self.variable += inkey

	class DropMenu:
		def __init__(self, location, size, variable, values, returnFunction, parameters=None):
			self.x,self.y = location
			self.sizex,self.sizey = size
			self.variable = variable
			self.values = values
			self.returnFunction = returnFunction
			self.opened = False
			self.parameters = parameters

		def redraw(self, menu):
			menu.engine.screen.fill((0,0,0), ((self.x,self.y),(self.sizex,self.sizey)))
			self.draw(menu)
			pygame.display.update()

		def draw(self,menu):
			if not(self.opened):
				self.menu = menu
				menu.engine.screen.fill((0,128,0),((self.x,self.y),(self.sizex,self.sizey)))

				text = menu.engine.text.render(self.variable[1], True, (255,255,255))
				menu.engine.screen.blit(text, (((2*self.x+self.sizex)-text.get_width())/2,((2*self.y+self.sizey)-text.get_height())/2))
			else:
				for i,value in enumerate([self.variable] + self.values):
					starty = self.y + self.sizey*i
					endy = self.y + self.sizey*(i+1)
					self.menu.engine.screen.fill((0,128,0),((self.x,starty),(self.sizex,self.sizey)))

					text = self.menu.engine.text.render(value[1], True, (255,255,255))
					self.menu.engine.screen.blit(text, (((2*self.x+self.sizex)-text.get_width())/2,((starty+endy)-text.get_height())/2))

		def action(self, menu, x,y):
			if not(self.opened):
				self.opened = True
				self.redraw(menu)
				while True:
					event = pygame.event.poll()
					if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
						break
					elif event.type == pygame.MOUSEBUTTONDOWN:
						mousex = pygame.mouse.get_pos()[0]/Settings.settings["Screen"]["scalefactor"]
						mousey = pygame.mouse.get_pos()[1]/Settings.settings["Screen"]["scalefactor"]
						if mousex <= self.sizex+self.x and mousex >= self.x:
							if mousey <= self.y + (len(self.values)+1)*self.sizey and mousey > self.y+self.sizey:
								self.variable = self.values[int((mousey-self.y)/self.sizey-1)]
								self.returnFunction(self.variable, self.parameters)
						break
				self.opened=False
			self.redraw(menu)

	class GetKey:
		def __init__(self, location, size, variable, returnFunction, parameters=None):
			self.x,self.y = location
			self.sizex,self.sizey = size
			self.variable = variable
			self.returnFunction = returnFunction
			self.parameters = parameters
			self.active = False

		def redraw(self, menu):
			menu.engine.screen.fill((0,0,0), ((self.x,self.y),(self.sizex,self.sizey)))
			self.draw(menu)
			pygame.display.update()

		def draw(self, menu):
			if self.active:
				pygame.draw.rect(menu.engine.screen, (255,0,0),(self.x,self.y, self.sizex,self.sizey), 1)
			else:
				pygame.draw.rect(menu.engine.screen, (255,255,255),(self.x,self.y, self.sizex,self.sizey), 1)
			text = menu.engine.text.render(pygame.key.name(self.variable), True, (255,255,255))
			menu.engine.screen.blit(text, (self.x+self.sizex/2-text.get_width()/2,self.y+2+self.sizey/2-text.get_height()/2))

		def action(self, menu, x,y):
			self.active = True
			self.redraw(menu)
			while True:
				event = pygame.event.poll()
				if event.type == pygame.KEYDOWN:
					self.variable = event.key
					self.returnFunction(self.variable, self.parameters)
					self.active = False
					self.redraw(menu)
					break
