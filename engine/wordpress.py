#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import json
from random import randint
from core import *

class Wordpress:
	url     = "http://wp-example.com"
	version = "0.0.0"
	plugins = {}
	themes  = {}
	index   = None
	agent   = False
	users   = {}
	files   = set()

	def __init__(self, url, user_agent, nocheck, max_threads):
		print info("URL: %s" % url)
		self.url   = url
		self.agent = user_agent
		self.max_threads = int(max_threads)
		self.random_agent()
		self.clean_url()
		self.is_up_and_installed()
		self.is_wordpress(nocheck)
		self.is_readme()
		self.is_debug_log()
		self.is_backup_file()
		self.is_xml_rpc()
		self.is_directory_listing()
		self.is_robots_text()
		self.is_common_file()
		self.full_path_disclosure()
		self.enum_wordpress_users()


	"""
	name        : clean_url()
	description : set the url to http(s)://example.com/
	"""
	def clean_url(self):
		if self.url[-1] != '/':
			self.url = self.url + '/'

	"""
	name        : random_agent()
	description : give a random user agent
	"""
	def random_agent(self):
		if self.agent != "random_agent":
			self.agent = "Wordpresscan - For educational purpose only !"
		else:
			with open('database/user-agents.txt','r') as f:
				uas = f.read()

				# remove '#SOMETHING' and '\n\n'
				uas = re.sub("#.*","", uas)
				uas = uas.replace("\n\n","")
				uas = uas.split('\n')

			random = randint(0, len(uas))
			self.agent = uas[random]

	"""
	name        : is_wordpress()
	description : detect a WordPress instance
	"""
	def is_wordpress(self, nocheck):
		self.index = requests.get(self.url, headers={"User-Agent":self.agent}, verify=False)
		if nocheck == False:
			if not "wp-" in self.index.text:
				print critical("Not a WordPress !")
				exit()

	"""
	name        : is_up_and_installed()
	description : check if a website is up or down, then check the installation and a forced redirect
	"""
	def is_up_and_installed(self):
		try:
			r = requests.get(self.url, allow_redirects=False, headers={"User-Agent":self.agent} , verify=False)

	  		if 'location' in r.headers:

	  			# Install is not complete
				if "wp-admin/install.php" in r.headers['location']:
					print critical("The Website is not fully configured and currently in install mode. Call it to create a new admin user.")
		  			exit()

		  		# Redirect
	  			print notice("The remote host tried to redirect to: %s" % r.headers['location'])
	  			user_input = str(raw_input("[?] Do you want to follow the redirection ? [Y]es [N]o, "))

	  			if user_input.lower() == "y":
	  				self.url = r.headers['location']

	  			else:
	  				print critical("Redirection not followed - End of the scan !")
	  				exit()

		except Exception as e:
			print e
			print critical("Website down!")
	  		exit()


	"""
	name        : is_readme()
	description : get the readme file and extract the version is there is any
	"""
	def is_readme(self):
		r = requests.get(self.url + 'readme.html', headers={"User-Agent":self.agent}, verify=False)

		if "200" in str(r):
			self.files.add('readme.html')

			# Basic version fingerprinting
			regex = 'Version (.*)'
			regex = re.compile(regex)
			matches = regex.findall(r.text)

			if len(matches) > 0 and matches[0] != None and matches[0] != "":
				self.version = matches[0]
				print critical("The Wordpress '%s' file exposing a version number: %s" % (self.url+'readme.html', matches[0]))

	"""
	name        : is_debug_log()
	description : determine if there is a debug.log file
	"""
	def is_debug_log(self):
		r = requests.get(self.url + 'debug.log', headers={"User-Agent":self.agent}, verify=False)
		if "200" in str(r) and not "404" in r.text :
			self.files.add('debug.log')
			print critical( "Debug log file found: %s" % (self.url + 'debug.log') )


	"""
	name        : is_backup_file()
	description : determine if there is any unsafe wp-config backup
	"""
	def is_backup_file(self):
		backup = [
			'wp-config.php~', 'wp-config.php.save', '.wp-config.php.bck', 
			'wp-config.php.bck', '.wp-config.php.swp', 'wp-config.php.swp', 
			'wp-config.php.swo', 'wp-config.php_bak', 'wp-config.bak', 
			'wp-config.php.bak', 'wp-config.save', 'wp-config.old', 
			'wp-config.php.old', 'wp-config.php.orig', 'wp-config.orig', 
			'wp-config.php.original', 'wp-config.original', 'wp-config.txt', 
			'wp-config.php.txt', 'wp-config.backup', 'wp-config.php.backup', 
			'wp-config.copy', 'wp-config.php.copy', 'wp-config.tmp', 
			'wp-config.php.tmp', 'wp-config.zip', 'wp-config.php.zip', 
			'wp-config.db', 'wp-config.php.db', 'wp-config.dat',
			'wp-config.php.dat', 'wp-config.tar.gz', 'wp-config.php.tar.gz', 
			'wp-config.back', 'wp-config.php.back', 'wp-config.test', 
			'wp-config.php.test', "wp-config.php.1","wp-config.php.2",
			"wp-config.php.3", "wp-config.php._inc", "wp-config_inc",
			
			'wp-config.php.SAVE', '.wp-config.php.BCK', 
			'wp-config.php.BCK', '.wp-config.php.SWP', 'wp-config.php.SWP', 
			'wp-config.php.SWO', 'wp-config.php_BAK', 'wp-config.BAK', 
			'wp-config.php.BAK', 'wp-config.SAVE', 'wp-config.OLD', 
			'wp-config.php.OLD', 'wp-config.php.ORIG', 'wp-config.ORIG', 
			'wp-config.php.ORIGINAL', 'wp-config.ORIGINAL', 'wp-config.TXT', 
			'wp-config.php.TXT', 'wp-config.BACKUP', 'wp-config.php.BACKUP', 
			'wp-config.COPY', 'wp-config.php.COPY', 'wp-config.TMP', 
			'wp-config.php.TMP', 'wp-config.ZIP', 'wp-config.php.ZIP', 
			'wp-config.DB', 'wp-config.php.DB', 'wp-config.DAT',
			'wp-config.php.DAT', 'wp-config.TAR.GZ', 'wp-config.php.TAR.GZ', 
			'wp-config.BACK', 'wp-config.php.BACK', 'wp-config.TEST', 
			'wp-config.php.TEST', "wp-config.php._INC", "wp-config_INC"
			]

		for b in backup:
			r = requests.get(self.url + b, headers={"User-Agent":self.agent}, verify=False)
			if "200" in str(r) and not "404" in r.text :
				self.files.add(b)
				print critical("A wp-config.php backup file has been found in: %s" % (self.url + b) )


	"""
	name        : is_xml_rpc()
	description : determine if there is an xml rpc interface
	"""
	def is_xml_rpc(self):
		r = requests.get(self.url + "xmlrpc.php", headers={"User-Agent":self.agent}, verify=False)
		if r.status_code == 405 :
			self.files.add("xmlrpc.php")
			print info("XML-RPC Interface available under: %s " % (self.url+"xmlrpc.php") )


	"""
	name        : is_directory_listing()
	description : detect if a directory is misconfigured
	"""
	def is_directory_listing(self):
		directories = ["wp-content/uploads/", "wp-content/plugins/", "wp-content/themes/","wp-includes/", "wp-admin/"]
		dir_name    = ["Uploads", "Plugins", "Themes", "Includes", "Admin"]

		for directory, name in zip(directories,dir_name):
			r = requests.get(self.url + directory, headers={"User-Agent":self.agent}, verify=False)
			if "Index of" in r.text:
				self.files.add(directory)
				print warning("%s directory has directory listing enabled : %s" % (name, self.url + directory))


	"""
	name        : is_robots_text()
	description : detect if a robots.txt file
	"""
	def is_robots_text(self):
		r = requests.get(self.url + "robots.txt", headers={"User-Agent":self.agent}, verify=False)
		if "200" in str(r) and not "404" in r.text :
			self.files.add("robots.txt")
			print info("robots.txt available under: %s " % (self.url+"robots.txt") )
			lines = r.text.split('\n')
			for l in lines:
				if "Disallow:" in l:
					print info("\tInteresting entry from robots.txt: %s" % (l))

	"""
	name        : is_common_file()
	description : detect if a common file such as license.txt is present
	"""
	def is_common_file(self):
		files = ["sitemap.xml","license.txt"]
		for f in files:
			r = requests.get(self.url + f, headers={"User-Agent":self.agent}, verify=False)
			if "200" in str(r) and not "404" in r.text :
				self.files.add(f)
				print info("%s available under: %s " % (f, self.url+f) )

	"""
	name        : full_path_disclosure()
	description : detect a full path disclosure
	"""
	def full_path_disclosure(self):
		r = requests.get(self.url + "wp-includes/rss-functions.php", headers={"User-Agent":self.agent}, verify=False).text
		regex = re.compile("Fatal error:.*? in (.*?) on", re.S)
		matches = regex.findall(r)

		if matches != []:
			print warning("Full Path Disclosure (FPD) in %s exposing %s" % (self.url + "wp-includes/rss-functions.php", matches[0].replace('\n','')) )


	"""
	name        : enum_wordpress_users()
	description : enumerate every users of the wordpress
	"""
	def enum_wordpress_users(self):
		r = requests.get(self.url + "wp-json/wp/v2/users", headers={"User-Agent":self.agent} , verify=False)

		if "200" in str(r):
			print notice("Enumerating Wordpress users")
			users = json.loads(r.text)
			for user in users:
				print info("\tIdentified the following user : %s, %s, %s" % (user['id'], user['name'], user['slug']) )
			self.users = users


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
		print "Agent   : %s" % self.agent
		print "Users   : %s" % self.users
		print "Files   : %s" % self.files
		print "---------------------------"
