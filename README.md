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
python main.py -u "http://localhost/wordpress" --update --aggressive
-u : Url of the WordPress
--update : Update the wpscan database
--aggressive : Launch an aggressive version to scan for plugins/themes
```

## Output example from a test environment
![alt tag](https://github.com/swisskyrepo/Wordpresscan/blob/master/screens/Version%204.4.7.png?raw=true)


## Credits and Contributor
* Original idea and script from [WPScan Team](https://wpscan.org/)