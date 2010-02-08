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

			if Settings.showFPS:
				self.engine.screen.blit(self.engine.text.render(str(int(self.engine.clock.get_fps())), True, (255,0,0)), (Settings.width-40,10))

			if Settings.scale != 1:
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
				x = pygame.mouse.get_pos()[0]/Settings.scale
				y = pygame.mouse.get_pos()[1]/Settings.scale
				for widget in self.widgets:
					try:
						if x > widget.x and x < widget.x+widget.sizex and y > widget.y and y < widget.y+widget.sizey:
							widget.action(x,y)
							if widget.isDraggable:
								self.dragging = widget
					except AttributeError:
						pass
			elif self.dragging != None:
				if event.type == pygame.MOUSEMOTION:
					x = pygame.mouse.get_pos()[0]/Settings.scale
					y = pygame.mouse.get_pos()[1]/Settings.scale
					self.dragging.action(x,y)
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

	def quit(self,x=0,y=0):
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

		def action(self,x,y):
			if self.variable:
				self.variable  = False
			else:
				self.variable  = True
			self.returnValue(self.variable)

	class Slider:
		def __init__(self, location, size, variable, valueRange, returnValue, additionalVariable):
			self.x, self.y = location
			self.sizex, self.sizey = size
			self.variable = variable
			self.valueRange = valueRange
			self.returnValue = returnValue
			self.additionalVariable = additionalVariable
			self.isDraggable = True

		def draw(self, menu):
			menu.engine.screen.fill((0,128,0),((self.x,self.y),(self.sizex,self.sizey)))
			menu.engine.screen.fill((255,255,255),((self.x-self.sizex/20+(self.variable-self.valueRange[0])*(self.sizex/(self.valueRange[1]-self.valueRange[0])),self.y-0.1*self.sizey),(self.sizex/10,1.2*self.sizey)))
			text = menu.engine.text3.render(str(int(round(self.variable))), True, (128,0,0))
			menu.engine.screen.blit(text, (self.x,self.y-0.05*self.sizey))

		def action(self,x,y):
			if x < self.x:
				self.variable = self.valueRange[0]
			elif x > self.x+self.sizex:
				self.variable = self.valueRange[1]
			else:
				self.variable = (x-self.x)*((self.valueRange[1]-self.valueRange[0])/float(self.sizex))+self.valueRange[0]
			if self.additionalVariable == None:
				self.returnValue(int(round(self.variable)))
			else:
				self.returnValue(int(round(self.variable)), self.additionalVariable)
				
	class InputBox:
		def __init__(self, location, size, question, variable, menu, defaultValue, additionalVariable):
			self.x,self.y = location
			self.sizex,self.sizey = size
			self.question = question
			self.variable = variable
			self.current_string = []
			for str in defaultValue:
				self.current_string.append(str)
			self.menu = menu
			self.additionalVariable = additionalVariable

		def draw(self,menu):
			self.display = self.display_box(menu, self.question + ": " + pygame.string.join(self.current_string,""), self.x,self.y, self.sizex,self.sizey)

		def action(self,x,y):
			while 1:
				inkey = self.get_key()
				if inkey == "\b":
					self.current_string = self.current_string[0:-1]
				elif inkey == "\r":
					break
				elif inkey == "^[":
					self.current_string = []
					break
				else:
					self.current_string.append(inkey)
				
				self.display = self.display_box(self.menu, self.question + ": " + pygame.string.join(self.current_string,""), self.x,self.y, self.sizex,self.sizey)
				self.menu.draw()
				pygame.display.update()
			if self.additionalVariable == None:
				self.variable(self.current_string)
			else:
				self.variable(self.current_string, self.additionalVariable)
			
		def display_box(self,menu, message, x,y, sizex,sizey):
			font = menu.engine.text
			self.message = message
			pygame.draw.rect(menu.engine.screen, (0,0,0),(x,y,sizex,sizey), 1)
			pygame.draw.rect(menu.engine.screen, (255,255,255),(x,y,sizex,sizey), 1)
			if len(message) != 0:
				menu.engine.screen.blit(font.render(self.message, 1, (255,255,255)),((x,y,sizex,sizey)))

		def get_key(self):
			while 1:
				event = pygame.event.poll()
				if event.type == pygame.KEYDOWN:
					return event.unicode
				else:
					pass

	class DropMenu:
		def __init__(self, location, size, variable, values, currentValue):
			self.x,self.y = location
			self.sizex,self.sizey=size
			self.variable=variable
			self.values = values
			self.currentValue =currentValue
			
		def draw(self,menu):
			self.menu = menu
			menu.engine.screen.fill((0,128,0),((self.x,self.y),(self.sizex,self.sizey)))

			text = menu.engine.text2.render(str(self.currentValue), True, (255,255,255))
			menu.engine.screen.blit(text, (((2*self.x+self.sizex)-text.get_width())/2,((2*self.y+self.sizey)-text.get_height())/2))
		
		def action(self,x,y):
			valueId = 0
			for value in self.values:
				valueId += 1
				starty = (valueId-1)*self.sizey
				endy = self.sizey*valueId
				self.menu.engine.screen.fill((0,128,0),((self.x,starty),(self.sizex,self.sizey)))

				text = self.menu.engine.text2.render(str(value), True, (255,255,255))
				self.menu.engine.screen.blit(text, (((2*self.x+self.sizex)-text.get_width())/2,((starty+endy)-text.get_height())/2))
			pygame.display.update()
			while 1:
				event = pygame.event.poll()
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					self.quit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					mousex = pygame.mouse.get_pos()[0]/Settings.scale
					mousey = pygame.mouse.get_pos()[1]/Settings.scale
					if mousex <=self.sizex+self.x and mousex>=self.x:
						self.currentValue = self.values[int(mousey/self.sizey)]
						self.variable(self.currentValue)
						self.quit()
					