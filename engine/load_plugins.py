#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import json
import os
import imp

from wordpress import *

class Load_Plugins:
	plugin_folder = "./plugins"

	def __init__(self, wordpress):
		available_plugins = os.listdir(self.plugin_folder)
		for plugins in available_plugins:
			if not ".pyc" in plugins and not "__init__" in plugins:

				# Find and load the package
				name = plugins.replace('.py','')
				f, file, desc = imp.find_module('plugins', ['.'])
				pkg = imp.load_module('plugins', f, file, desc)

				# Find and load the plugin
				f, file, desc = imp.find_module(name, pkg.__path__)
				loaded = imp.load_module('plugins.' + name, f, file, desc)

				# Run the __init__
				print notice('Plugin %s loaded.' % loaded.name)
				loaded.__init__(wordpress)
