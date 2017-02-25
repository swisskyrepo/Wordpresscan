# Wordpresscan
A simple Wordpress scanner written in python
```
WORK IN PROGRESS - DO NOT USE
```

## Disclaimer
```
The author of this github is not responsible for misuse or for any damage that you may cause!
You agree that you use this software at your own risk.
```


# Output example from a test environment
```bash
_______________________________________________________________ 
 _    _               _                                         
| |  | |             | |                                        
| |  | | ___  _ __ __| |_ __  _ __ ___  ___ ___  ___ __ _ _ __  
| |/\| |/ _ \| '__/ _` | '_ \| '__/ _ \/ __/ __|/ __/ _` | '_ \ 
\  /\  / (_) | | | (_| | |_) | | |  __/\__ \__ \ (_| (_| | | | |
 \/  \/ \___/|_|  \__,_| .__/|_|  \___||___/___/\___\__,_|_| |_|
                       | |                                      
                       |_|                                      
 Wordpress scanner based on wpscan work - @pentest_swissky      
_______________________________________________________________ 
[0m[+] URL: http://localhost/wp_target 
[0m
[91m[!] The Wordpress 'http://localhost/wp_target/readme.html' file exposing a version number: 3.2.1[0m
[91m[!] Debug log file found: http://localhost/wp_target/debug.log[0m
[91m[!] A wp-config.php backup file has been found in: http://localhost/wp_target/wp-config.php.bak[0m
[93m[i] Uploads directory has directory listing enabled : http://localhost/wp_target/wp-content/uploads/[0m
[93m[i] Includes directory has directory listing enabled : http://localhost/wp_target/wp-includes/[0m
[0m[+] robots.txt available under: http://localhost/wp_target/robots.txt [0m
[0m[+] 	Interesting entry from robots.txt: Disallow: /wp-admin/[0m
[0m[+] 	Interesting entry from robots.txt: Disallow: /wp-includes/[0m
[0m[+] 	Interesting entry from robots.txt: Disallow: /wordpress/admin/[0m
[0m[+] 	Interesting entry from robots.txt: Disallow: /wordpress/wp-admin/[0m
[0m[+] 	Interesting entry from robots.txt: Disallow: /wordpress/secret/[0m
[0m[+] 	Interesting entry from robots.txt: Disallow: /Wordpress/wp-admin/[0m
[0m[+] 	Interesting entry from robots.txt: Disallow: /wp-admin/tralling-space/ [0m

[93m[i] Full Path Disclosure (FPD) in http://localhost/wp_target/wp-includes/rss-functions.php exposing /home/web/www/blog/wordpress/wp-includes/rss-functions.php[0m
[0m[+] WordPress version 3.2.1 identified from advanced fingerprinting[0m

[93m[i] 	REDIRECT : WordPress 3.0 - 3.6 Crafted String URL Redirect Restriction Bypass - ID:5970[0m
[0m[+] 	Fixed in 3.6.1[0m
[0m[+] 	References:[0m
		 - http://packetstormsecurity.com/files/123589/
		 - http://core.trac.wordpress.org/changeset/25323
		 - http://www.gossamer-threads.com/lists/fulldisc/full-disclosure/91609
		 - Exploitdb 28958
		 - Cve 2013-4339
		 - Secunia 54803

[93m[i] 	SSRF : WordPress 1.5.1 - 3.5 XMLRPC Pingback API Internal/External Port Scanning - ID:5988[0m
[0m[+] 	Fixed in 3.5.1[0m
[0m[+] 	References:[0m
		 - https://github.com/FireFart/WordpressPingbackPortScanner
		 - Cve 2013-0235

[...]

[93m[i] 	UNKNOWN : WordPress <= 4.7 - Post via Email Checks mail.example.com by Default - ID:8719[0m
[0m[+] 	Fixed in 4.7.1[0m
[0m[+] 	References:[0m
		 - https://github.com/WordPress/WordPress/commit/061e8788814ac87706d8b95688df276fe3c8596a
		 - https://wordpress.org/news/2017/01/wordpress-4-7-1-security-and-maintenance-release/
		 - Cve 2017-5491

[93m[i] 	CSRF : WordPress 2.8-4.7 - Accessibility Mode Cross-Site Request Forgery (CSRF) - ID:8720[0m
[0m[+] 	Fixed in 4.7.1[0m
[0m[+] 	References:[0m
		 - https://github.com/WordPress/WordPress/commit/03e5c0314aeffe6b27f4b98fef842bf0fb00c733
		 - https://wordpress.org/news/2017/01/wordpress-4-7-1-security-and-maintenance-release/
		 - Cve 2017-5492

[93m[i] 	UNKNOWN : WordPress 3.0-4.7 - Cryptographically Weak Pseudo-Random Number Generator (PRNG) - ID:8721[0m
[0m[+] 	Fixed in 4.7.1[0m
[0m[+] 	References:[0m
		 - https://github.com/WordPress/WordPress/commit/cea9e2dc62abf777e06b12ec4ad9d1aaa49b29f4
		 - https://wordpress.org/news/2017/01/wordpress-4-7-1-security-and-maintenance-release/
		 - Cve 2017-5493
```

## Install & Launch
```bash
git clone https://github.com/swisskyrepo/Wordpresscan.git
cd Wordpresscan
python main.py -u "http://localhost/wordpress" --update
```

## Credits and Contributor
 