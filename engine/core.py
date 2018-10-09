#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import os
import time
import hashlib
import json

"""
name        : notice(msg), critical(msg), warning(msg), info(msg)
description : add color to message based on their impact
return      : string
"""
def ask(msg):
  return "\033[1m[?] " + msg + "\033[0m"

def notice(msg):
  return "\n\033[1m[i] " + msg + "\033[0m"

def critical(msg):
  return "\033[91m[!] " + msg + "\033[0m"

def warning(msg):
  return "\033[93m[i] " + msg + "\033[0m"

def info(msg):
  return "\033[0m[+] " + msg + "\033[0m"

def vulnerable(msg):
  return "\033[91m[!]" + msg + "\033[0m"

def display(msg):
  return "\033[0m | " + msg + "\033[0m"



"""
name        : format_url()
description : will format the URL to provide an http
"""
def format_url(url):
    if not "http" in url:
        return "http://"+url
    return url

"""
name        : unzip_file()
description : unzip a file, used for user-agents.txt and timthumbs.txt
"""
def unzip_file(filename):
  with open(filename, 'r') as f:
    data = f.read()

    # Check for a buggy .gz
    if not "/timthumb.php" in data and not "Mozilla/5.0" in data:
      os.system('mv '+ filename + ' ' + filename + ".gz")
      os.system('gzip -d '+ filename+".gz")

"""
name        : database_update()
description : download and update the database from wpscan website
warning     : user-agents.txt and timthumbs.txt are zip files
"""
def database_update():
  print "\033[93mUpdating database\033[92m - Last update: \033[0m" + database_last_date('database/local_vulnerable_files.xml')
  update_url = "https://data.wpscan.org/"
  update_files = [ 'local_vulnerable_files.xml', 'local_vulnerable_files.xsd',
  'timthumbs.txt', 'user-agents.txt', 'wp_versions.xml', 'wp_versions.xsd',
  'wordpresses.json', 'plugins.json', 'themes.json']

  for f in update_files:
    print "\t\033[93mDownloading \033[0m"+ f +" \033[92mFile updated !\033[0m"
    download_raw_file(update_url+f, "database/"+f, True)

  unzip_file("database/user-agents.txt")
  unzip_file("database/timthumbs.txt")


"""
name        : database_last_date()
description : get the date of the last update through file modification date
return      : string
"""
def database_last_date(filename):
  if not os.path.isfile(filename):
    return "Never"
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
    with open( filename, 'wb+' ) as ddl_file:
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
def is_lower(str_one, str_two, equal):
  sum_one = 0
  sum_two = 0

  # Handle the NoneType
  if str_one == None:
      if str_two == None:
          return False
      else:
          return True

  if str_two == None:
      if str_one == None:
          return False
      else:
          return True

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

  # For inferior
  if sum_one < sum_two:
    return True

  # Handle < and = if define in equal
  if equal and sum_one == sum_two:
    return True

  return False



"""
name        : display_vulnerable_component(self, name, version):
description : display info about vulnerability from the file
"""
def display_vulnerable_component(name, version, file):
    # Load json file
    with open('database/' + file + '.json') as data_file:
      data = json.load(data_file)

    print warning("Name: %s - v%s" % (name, version))
    if name in data.keys():

      # Display the out of date info if the version is lower of the latest version
      if is_lower(version, data[name]['latest_version'], False):
        print info("The version is out of date, the latest version is %s" % data[name]['latest_version'])

      # Display the vulnerability if it's not patched version
      for vuln in data[name]['vulnerabilities']:
        if 'fixed_in' in vuln.keys() and (vuln['fixed_in'] == None or is_lower(version, vuln['fixed_in'], True)):

          # Main informations
          print "\t",vulnerable("%s : %s - ID:%s" % (vuln['vuln_type'], vuln['title'] , vuln['id']) )
          print "\t",display("Fixed in %s"% vuln['fixed_in'])

          # Display references
          print "\t",display("References:")
          for refkey in vuln['references'].keys():
            for ref in vuln['references'][refkey]:
              if refkey != 'url':
                print "\t\t - %s %s" % (refkey.capitalize(), ref)
              else:
                print "\t\t - %s" %ref
