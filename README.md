# 0xWPBF
Wordpress users enumerate and brute force attack
# screenshot
![alt text](https://github.com/0xAbdullah/0xWPBF/blob/master/Screenshot.gif)
# Installation
```bash
1) git clone https://github.com/0xAbdullah/0xWPBF.git
2) pip install mechanicalsoup
```
# Usage
```bash
python 0xwpbf.py -s http://example.com
[--] The command above extracts username/s active on website automatically
python 0xwpbf -s http://example.com -e users.txt
[--] The above command guesses user names on website using a list of usernames
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

Website: www.0xa.tech

Twitter : 0xAbdullah
