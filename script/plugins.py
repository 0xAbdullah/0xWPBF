import requests, re
from lxml.html import *
from script import Contact

user_agent = Contact.userAgent()
proxy = Contact.proxy(None)
proxy = Contact.proxy(proxy)

def plugin(host):
    req = requests.get(host, headers = user_agent,  proxies=proxy)
    page = fromstring(req.content)
    urls = page.xpath('//@href')
    pluginsList = []
    found = False

    for checkPlugins in urls:
        if '/wp-content/plugins/' in checkPlugins:
            try:
                pluginsName = checkPlugins.rsplit('/', -3)[5]
                if pluginsName == 'plugins':
                    pluginsName = checkPlugins.rsplit('/', -3)[7]
                elif pluginsName == 'wp-content':
                    pluginsName = checkPlugins.rsplit('/', -3)[7]
                pluginsVersion = checkPlugins.rsplit('/', 2)[-1]
                pluginsVersion = re.search('([0-9]+\.[0-9]+\.?[0-9]*)', (str(pluginsVersion)))

                if pluginsName not in pluginsList:
                    found = True
                    pluginsList.append(pluginsName)
                    print('[-] Plugin: {} v{}'.format(pluginsName, pluginsVersion.group(0)))
            except:
                pass

    if found:
        pass
    else:
        print("[-] No Plugins Found!")