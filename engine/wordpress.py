#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
from core import *

class Wordpress:
	url     = "http://wp-example.com"
	version = "0.0.0"
	plugins = False
	themes  = False

	def __init__(self, url):
		self.url = url
		self.is_up_and_installed()
		self.is_readme()
		self.is_debug_log()
		self.is_backup_file()


	"""
	name        : is_up_and_installed()
	description : check if a website is up or down, then check the installation and a forced redirect
	"""  
	def is_up_and_installed(self):
		try:
			r = requests.get(self.url,  allow_redirects=False)

	  		if 'location' in r.headers:

	  			# Install is not complete
				if "wp-admin/install.php" in r.headers['location']:
					print critical("The Website is not fully configured and currently in install mode. Call it to create a new admin user.")
		  			exit()

		  		# Redirect
	  			print notice("The remote host tried to redirect to: %s" % r.headers['location'])
	  			user_input = str(raw_input("[?] Do you want follow the redirection ? [Y]es [N]o, "))

	  			if user_input == "Y":
	  				self.url = r.headers['location']

	  			else:
	  				print critical("Redirection not followed - End of the scan !")
	  				exit()

		except Exception as e:
			print critical("Website down!"),e
	  		exit()
	  	

	"""
	name        : is_readme()
	description : get the readme file and extract the version is there is any
	""" 
	def is_readme(self):
		r = requests.get(self.url + '/readme.html').text
		regex = 'Version (.*)'
		regex = re.compile(regex)
		matches = regex.findall(r)

		if matches[0] != None and matches[0] != "":
			self.version = matches[0]
			print warning("The wordpress %s file exposing a version number %s" % (self.url+'/readme.html', matches[0]))


	"""
	name        : is_debug_log()
	description : determine if there is a debug.log file
	""" 
	def is_debug_log(self):
		r = requests.get(self.url + '/debug.log')
		if "200" in str(r) and not "404" in r.text :
			print critical( "Debug log file found: %s" % (self.url + '/debug.log') )


	"""
	name        : is_backup_file()
	description : determine 
	""" 
	def is_backup_file(self):
		backup = ['wp-config.php~', 'wp-config.php.save', '.wp-config.php.swp', 'wp-config.php.swp', '.wp-config.php.swp', 'wp-config.php.swp', 'wp-config.php.swo', 'wp-config.php_bak', 'wp-config.bak', 'wp-config.php.bak', 'wp-config.save', 'wp-config.old', 'wp-config.php.old', 'wp-config.php.orig', 'wp-config.orig', 'wp-config.php.original', 'wp-config.original', 'wp-config.txt']
		for b in backup:
			r = requests.get(self.url + "/" + b)
			if "200" in str(r) and not "404" in r.text :
				print critical("A wp-config.php backup file has been found in: %s" % (self.url + "/" + b) ) 
        

	"""
	name        : to_string()
	description : display a debug view of the object
	"""  
	def to_string(self):
		print "--------WORDPRESS----------"
		print "URL     : %s" % self.url
		print "Version : %s" % self.version
		print "Plugins : %s" % self.plugins
		print "Themes  : %s" % self.themes
		print "---------------------------"