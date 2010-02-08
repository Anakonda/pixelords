# -*- coding: utf-8 -*-

import json

class Config():
	def load(self):
		configFile = open('config.txt', 'r')
		settings = json.loads(configFile.read())
		configFile.close()

		return settings

	def save(self, settings):
		configFile = open('config.txt', 'w')
		configFile.write(json.dumps(settings, sort_keys=True, indent=4))
		configFile.close()

config = Config()
settings = config.load()
