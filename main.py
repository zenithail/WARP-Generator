import threading
import random
import httpx
import os
import time
import requests
from colorama import Fore

ppkeys = requests.get('https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/24pbgen/base_keys')
pkeys = ppkeys.content.decode('UTF8')
keys = pkeys.split(',')
gkeys = []

print(Fore.RED + " _    _  ___  ____________   _____  _____ _   _ ")
print(Fore.BLUE + "| |  | |/ _ \ | ___ \ ___ \ |  __ \|  ___| \ | |")
print(Fore.YELLOW + "| |  | / /_\ \| |_/ / |_/ / | |  \/| |__ |  \| |")
print(Fore.MAGENTA + "| |/\| |  _  ||    /|  __/  | | __ |  __|| . ` |")
print(Fore.GREEN + "\  /\  / | | || |\ \| |     | |_\ \| |___| |\  |")
print(Fore.CYAN + " \/  \/\_| |_/\_| \_\_|      \____/\____/\_| \_/")
print("")
print(Fore.WHITE + "           ----> t.me/skxuhq             ")

def generate_key(thread_num, total_keys, keys_per_thread):
    global gkeys

    try:
        headers = {
            "CF-Client-Version": "a-6.11-2223",
            "Host": "api.cloudflareclient.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.1",
        }

        keys_generated = 0

        while keys_generated < keys_per_thread:
            with httpx.Client(base_url="https://api.cloudflareclient.com/v0a2223",
                              headers=headers,
                              timeout=30.0) as client:

                r = client.post("/reg")
                id = r.json()["id"]
                license = r.json()["account"]["license"]
                token = r.json()["token"]

                r = client.post("/reg")
                id2 = r.json()["id"]
                token2 = r.json()["token"]

                headers_get = {"Authorization": f"Bearer {token}"}
                headers_get2 = {"Authorization": f"Bearer {token2}"}
                headers_post = {
                    "Content-Type": "application/json; charset=UTF-8",
                    "Authorization": f"Bearer {token}",
                }

                json = {"referrer": f"{id2}"}
                client.patch(f"/reg/{id}", headers=headers_post, json=json)

                client.delete(f"/reg/{id2}", headers=headers_get2)

                key = random.choice(keys)

                json = {"license": f"{key}"}
                client.put(f"/reg/{id}/account", headers=headers_post, json=json)

                json = {"license": f"{license}"}
                client.put(f"/reg/{id}/account", headers=headers_post, json=json)

                r = client.get(f"/reg/{id}/account", headers=headers_get)
                account_type = r.json()["account_type"]
                referral_count = r.json()["referral_count"]
                license = r.json()["license"]

                client.delete(f"/reg/{id}", headers=headers_get)
                gkeys.append(license)
                print(f"{Fore.GREEN}[+] {license}")
                f = 'keys.txt'
                with open(f, 'a') as file:
                    file.write(str(f"{license}\n"))

                keys_generated += 1

            if thread_num % 2 == 0:
                time.sleep(60)

    except:
        time.sleep(15)

num_threads = int(input(f"{Fore.CYAN}[+] Enter the number of threads to use:\n "))
keys_per_thread = int(input(f"{Fore.CYAN}[+] Enter the number of keys to generate per thread:\n "))

total_keys = keys_per_thread * num_threads

threads = []
for i in range(num_threads):
    thread = threading.Thread(target=generate_key, args=(i + 1, total_keys, keys_per_thread))
    threads.append(thread)
    thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    for thread in threads:
        thread.join()

os.system('cls' if os.name == 'nt' else 'clear')
for x in gkeys:
    print(Fore.GREEN + "[+]", x)

input('\n(Enter) to exit.\n')