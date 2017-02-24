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

	"""
	name        : fingerprint_wp_version(wordpress)
	description : 
	"""
	def fingerprint_wp_version(self, wordpress):
		tree = etree.parse("database/wp_versions.xml")
		root = tree.getroot()

		# Iterating through 'src' file
		for i in range(len(root)):
			
			# !!!! check for '$' $wp-content$ , $wp-plugin$

			# Download file
			ddl_url  = wordpress.url + root[i].get('src')
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
					
