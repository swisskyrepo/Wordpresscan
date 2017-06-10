#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import argparse
from engine.core import *
from engine.load_plugins import *
from engine.wordpress import *
from engine.scan import *
from engine.fuzz import *
from engine.brute import *

if __name__ == "__main__":

	print "_______________________________________________________________ "
	print " _    _               _                                         "
	print "| |  | |             | |                                        "
	print "| |  | | ___  _ __ __| |_ __  _ __ ___  ___ ___  ___ __ _ _ __  "
	print "| |/\| |/ _ \| '__/ _` | '_ \| '__/ _ \/ __/ __|/ __/ _` | '_ \ "
	print "\  /\  / (_) | | | (_| | |_) | | |  __/\__ \__ \ (_| (_| | | | |"
	print " \/  \/ \___/|_|  \__,_| .__/|_|  \___||___/___/\___\__,_|_| |_|"
	print "                       | |                                      "
	print "                       |_|                                      "
	print " WordPress scanner based on wpscan work - @pentest_swissky      "
	print "_______________________________________________________________ "

	parser = argparse.ArgumentParser()
	parser.add_argument('-u', action ='store', dest='url', help="Wordpress URL")
	parser.add_argument('--update', action ='store_const', const='update', dest='update', help="Update the database")
	parser.add_argument('--aggressive', action ='store_const', const='aggressive', dest='aggressive', default=False, help="Update the database")
	parser.add_argument('--fuzz', action ='store_const', const='fuzz', dest='fuzz', default=False, help="Fuzz the files")
	parser.add_argument('--brute', action ='store', dest='brute', default=None, help="Bruteforce users and passwords")
	parser.add_argument('--random-agent', action ='store_const', const='random_agent', dest='random_agent', default=False, help="Random User-Agent")
	results = parser.parse_args()

	# Check wordpress url
	if results.url != None:

		# Update scripts
		if results.update != None:
			database_update()

		# Build a new wordpress object
		wp = Wordpress(results.url, results.random_agent)

		# Launch bruteforce
		Brute_Engine(wp, results.brute)

		# Launch fuzzing
		Fuzz_Engine(wp, results.fuzz)

		# Launch scans
		Scan_Engine(wp, results.aggressive)

		# Load plugins for more functions
		Load_Plugins(wp)

	else:
		parser.print_help()
