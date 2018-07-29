#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning # Required for bad https website
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
	parser.add_argument('--aggressive', action ='store_const', const='aggressive', dest='aggressive', default=False, help="Aggressive scan for plugins/themes")
	parser.add_argument('--fuzz', action ='store_const', const='fuzz', dest='fuzz', default=False, help="Fuzz the files")
	parser.add_argument('--brute', action ='store_const', const='brute', dest='brute', default=False, help="Bruteforce users and passwords")
	parser.add_argument('--nocheck', action ='store_const', const='nocheck',dest='nocheck', default=False, help="Check for a Wordpress instance")
	parser.add_argument('--random-agent', action ='store_const', const='random_agent', dest='random_agent', default=False, help="Random User-Agent")
	parser.add_argument('--threads', action ='store', dest='max_threads', default=1, help="Number of threads to use")
	parser.add_argument('--usernames', action ='store', dest='usernames', default='', help="Usernames to bruteforce separated with a ','")
	parser.add_argument('--users-list', action ='store', dest='users_list', default=None, help="Users list for bruteforce")
	parser.add_argument('--passwords-list', action ='store', dest='passwords_list', default=None, help="Passwords list for bruteforce")
	parser.add_argument('--debug', action ='store_const', const='debug', dest='debug', default=False, help="Enable a debugging flag")
	results = parser.parse_args()

	# Check wordpress url
	if results.url != None:
		# Disable warning for ssl verify=False
		# NOTE: This should not be removed until a correct solution is found
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

		# Update scripts
		if results.update != None:
			database_update()

		# Build a new wordpress object
		wp = Wordpress(format_url(results.url), results.random_agent, results.nocheck, results.max_threads)

		# Launch bruteforce
		Brute_Engine(wp, results.brute, results.usernames, results.users_list, results.passwords_list)

		# Launch fuzzing
		Fuzz_Engine(wp, results.fuzz)

		# Launch scans
		Scan_Engine(wp, results.aggressive)

		# Load plugins for more functions
		Load_Plugins(wp)

		# Debug
		if results.debug:
			wp.to_string()

	else:
		parser.print_help()
