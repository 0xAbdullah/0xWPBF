import requests
import json
from script import Contact
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
user_agent = Contact.userAgent()
proxy = Contact.proxy(None)
proxy = Contact.proxy(proxy)


def getUser(host):
    found = False
    for id in range(1, 25):
        try:
            req = requests.get(host+"/wp-json/wp/v2/users/"+str(id),
                               verify=False, headers = user_agent,  proxies=proxy).text # Insert your URL to extract
            getUser = json.loads(req)
            print('[-] ID: {}'.format(getUser['id']))
            print('[-] Name: {}'.format(getUser['name']))
            print('[-] Username: {}'.format(getUser['slug']))
            found = True
        except:
            pass
    if found == False:
        print('[-] No users found!')


def autoEnumeration(host):
    def getUserFromTitle():
        checkUser = (host + "/?author=")
        userID = 0
        global found
        found = False
        usernameList = []

        for i in checkUser:
            userID += 1
            check = (checkUser + str(userID))
            r = requests.get(check, verify=False, headers = user_agent,  proxies=proxy)
            tree = fromstring(r.content)
            username = tree.findtext('.//title')
            username = username.split(username, 0)[0]

            if '|' in username:
                username = username.split('|', 1)[0]
            elif '–' in username:
                username = username.split('–', 1)[0]
            elif '-' in username:
                username = username.split('-', 1)[0]
            elif ',' in username:
                username = username.split(',', 1)[0]
            if 'Page not found' in username:
                break
            if username not in usernameList:
                if userID == 1:
                    print('[*] ID\tUsername')
                found = True
                usernameList.append(username)

                print('[-] {}\t{}'.format(userID, username))
            else:
                break
            if found == False:
                print('\r[!] Users Not Found !', end='')

    def getUserFromURL():
        checkUser = (host + "/?author=")
        found = False
        userID = 0

        usernameList = []
        for i in checkUser:
            userID += 1
            check = (checkUser + str(userID))
            res = requests.get(check, allow_redirects=True, verify=False, headers = user_agent,  proxies=proxy)
            username = res.url.rsplit('/', 0)[-1]
            username = username.rsplit('/', 1)
            username = ''.join(username)
            username = username.rsplit('/', 1)[1]
            if "author" in username:
                if found:
                    break
                print("[=] There is a problem, the URL can not be traced")
                break

            found = True
            if username in usernameList:
                break
            usernameList.append(username)
            if userID == 1:
                print('[*] ID\tUsername')
            print('[-] {}\t{}'.format(userID, username))



    checkMethod = requests.get(host + "/?author=1", allow_redirects=False, verify=True, headers = user_agent,  proxies=proxy)

    if checkMethod.status_code == 301:
        getUserFromURL()
    else:
        getUserFromTitle()

