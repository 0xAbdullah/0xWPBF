import requests, re, sys
from lxml.html import *
from script import Contact

user_agent = Contact.userAgent()
proxy = Contact.proxy(None)
proxy = Contact.proxy(proxy)

def title(host):
    r = requests.get(host, headers = user_agent,  proxies=proxy)
    tree = fromstring(r.content)
    siteTitle = tree.findtext('.//title')
    if '|' in siteTitle:
        siteTitle = siteTitle.split('|', 1)[0]
    elif '–' in siteTitle:
        siteTitle = siteTitle.split('–', 1)[0]
    elif '-' in siteTitle:
        siteTitle = siteTitle.split('-', 1)[0]
    return siteTitle

def dirAndFile(host):
    listPath = ["/robots.txt", "/license.txt", "/readme.html", "/xmlrpc.php", "/error_log", "/installer-log.txt", "/.wp-config.php.swp",
                "/wp-includes","/wp-content", "/wp-content/backup-db","/wp-content/uploads" , "/wp-content/debug.log", "/wp-admin/error_log"]
    print('[=] STATU   URL')
    for path in listPath:

        try:

            check = requests.get(host + path, headers=user_agent, proxies=proxy).status_code
            if check == 404:
                pass
            elif check == 200:
                status = ('[-]  {}    {}{} '.format(check, host, path))
                print(status)
            else:
                status = ('[-]  {}    {}{} '.format(check, host, path))
                print(status)

        except:
            print('[-] There is no response from the server   {}{}'.format(host, path))

def version(host):
    checkVersion = requests.get(host, headers = user_agent,  proxies=proxy).text
    checkVersion = re.search('WordPress ([0-9]+\.[0-9]+\.?[0-9]*)', (str(checkVersion)))
    try:
        checkVersion = checkVersion.group(0)
        checkVersion = re.sub("WordPress ", "", checkVersion)
        checkVersion = ['[-] Wordpress Version: ', checkVersion]
        checkVersion = ''.join(checkVersion)
    except :
        checkVersion = '[-] Wordpress Version: None'
    return checkVersion

def theme(host):
    req = requests.get(host, headers = user_agent,  proxies=proxy)
    page = fromstring(req.content)
    urls = page.xpath('//link/@href')
    for checkVersion in urls:

        if '/wp-content/themes/' and '/style.css' in checkVersion:
            themeName = checkVersion.rsplit('/', -3)[5]
            if themeName == 'themes':
                themeName = checkVersion.rsplit('/', -3)[6]
            themeVersion = checkVersion.rsplit('/', 2)[-1]
            themeVersion = re.search('([0-9]+\.[0-9]+\.?[0-9]*)', (str(themeVersion)))
            try:
                print('[-] Theme Name: {}'.format(themeName))
            except:
                print('[-] Theme Name: None')
            try:
                print('[-] Theme Version: {}'.format(themeVersion.group(0)))
            except:
                print('[-] Theme Version: None')
            break

def checkWP(host):
    found = False
    req = requests.get(host, headers = user_agent,  proxies=proxy)
    page = fromstring(req.content)
    urls = page.xpath('//@href')

    for check in urls:
        if '/wp-content/' in check:
            found = True
    if found == False:
        sys.exit('[!] This website does not using Wordpress')

def headersInfo(host):
    req = requests.get(host, headers = user_agent,  proxies=proxy)
    try:
        print('[-] Server: {}'.format(req.headers['Server']))
    except:
        print('[-] Serer: Unknown')
    try:
        print('[-] Link: {}'.format(req.headers['Link']))
    except:
        print('[-] Link: None')