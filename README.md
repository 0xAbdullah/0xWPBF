# 0xWPBF
Wordpress users enumerate and brute force attack
# screenshot
![](https://raw.githubusercontent.com/0xAbdullah/0xWPBF/master/screenshot/Screenshot1.png)
![](https://raw.githubusercontent.com/0xAbdullah/0xWPBF/master/screenshot/Screenshot2.png)
![](https://raw.githubusercontent.com/0xAbdullah/0xWPBF/master/screenshot/Screenshot3.png)
# Installation
```bash
1) git clone https://github.com/0xAbdullah/0xWPBF.git
2) pip install mechanicalsoup
3) pip install PrettyTable
```
# Usage
```bash
python 0xwpbf.py -s http://example.com
[E] Quick scan of the website to identify <Theme & version, WordPress version, Plugins & version, Scanning for Files and Directories, active user>
python 0xwpbf -s http://example.com -e users.txt
[--] The command above guesses user names on website using a list of usernames
python 0xwpbf.py -s http://example.com -u username -p password.txt -t 5
[--] -u = Target username / -p = Path of password file / -t = Number of threads

  -h, --help  show this help message and exit
  -s S        Target Website.
  -p P        Password list / Path of password file.
  -u U        Target username.
  -e E        Guess usernames / Path of usernames file.
  -t T        Number of threads.



```
# Coded By
Abdullah AlZahrani

Twitter : 0xAbdullah

### G2:
Dr.Abolalh; Und3r-r00t; Dr.Silent; Null; xSecurity; TA Hacker; 1333Cyb3r; HitmanAlharbi; Ali AlZahrani; Saleh AlZahrani <3
