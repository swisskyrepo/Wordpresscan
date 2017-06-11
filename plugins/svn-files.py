#!/usr/bin/python
# -*- coding: utf-8 -*-

# name        : SVN configuration files
# description : Check for the file http://blog.domain.com/.svn/text-base/wp-config.php.svn-base
# author      : Wordpresscan Team

import requests

name = "SVN configuration files"

def __init__(wordpress):
	payload = ".svn/text-base/wp-config.php.svn-base"
	r = requests.get(wordpress.url + payload, headers={"User-Agent":wordpress.agent}, verify=False)

	if "200" in str(r):
		print "[+] Wordpress configuration found from SVN !"
		print "[!] {}".format(wordpress.url + payload)
