# -*- coding: utf-8 -*-

import json

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
	return config.load("maps/" + str(settings["Rules"]["map"]) + "/config.txt")
