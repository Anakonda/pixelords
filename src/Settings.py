# -*- coding: utf-8 -*-

import json
import Functions

class Config():
	def load(self, file):
		configFile = open(file, 'r')
		settings = json.loads(configFile.read())
		configFile.close()

		return settings

	def save(self, settings):
		configFile = open('config.txt', 'w')
		configFile.write(json.dumps(settings, sort_keys=True, indent=4))
		configFile.close()

config = Config()
settings = config.load("config.txt")
def getMapSettings():
	try:
		return config.load("maps/" + str(settings["Rules"]["map"]) + "/config.txt")
	except Exception as error:
		Functions.formatException(self.engine, error)