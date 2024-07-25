import os
import sys
import subprocess
import platform

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = [
    'aiohttp', 'colorama', 'tqdm', 'pyfiglet', 'psutil', 'requests', 'webbrowser'
]

print("Checking and installing required packages...")
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        install_package(package)

import json
import datetime
import random
import string
import time
import asyncio
import aiohttp
import threading
import webbrowser
from colorama import init, Fore, Style
from tqdm import tqdm
import pyfiglet
import psutil
import requests

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Define script version and window title
script_version = '6.0.0'
window_title = f"ULTRA WARP-PLUS-CLOUDFLARE (version {script_version})"

# Set window title based on OS
os.system(
    f'title {window_title}'
    if os.name == 'nt'
    else 'PS1="\\[\\e]0;' + window_title + '\\a\\]"; echo $PS1'
)

# Clear console screen based on OS
os.system('cls' if os.name == 'nt' else 'clear')

# Print cool ASCII art
ascii_banner = pyfiglet.figlet_format("WARP+", font="slant")
print(Fore.CYAN + Style.BRIGHT + ascii_banner)

print(Fore.GREEN + Style.BRIGHT + f"[+] ULTRA WARP-PLUS-CLOUDFLARE (version {script_version})")
print(Fore.YELLOW + "[-] With this script, you can obtain unlimited WARP+ referral data.")
print(Fore.MAGENTA + "[♡] Author: https://github.com/ChefAdorous | https://t.me/ChefAdorous")
print(Fore.CYAN + "=" * 70)

# Initialize user settings
referrer = ""
min_interval = 0.5  # Default minimum request interval (seconds)
max_interval = 3    # Default maximum request interval (seconds)
save_file = "warp_ultra.sav"
stop_flag = False
max_concurrent_requests = 10

# Load referral data and saved client IDs from script data structures
try:
    with open(save_file, "r") as f:
        referral_data = json.load(f)
except FileNotFoundError:
    referral_data = {
        "users": {},
        "total": {
            "total_referrals": 0
        }
    }

# Function to generate a random string
def genString(stringLength):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(stringLength))

# Function to generate a random digit string
def digitString(stringLength):
    return ''.join(random.choice(string.digits) for _ in range(stringLength))

# Define the API URL
url = f'https://api.cloudflareclient.com/v0a{digitString(3)}/reg'

# Asynchronous function to send a request to the API and handle the response
async def run(session, semaphore):
    async with semaphore:
        try:
            install_id = genString(22)
            body = {
                "key": f"{genString(43)}=",
                "install_id": install_id,
                "fcm_token": f"{install_id}:APA91b{genString(134)}",
                "referrer": referrer,
                "warp_enabled": False,
                "tos": f"{datetime.datetime.now().isoformat()[:-3]}+02:00",
                "type": "Android",
                "locale": "es_ES",
            }
            headers = {
                'Content-Type': 'application/json; charset=UTF-8',
                'Host': 'api.cloudflareclient.com',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'User-Agent': 'okhttp/3.12.1'
            }

            async with session.post(url, json=body, headers=headers) as response:
                if response.status == 200:
                    return True
                else:
                    return False
        except Exception as error:
            print(Fore.RED + f"Error: {error}")
            return False

# Function to update the log file with referral data
def update_log_file():
    with open(save_file, "w") as log_file:
        json.dump(referral_data, log_file, indent=2)

# Asynchronous function to start the script
async def start_script():
    global stop_flag, referral_data
    g = 0
    b = 0
    stop_flag = False

    print(Fore.YELLOW + "\n[*] Starting ULTRA WARP+ referral process...")
    
    semaphore = asyncio.Semaphore(max_concurrent_requests)
    
    async with aiohttp.ClientSession() as session:
        with tqdm(total=1000, bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET)) as pbar:
            while not stop_flag:
                tasks = [run(session, semaphore) for _ in range(max_concurrent_requests)]
                results = await asyncio.gather(*tasks)
                
                for result in results:
                    if result:
                        g += 1
                        if referrer in referral_data["users"]:
                            referral_data["users"][referrer][1] += 1
                        else:
                            referral_data["users"][referrer] = [referrer, 1]
                        referral_data["total"]["total_referrals"] += 1
                        update_log_file()
                        pbar.update(1)
                        pbar.set_description(f"Progress: {g} GB added")
                    else:
                        b += 1
                
                await asyncio.sleep(random.uniform(min_interval, max_interval))

        print(Fore.GREEN + f"\n[+] Total: {g} GB added successfully, {b} failed attempts")

# Function to check for the 's' key press to stop the script
def check_stop_key():
    global stop_flag
    while True:
        if input(Fore.YELLOW + "Press 's' and Enter to stop the script: ").strip().lower() == 's':
            stop_flag = True
            print(Fore.RED + "\n[!] Stopping the script...")
            break

# Function to open Telegram channel
def open_telegram_channel():
    webbrowser.open('https://t.me/VorTexCyberBD')
    print(Fore.GREEN + "[+] Opened Telegram channel in your default browser.")

# Function to check system resources
def check_system_resources():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    
    print(Fore.CYAN + "\n[+] System Resources:")
    print(f"CPU Usage: {cpu_percent}%")
    print(f"Memory Usage: {memory_percent}%")
    print(f"Disk Usage: {disk_percent}%")

# Function to check internet speed
def check_internet_speed():
    print(Fore.YELLOW + "\n[*] Checking internet speed...")
    speed_test_url = "http://speedtest.ftp.otenet.gr/files/test100k.db"
    start_time = time.time()
    response = requests.get(speed_test_url)
    end_time = time.time()
    
    file_size = len(response.content) / 1024  # KB
    duration = end_time - start_time
    speed = (file_size / duration) * 8 / 1024  # Mbps
    
    print(Fore.GREEN + f"[+] Download speed: {speed:.2f} Mbps")

# Main script loop
async def main():
    global referrer, min_interval, max_interval, max_concurrent_requests

    while True:
        print(Fore.CYAN + "\n[+] ULTRA WARP+ MENU:")
        print(Fore.WHITE + "1. Start Script")
        print("2. Set Request Interval")
        print("3. Set Referrer (User ID)")
        print("4. Display Referral Data")
        print("5. Open Telegram Channel")
        print("6. Check System Resources")
        print("7. Check Internet Speed")
        print("8. Set Max Concurrent Requests")
        print("9. Exit")

        choice = input(Fore.GREEN + "Enter your choice: ")

        if choice == '1':
            if not referrer:
                referrer = input(Fore.YELLOW + "Enter the Referrer (User ID): ")
            stop_thread = threading.Thread(target=check_stop_key)
            stop_thread.daemon = True
            stop_thread.start()
            await start_script()
        elif choice == '2':
            min_interval = float(input(Fore.YELLOW + "Enter Minimum Request Interval (seconds): "))
            max_interval = float(input(Fore.YELLOW + "Enter Maximum Request Interval (seconds): "))
        elif choice == '3':
            referrer = input(Fore.YELLOW + "Enter the Referrer (User ID): ")
        elif choice == '4':
            print(Fore.MAGENTA + "Referral Data:")
            print(json.dumps(referral_data, indent=2))
        elif choice == '5':
            open_telegram_channel()
        elif choice == '6':
            check_system_resources()
        elif choice == '7':
            check_internet_speed()
        elif choice == '8':
            max_concurrent_requests = int(input(Fore.YELLOW + "Enter Max Concurrent Requests: "))
        elif choice == '9':
            print(Fore.RED + "[+] Exiting the script.")
            break
        else:
            print(Fore.RED + "[!] Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    asyncio.run(main())
