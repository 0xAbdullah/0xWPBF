#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse, os, sys
from script import info
from script import Contact
from script import plugins
from script import Brute_Force
from script import username
from script import backup

print('''
    █▀▀█ █░█  █░░░█    █▀▀█     █▀▀▄     █▀▀
    █▄▀█ ▄▀▄  █▄█▄█ord █░░█ress █▀▀▄RUTE █▀▀ORCER
    █▄▄█ ▀░▀  ░▀░▀░    █▀▀▀     ▀▀▀░     ▀░░ v1.4
    0xWPBF v1.4 Coded By Abdullah AlZahrani | Website: www.xRedTeam.com
    Twitter: @0xAbdullah | GitHub.com/0xAbdullah
    ''')

parser = argparse.ArgumentParser(description="[--] 0xWPBF website scanner")
parser.add_argument('-url', required=True, default=None, help='This argument is used to specify the URL of the target WordPress site.')
parser.add_argument('-u', required=False, default=None, help='Use this to specify the WordPress username.')
parser.add_argument('-p', required=False, default=None, help='Use this to specify the name of the password dictionary file.')
parser.add_argument('-m', required=False, default=None, help='Methods for brute force.') # This feature will be in the next release
parser.add_argument('-proxy', required=False, default=None, help='Supply a proxy. HTTP, HTTPS.')

args = vars(parser.parse_args())

if len(sys.argv) == 1:
    sys.exit("[!] Usage: python3 0xwpbf.py -u http[s]://example.com")

host = args['url']
proxyInput = args['proxy']
method = args['m']
usernameBF = args['u']
wordlist = args['p']

if not host.startswith('http'):
    sys.exit("[!] Wrong URL format\n[>] EXAMPLE: http[s]://example.com")

if host.endswith('/'):
    host = host[:-1]

if proxyInput == None:
    proxyIP = Contact.proxy(None)
else:
    proxyIP = Contact.proxy(proxyInput)

info.checkWP(host)

if __name__ == '__main__':
    if host is not None and usernameBF is not None and wordlist is not None:
        if not os.path.exists(wordlist):
            print("[--] Password File Path Does Not exist !")
            sys.exit()
        if usernameBF == None:
            sys.exit("[--] Enter the username!")
        print('[-] Host: {}'.format(host))
        if method == None or method == 'wp-login':
            Brute_Force.wpLogin(host, method, usernameBF, wordlist)

    elif host is not None:
        print("[--] Information about your target")
        print('[-] Host: {}'.format(host))
        server = info.headersInfo(host)
        title = info.title(host)
        print('[-] Title: {}'.format(title))
        print(info.version(host))
        info.theme(host)
        print("\n[--] Scanning for Files and Directories")
        info.dirAndFile(host)
        print("\n[--] Scanning for [ZIP, RAR, TAR, SQL, DB] file")
        backup.filesScan(host)
        print("\n[--] Scanning for Plugins")
        plugins.plugin(host)
        print("\n[--] Scanning for active username/s automatically!")
        username.getUser(host)
