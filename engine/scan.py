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
			print info("WordPress version %s identified from advanced fingerprinting" % wordpress.version)
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
						print info("WordPress version %s identified from advanced fingerprinting" % wordpress.version)
						return
					

	"""
	name        : list_wp_version_vulnerabilities(self, wordpress, file)
	description : display info about vulnerabilities affecting the current wordpress
	"""
	def list_wp_version_vulnerabilities(self, wordpress, file):
		# Load json file
		with open('database/'+file+'.json') as data_file:
			data = json.load(data_file)
		
		for vuln in data[wordpress.version]["vulnerabilities"]: 
				
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