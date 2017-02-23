#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import os
import time

"""
name        : notice(msg), critical(msg), warning(msg), info(msg)
description : add color to message based on their impact
return      : string
"""
def notice(msg):
  return "\033[1m" + msg + "\033[0m"

def critical(msg):
  return "\033[91;1m/!\ ️" + msg + "\033[0m"

def warning(msg):
  return "\033[92m" + msg + "\033[0m"

def info(msg):
  return "\033[93m" + msg + "\033[0m"


"""
name        : database_update()
description : download and update the database from wpscan website
"""
def database_update():
  print "\033[93mUpdating database\033[92m - Last update: \033[0m" + database_last_date('database/local_vulnerable_files.xml')
  update_url = "https://data.wpscan.org/"
  update_files = [ 'local_vulnerable_files.xml', 'local_vulnerable_files.xsd', 
  'timthumbs.txt', 'user-agents.txt', 'wp_versions.xml', 'wp_versions.xsd', 
  'wordpresses.json', 'plugins.json', 'themes.json', 'LICENSE'] 

  for f in update_files:
    print "\t\033[93mDownloading \033[0m"+ f +" \033[92mFile updated !\033[0m"
    source = requests.get( update_url+f, stream=True).raw

    # Write the file
    with open( 'database/'+f, 'wb' ) as ddl_file:
      progress = 0
      while True:
          length = 16*1024
          buf = source.read(length)
          if not buf:
              break
          ddl_file.write(buf)
          progress += len(buf)
          print('\tDownloaded : %.2f Mo\r' % (float(progress)/(1024*1024))),
        

"""
name        : database_last_date()
description : get the date of the last update through file modification date
return      : string
"""        
def database_last_date(filename):
  (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filename)
  return time.ctime(mtime)
