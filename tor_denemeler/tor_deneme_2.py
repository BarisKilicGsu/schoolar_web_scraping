import time
import requests
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
import random
proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}
print("IP adresini random 1-11 saniye arasında degistir....\n")
while True:
    headers = { 'User-Agent': UserAgent().random }
    time.sleep(random.randint(1,11))
    with Controller.from_port(port = 9051) as c:
        c.authenticate(password = "1805Sila")
        c.signal(Signal.NEWNYM)
        print(f"Your IP is : {requests.request('GET','https://ident.me', proxies=proxies, headers=headers).text}  ||  User Agent is : {headers['User-Agent']}")