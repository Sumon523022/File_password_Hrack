#!/usr/bin/env python
import os
import time
import argparse
import sys
import subprocess
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

try:
    import rarfile
except ImportError:
    print("❌ rarfile not installed. Run: pip install rarfile")
    sys.exit(1)

try:
    import pyzipper
    HAS_ZIP = True
except ImportError:
    HAS_ZIP = False
    print("⚠️ pyzipper not installed. ZIP extraction will not work. (pip install pyzipper)")

# ======================== Bash-স্টাইল কালার কোড ========================
COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'light_red': '\033[91m',
    'light_green': '\033[92m',
    'light_yellow': '\033[93m',
    'light_blue': '\033[94m',
    'light_magenta': '\033[95m',
    'light_cyan': '\033[96m',
    'light_white': '\033[97m',
}

def colorize(text, *styles):
    """এক বা একাধিক স্টাইল প্রয়োগ করে (যেমন 'bold', 'light_red')"""
    codes = ''.join(COLORS.get(s, '') for s in styles)
    return f"{codes}{text}{COLORS['reset']}"

def random_color():
    """এলোমেলো একটি রঙ (reset বাদে)"""
    return random.choice(list(COLORS.values())[:-1])

# ======================== ব্যানার ========================
def print_banner():
    print(colorize("               <<< ", "bold", "white") +
          colorize("Created by Sumon523022 ", "bold", "light_red") +
          colorize(">>>", "bold", "white"))

    # File = Yellow, Hrack = Cyan
    print(colorize("       _____ _ _      ", "bold", "yellow") +
          colorize("       _   _               _", "bold", "cyan"))
    print(colorize("      |  ___(_) | ___", "bold", "yellow") +
          colorize("       | | | | __ _  ___ __| |", "bold", "cyan"))
    print(colorize("      | |_  | | |/ _ \\", "bold", "yellow") +
          colorize("      | |_| |/ _` |/ __/ _` |", "bold", "cyan"))
    print(colorize("      |  _| | | |  __/", "bold", "yellow") +
          colorize("      |  _  | (_| | (_| (_| |", "bold", "cyan"))
    print(colorize("      |_|   |_|_|\\___|", "bold", "yellow") +
          colorize("      |_| |_|\\__,_|\\___\\__,_|", "bold", "cyan"))

    print(colorize("               >>> ", "light_red") +
          colorize("One Tap Termux Customizer", "bold", "light_green"))
    print()

# ======================== পাসওয়ার্ড টেস্ট ফাংশন ========================
def test_password(archive_path, password, output_dir, extension):
    try:
        if extension == '.rar':
            try:
                with rarfile.RarFile(archive_path) as rf:
                    if hasattr(rf, 'test_password'):
                        if rf.test_password(password):
                            return True
                        else:
                            return False
            except:
                pass
            cmd = ['unrar', 't', '-p' + password, archive_path]
            try:
                result = subprocess.run(cmd, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL, timeout=5)
                return result.returncode == 0
            except:
                return False
        elif extension == '.zip' and HAS_ZIP:
            with pyzipper.AESZipFile(archive_path, 'r') as zf:
                zf.extractall(output_dir, pwd=password.encode('utf-8', errors='ignore'))
            return True
        else:
            return False
    except:
        return False

# ======================== মেইন ক্র্যাক ফাংশন ========================
def crack(archive_path, wordlist_path, output_dir, threads=4):
    print_banner()  # রঙিন ব্যানার প্রিন্ট

    ext = os.path.splitext(archive_path)[1].lower()
    if ext not in ('.rar', '.zip'):
        print(colorize("❌ Only .rar and .zip archives are supported.", "light_red"))
        return
    if ext == '.zip' and not HAS_ZIP:
        print(colorize("❌ pyzipper is not installed, cannot handle ZIP files.", "light_red"))
        return

    if not os.path.isfile(archive_path) or not os.path.isfile(wordlist_path):
        print(colorize("❌ File(s) not found.", "light_red"))
        return

    os.makedirs(output_dir, exist_ok=True)

    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = [line.strip() for line in f if line.strip()]

    # হেডার তথ্য – এলোমেলো রঙে
    info_color = random.choice(['light_cyan', 'light_magenta', 'light_yellow', 'light_green'])
    print(colorize(f"[*] Target: {archive_path} | Format: {ext}", info_color))
    print(colorize(f"[*] Total passwords: {len(passwords)} | Threads: {threads}", info_color))
    print(colorize("[*] Testing passwords using unrar (test mode – no extraction)", "cyan"))

    start = time.time()
    found = None
    attempts = 0

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(test_password, archive_path, pwd, output_dir, ext): pwd
                   for pwd in passwords}
        with tqdm(total=len(passwords),
                  desc=colorize("Cracking", "bold", "light_magenta"),
                  colour='green', unit='pwd') as progress_bar:
            for future in as_completed(futures):
                attempts += 1
                if future.result():
                    found = futures[future]
                    for f in futures:
                        f.cancel()
                    break
                progress_bar.update(1)

    elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start))

    if found:
        # সফল – বোল্ড সবুজ + এলোমেলো রঙে সময়/অ্যাটেম্পট
        print(colorize(f"\n✅ Password found: {found}", "bold", "light_green"))
        print(colorize("📁 (Not extracted automatically – you can extract it manually)", "light_yellow"))
        result_color = random.choice(['light_cyan', 'light_magenta', 'light_yellow'])
        print(colorize(f"   Time: {elapsed} | Attempts: {attempts}", result_color))
    else:
        print(colorize(f"\n❌ No matching password found.", "light_red"))
        print(colorize(f"   Time: {elapsed} | Attempts: {attempts}", "light_yellow"))

# ======================== কমান্ড-লাইন ইন্টারফেস ========================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Password cracker for RAR/ZIP archives using a wordlist.")
    parser.add_argument("-z", required=True, help="Archive file path")
    parser.add_argument("-w", required=True, help="Wordlist file path")
    parser.add_argument("-o", required=True, help="Output directory (used for ZIP extraction test)")
    parser.add_argument("-t", type=int, default=4, help="Number of threads (default: 4)")
    args = parser.parse_args()
    crack(args.z, args.w, args.o, args.t)