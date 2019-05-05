# 0xWPBF
Wordpress users enumerate and brute force attack
# screenshot
![](https://raw.githubusercontent.com/0xAbdullah/0xWPBF/master/screenshot/Screenshot1.png)
# Installation
```bash
1) git clone https://github.com/0xAbdullah/0xWPBF.git
```
# Usage
```bash
python3 0xwpbf.py -url http://example.com
[E] Quick scan of the website to identify <Theme & version, WordPress version, Plugins & version, Scanning for Files and Directories, active user>
python3 0xwpbf -url http://example.com -u admin -p passwordlist.txt
[--] Launch a WordPress Bruteforce Attack.

  -h, --help    show this help message and exit
  -url URL      This argument is used to specify the URL of the target
                WordPress site.
  -u U          Use this to specify the WordPress username.
  -p P          Use this to specify the name of the password dictionary file.
  -m M          Methods for brute force.
  -proxy PROXY  Supply a proxy. HTTP, HTTPS.
```
### Coded By
```bash
Abdullah AlZahrani
Twitter : 0xAbdullah
```
