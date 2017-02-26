#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import json

from core import *
from wordpress import *
from lxml import etree


class Scan_Engine:

	def __init__(self, wordpress):
		self.fingerprint_wp_version(wordpress)
		self.list_wp_version_vulnerabilities(wordpress, "wordpresses")
		self.enumerating_themes_passive(wordpress)
		self.enumerating_plugins_passive(wordpress)

	"""
	name        : fingerprint_wp_version(wordpress)
	description : compare hashes of unique files in order to detect the version
	"""
	def fingerprint_wp_version(self, wordpress):
		# Meta tag based
		regex = re.compile('meta name="generator" content="WordPress (.*?)"')
		match = regex.findall( requests.get(wordpress.url).text )
		
		if match != []:
			wordpress.version = match[0]
			print critical("WordPress version %s identified from advanced fingerprinting" % wordpress.version)
			return

		# Hash based
		tree = etree.parse("database/wp_versions.xml")
		root = tree.getroot()

		# Iterating through 'src' file
		for i in range(len(root)):

			# Download file
			ddl_url  = (wordpress.url + root[i].get('src') ).replace('$','')
			ddl_name = "/tmp/" + (root[i].get('src').replace('/','-'))
			download_file( ddl_url , ddl_name , True ) 

			# Get hash of the file
			ddl_hash = md5_hash(ddl_name)

			# Delete the file
			remove_file(ddl_name)

			# Iterating throug 'md5' hash
			for j in range(len(root[i])):
				if "Element" in str(root[i][j]):

					# Detect the version
					if ddl_hash == root[i][j].get('md5'): 
						wordpress.version =  root[i][j][0].text
						print critical("WordPress version %s identified from advanced fingerprinting" % wordpress.version)
						return
					

	"""
	name        : list_wp_version_vulnerabilities(self, wordpress, file)
	description : display info about vulnerabilities affecting the current wordpress
	"""
	def list_wp_version_vulnerabilities(self, wordpress, file):
		# Load json file
		with open('database/'+file+'.json') as data_file:
			data = json.load(data_file)
		
		# Try to get a close result if the version is not in the list
		version = wordpress.version
		if data[wordpress.version]["vulnerabilities"] == []:
			versions = data.keys()
			for v in versions:
				if v[:4] in wordpress.version and is_lower(wordpress.version, v, False):
					version = v

		# Best accurate result
		for vuln in data[version]["vulnerabilities"]: 
				
			# Basic infos
			print warning("\t%s : %s - ID:%s" % (vuln['vuln_type'], vuln['title'] , vuln['id']) )
			print info("\tFixed in %s"% vuln['fixed_in']) 

			# Display references
			print info("\tReferences:")
			for refkey in vuln['references'].keys():
				for ref in vuln['references'][refkey]:
							
					if refkey != 'url':
						print "\t\t - %s %s" % (refkey.capitalize(), ref)
					else:
						print "\t\t - %s" %ref

			print ""


	"""
	name        : display_vulnerable_component(self, name, version):
	description : display info about vulnerability from the file
	"""
	def display_vulnerable_component(self, name, version, file):
		# Load json file
		with open('database/' + file + '.json') as data_file:
			data = json.load(data_file)
		
		print warning("Name: %s - v%s" % (name, version))
		if name in data.keys():

			# Display the out of date info if the version is lower of the latest version
			if is_lower(version, data[name]['latest_version'], False):	
				print info("The version is out of date, the latest version is %s" % data[name]['latest_version'])			
			
			# Display the vulnerability if it's not patched version
			for vuln in data[name]['vulnerabilities']:
				if 'fixed_in' in vuln.keys() and (vuln['fixed_in'] == None or is_lower(version, vuln['fixed_in'], True)):

					# Main informations
					print "\t",vulnerable("%s : %s - ID:%s" % (vuln['vuln_type'], vuln['title'] , vuln['id']) )
					print "\t",display("Fixed in %s"% vuln['fixed_in']) 

					# Display references
					print "\t",display("References:")
					for refkey in vuln['references'].keys():
						for ref in vuln['references'][refkey]:							
							if refkey != 'url':
								print "\t\t - %s %s" % (refkey.capitalize(), ref)
							else:
								print "\t\t - %s" %ref


	"""
	name        : enumerating_themes_passive(self, wordpress)
	description : enumerate every theme used by the wordpress
	"""
	def enumerating_themes_passive(self, wordpress):
		print notice("Enumerating themes from passive detection ...")
		r = requests.get(wordpress.url).text
	
		# Theme name (css file)
		regex = re.compile('wp-content/themes/(.*?)/.*?[css|js].*?ver=([0-9\.]*)')
		match = regex.findall(r)
		theme = {}

		# Unique theme
		for m in match:
			
			# Remove minified and github version
			theme_name = m[0]
			theme_name = theme_name.replace('-master','')
			theme_name = theme_name.replace('.min','')
			theme_version = m[1]

			if m[0] not in theme.keys():
				theme[m[0]] = m[1]
				self.display_vulnerable_component(theme_name, theme_version, "themes")

		
	"""
	name        : enumerating_plugins_passive(self, wordpress)
	description : enumerate every plugins used by the wordpress
	"""
	def enumerating_plugins_passive(self, wordpress):
		print notice("Enumerating plugins from passive detection ...")
		r = requests.get(wordpress.url).text

		# Plugin name (js file)
		regex = re.compile('wp-content/plugins/(.*?)/.*?[css|js].*?ver=([0-9\.]*)') 
		match = regex.findall(r)
		plugin = {}

		# Unique plugin
		for m in match:

			# Remove minified and github version
			plugin_name = m[0]
			plugin_name = plugin_name.replace('-master','')
			plugin_name = plugin_name.replace('.min','')
			plugin_version = m[1]

			if plugin_name not in plugin.keys() and m[1]!='1':
				plugin[plugin_name] = m[1]
				self.display_vulnerable_component(plugin_name, plugin_version, "plugins")