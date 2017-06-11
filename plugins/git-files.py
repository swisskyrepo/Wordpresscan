#!/usr/bin/python
# -*- coding: utf-8 -*-

# name        : GIT configuration files
# description : Check for the file http://blog.domain.com/.git/logs/HEAD
# author      : Wordpresscan Team

import requests

name = "GIT configuration files"

def __init__(wordpress):
	payload = ".git/logs/HEAD"
	r = requests.get(wordpress.url + payload, headers={"User-Agent":wordpress.agent}, verify=False)

	if "200" in str(r):
		print "[+] Wordpress configuration found from GIT !"
		print "[!] {}".format(wordpress.url + payload)
