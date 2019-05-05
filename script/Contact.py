import requests, random, sys

def proxy(proxyIP):
    if proxyIP == None:
        proxy = None
        pass

    else:

        if proxyIP.startswith('https://'):
            proxy = {'https':proxyIP}
        elif proxyIP.startswith('http://'):
            proxy = {'http':proxyIP}

        else:
            sys.exit('[!] wrong format')
        myip = requests.get('https://api.ipify.org/?format=raw').text
        myproxy = requests.get('https://api.ipify.org/?format=raw', proxies=proxy).text

        if myip == myproxy:
            sys.exit('[!] KillSwitch: ON\nThe proxy dose not work!')

    return proxy

def userAgent():
    choose = open('script/user-agent.txt', 'r').readlines()
    randomUserAgent = random.choice(choose)
    user_agent = {'User-Agent': '{}'.format(randomUserAgent.strip())}
    return user_agent

