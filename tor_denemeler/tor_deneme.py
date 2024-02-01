
import requests

session = requests.session()
session.proxies = {}

r = session.get('http://httpbin.org/ip')
print(r.text)

session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

r = session.get('http://httpbin.org/ip')
print(r.text)



