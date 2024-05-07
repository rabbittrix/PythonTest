import os
import requests
from time import sleep

def main():
    change = int(input("Afer how many seconds do you want to change the IP address? "))
    os.system("service tor start")
    url = "https://httpbin.org/ip"
    proxy = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
    
    while True:
        request = requests.get(url, proxies=proxy)
        if request.status_code == 200:
            print("your current IP :: {}".format(request.json().get('origin')))
        else:
            print("failed to get current IP")
        sleep(change)
        os.system("service tor reload")
        
if __name__ == "__main__":
    main()