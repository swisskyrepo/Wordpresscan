#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import os
import time
import hashlib

"""
name        : notice(msg), critical(msg), warning(msg), info(msg)
description : add color to message based on their impact
return      : string
"""
def ask(msg):
  return "\033[1m[?] " + msg + "\033[0m"

def notice(msg):
  return "\033[1m[i] " + msg + "\033[0m"

def critical(msg):
  return "\033[91m[!] " + msg + "\033[0m"

def warning(msg):
  return "\033[93m[i] " + msg + "\033[0m"

def info(msg):
  return "\033[0m[+] " + msg + "\033[0m"


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
    download_raw_file(update_url+f, "database/"+f, True)
    

"""
name        : database_last_date()
description : get the date of the last update through file modification date
return      : string
"""        
def database_last_date(filename):
  (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filename)
  return time.ctime(mtime)


"""
name        : download_raw_file(url, filename)
description : will download a raw file from url into filename
""" 
def download_raw_file(url, filename, verbosity):
  try:

    # Open the request
    source = requests.get( url, stream=True).raw

    # Write the file
    with open( filename, 'wb' ) as ddl_file:
      progress = 0
      while True:
          length = 16*1024
          buf = source.read(length)
          if not buf:
              break
          ddl_file.write(buf)
          progress += len(buf)
          
          if verbosity == True:
            print('\tDownloaded : %.2f Mo\r' % (float(progress)/(1024*1024))),
        
  except Exception as e:
    raise e
 
 
"""
name        : download_file(url, filename)
description : will download a file from url into filename
""" 
def download_file(url, filename, verbosity):
  try:

    # Open the request
    source = requests.get( url).text

    # Write the file
    with open( filename, 'wb' ) as ddl_file:
      ddl_file.write(source.encode('utf8'))
        
  except Exception as e:
    raise e


"""
name        : remove_file(filename)
description : will remove a file from the computer
""" 
def remove_file(filename):
  try:
    os.remove(filename)
  except Exception as e:
    raise e
  


"""
name        : md5_hash(filename)
description : will compute the md5 hash of the file
return      : string
""" 
def md5_hash(filename):
  return hashlib.md5(open(filename, 'rb').read()).hexdigest()


"""
name        : is_lower(str_one, str_two)
description : will compare two string version
return      : boolean
""" 
def is_lower(str_one, str_two):
  sum_one = 0
  sum_two = 0

  # Fix for X.X <= X.X.X and X.X.X <= X.X
  if len(str_one) < 5:
    str_one += '.0'
  if len(str_two) < 5:
    str_two += '.0'

  str_one = str_one[::-1].split('.')
  str_two = str_two[::-1].split('.')

  for i in range(len(str_one)):
    try:
      sum_one += ((i+1) ** 10) * (int(str_one[i]))
      sum_two += ((i+1) ** 10) * (int(str_two[i]))
    except Exception as e:
      return True
  
  if sum_one < sum_two:
    return True

  return False