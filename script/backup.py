import requests
from lxml.html import *
from script import Contact

user_agent = Contact.userAgent()
proxy = Contact.proxy(None)
proxy = Contact.proxy(proxy)

dirs = ['/wp-content/', '/wp-content/backups/', '/wp-content/files/', '/wp-content/uploads/',
        '/wp-content/backup-wp/', '/wp-content/uploads/backups/', '/wp-content/uploads/local-backup/',
        '/wp-content/uploads/backup-database/', '/wp-content/uploads/indeed-backups/', '/wp-content/uploads/ithemes-security/backups/',
        '/wp-content/uploads/ceceppaml/backup/']

fileType = ['zip', 'rar', 'tar', 'sql', 'db']

def filesScan(host):
    found = False
    for path in dirs:
        req = requests.get(host+path, headers=user_agent,  proxies=proxy)
        check = req.status_code
        if check == 200:
            try:
                page = fromstring(req.content)
                urls = page.xpath('//@href')

                for link in urls:
                    for type in fileType:
                        if link.endswith(type):
                            print("[-] " + host + path + link)
                            found = True
            except:
                pass
    if found == False:
        print('[-] No Files Found!!')