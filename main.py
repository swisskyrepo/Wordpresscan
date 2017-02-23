#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import argparse
from engine.core import *
from engine.load_plugins import *
from engine.wordpress import *

if __name__ == "__main__":

	print " _    _               _                                         "
	print "| |  | |             | |                                        "
	print "| |  | | ___  _ __ __| |_ __  _ __ ___  ___ ___  ___ __ _ _ __  "
	print "| |/\| |/ _ \| '__/ _` | '_ \| '__/ _ \/ __/ __|/ __/ _` | '_ \ "
	print "\  /\  / (_) | | | (_| | |_) | | |  __/\__ \__ \ (_| (_| | | | |"
	print " \/  \/ \___/|_|  \__,_| .__/|_|  \___||___/___/\___\__,_|_| |_|"
	print "                       | |                                      "
	print "                       |_|                                      "

	parser = argparse.ArgumentParser()
	parser.add_argument('-u', action ='store', dest='url', help="Wordpress URL")
	parser.add_argument('--update', action ='store_const', const='update', dest='update', help="Update the database")
	results = parser.parse_args()
	
	# Check wordpress url
	if results.url != None:
		print "Target: " + results.url

		# Update scripts	
		if results.update != None:		
			database_update()

		# Build a new wordpress object
		wp = Wordpress(results.url)
		wp.to_string()

	else:
		parser.print_help()