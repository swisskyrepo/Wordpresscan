# Wordpresscan
A simple Wordpress scanner written in python based on the work of WPScan (Ruby version)

## Disclaimer
```
The author of this github is not responsible for misuse or for any damage that you may cause!
You agree that you use this software at your own risk.
```


## Install & Launch
Dependencies
```
pip install requests
pip install tornado
```

Install
```bash
git clone https://github.com/swisskyrepo/Wordpresscan.git
cd Wordpresscan
```

Example 1 : Basic update and scan of a wordpress
```
python main.py -u "http://localhost/wordpress" --update --random-agent

-u : Url of the WordPress
--update : Update the wpscan database
--aggressive : Launch an aggressive version to scan for plugins/themes
--random-agent : Use a random user-agent for this session
```

Example 2 : Basic bruteforce
```
python main.py -u "http://127.0.0.1/wordpress/" --brute fuzz/wordlist.lst
python main.py -u "http://127.0.0.1/wordpress/" --brute admin

--brute file.lst : Will bruteforce every username and their password
--brute username : Will bruteforce the password for the given username
it will also try to bruteforce the password for the detected users.
```

Example 3 : Thinking is overrated, this is aggressive, mostly not advised!
```
python main.py -u "http://127.0.0.1/wordpress/" --fuzz

[i] Enumerating components from aggressive fuzzing ...
[i] File: http://127.0.0.1/wordpress/license.txt - found
[i] File: http://127.0.0.1/wordpress/readme.html - found
[i] File: http://127.0.0.1/wordpress/wp-admin/admin-footer.php - found
[i] File: http://127.0.0.1/wordpress/wp-admin/css/ - found
[i] File: http://127.0.0.1/wordpress/wp-admin/admin-ajax.php - found
[i] File: http://127.0.0.1/wordpress/wp-activate.php - found
--fuzz :  Will fuzz the website in order to detect as much file, themes and plugins as possible
```

## Output example from a test environment
![alt tag](https://github.com/swisskyrepo/Wordpresscan/blob/master/screens/Version%204.4.7.png?raw=true)


## Credits and Contributor
* Original idea and script from [WPScan Team](https://wpscan.org/)
