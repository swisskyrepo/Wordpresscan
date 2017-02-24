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
		self.list_wp_vulnerabilities(wordpress, "plugins")
		self.list_wp_vulnerabilities(wordpress, "themes")
		self.list_wp_vulnerabilities(wordpress, "wordpresses")

	"""
	name        : fingerprint_wp_version(wordpress)
	description : compare hashes of unique files in order to detect the version
	"""
	def fingerprint_wp_version(self, wordpress):
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
						print warning("Advanced fingerprinting detected wp version : %s" % wordpress.version)
						return
					

	"""
	name        : list_wp_vulnerabilities(self, wordpress, file)
	description : display info about a vulnerability
	"""
	def list_wp_vulnerabilities(self, wordpress, file):
		# Load json file
		with open('database/'+file+'.json') as data_file:
			data = json.load(data_file)

		# Extract plugin's infos
		for key in data.keys():

			# Skip the useless plugins
			if data[key]["vulnerabilities"] == []:
				continue

			# Display vulnerabilities
			print warning("%s: %s" % (file.capitalize(), key) )
			for vuln in data[key]["vulnerabilities"]:

				print notice("\t%s : %s - ID:%s" % (vuln['vuln_type'], vuln['title'] , vuln['id']) )
				print info("\tFixed in %s"% vuln['fixed_in'])

				# Display references
				if 'url' in vuln['references']:
					print info("\tReferences:")
					for ref in vuln['references']['url']:
						print "\t\t -",ref

				print ""
