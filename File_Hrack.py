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
    rarfile = None
    print("⚠️ rarfile not installed. RAR will not work. (pip install rarfile)")

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
    codes = ''.join(COLORS.get(s, '') for s in styles)
    return f"{codes}{text}{COLORS['reset']}"


def random_color():
    return random.choice([c for k, c in COLORS.items() if k not in ('reset', 'bold')])


# ======================== ব্যানার ========================
def print_banner():
    print(colorize("               <<< ", "bold", "white") +
          colorize("Created by Sumon523022 ", "bold", "light_red") +
          colorize(">>>", "bold", "white"))
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


# ======================== পাসওয়ার্ড টেস্ট ========================
def test_password(archive_path, password, output_dir, extension):
    try:
        if extension == '.rar':
            # rarfile দিয়ে দ্রুত টেস্ট
            if rarfile is not None:
                try:
                    with rarfile.RarFile(archive_path) as rf:
                        if hasattr(rf, 'test_password'):
                            return bool(rf.test_password(password))
                except Exception:
                    pass
            # fallback unrar
            cmd = ['unrar', 't', '-p' + password, archive_path]
            try:
                result = subprocess.run(cmd, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL, timeout=5)
                return result.returncode == 0
            except Exception:
                return False

        elif extension == '.zip' and HAS_ZIP:
            with pyzipper.AESZipFile(archive_path, 'r') as zf:
                zf.extractall(output_dir, pwd=password.encode('utf-8', errors='ignore'))
            return True

        elif extension == '.7z':
            # 7z টেস্ট মোড (কোনো এক্সট্রাকশন নয়, শুধু পাসওয়ার্ড যাচাই)
            cmd = ['7z', 't', f'-p{password}', archive_path, '-y']
            try:
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=15
                )
                return result.returncode == 0
            except subprocess.TimeoutExpired:
                return False
            except Exception:
                return False

        return False
    except Exception:
        return False


# ======================== মেইন ক্র্যাক ========================
def crack(archive_path, wordlist_path, output_dir, threads=4):
    print_banner()

    ext = os.path.splitext(archive_path)[1].lower()
    if ext not in ('.rar', '.zip', '.7z'):
        print(colorize("❌ Only .rar, .zip and .7z archives are supported.", "light_red"))
        return

    if ext == '.zip' and not HAS_ZIP:
        print(colorize("❌ pyzipper is not installed, cannot handle ZIP files.", "light_red"))
        return

    if ext == '.rar' and rarfile is None:
        print(colorize("⚠️ rarfile missing; falling back to unrar binary.", "light_yellow"))

    if ext == '.7z':
        # 7z ইনস্টল আছে কিনা চেক
        try:
            subprocess.run(['7z'], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=3)
        except FileNotFoundError:
            print(colorize("❌ '7z' command not found. Install: pkg install p7zip", "light_red"))
            return
        except Exception:
            pass

    if not os.path.isfile(archive_path) or not os.path.isfile(wordlist_path):
        print(colorize("❌ File(s) not found.", "light_red"))
        return

    os.makedirs(output_dir, exist_ok=True)

    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = [line.strip() for line in f if line.strip()]

    info_color = random.choice(['light_cyan', 'light_magenta', 'light_yellow', 'light_green'])
    print(colorize(f"[*] Target: {archive_path} | Format: {ext}", info_color))
    print(colorize(f"[*] Total passwords: {len(passwords)} | Threads: {threads}", info_color))
    print(colorize("[*] Testing passwords in test mode (no extraction)", "cyan"))
    print()

    start = time.time()
    found = None
    attempts = 0

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(test_password, archive_path, pwd, output_dir, ext): pwd
            for pwd in passwords
        }
        with tqdm(total=len(passwords),
                  desc=colorize("Cracking", "bold", "light_magenta"),
                  colour='green', unit='pwd') as progress_bar:
            for future in as_completed(futures):
                attempts += 1
                try:
                    ok = future.result()
                except Exception:
                    ok = False
                if ok:
                    found = futures[future]
                    for f in futures:
                        f.cancel()
                    break
                progress_bar.update(1)

    elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start))

    if found:
        print(colorize(f"\n✅ Password found: {found}", "bold", "light_green"))
        print(colorize("📁 (Not extracted automatically – you can extract it manually)", "light_yellow"))
        result_color = random.choice(['light_cyan', 'light_magenta', 'light_yellow'])
        print(colorize(f"   Time: {elapsed} | Attempts: {attempts}", result_color))

        # 7z হলে সরাসরি এক্সট্রাক্ট করার অপশন
        if ext == '.7z':
            try:
                ans = input(colorize("\n? Extract now to output dir? [y/N]: ",
                                     "bold", "light_cyan")).strip().lower()
            except (EOFError, KeyboardInterrupt):
                ans = 'n'
            if ans == 'y':
                extract_cmd = ['7z', 'x', f'-p{found}', archive_path,
                               f'-o{output_dir}', '-y']
                print(colorize("[*] Extracting...", "cyan"))
                subprocess.run(extract_cmd)
                print(colorize(f"✅ Extracted to: {output_dir}", "light_green"))
    else:
        print(colorize(f"\n❌ No matching password found.", "light_red"))
        print(colorize(f"   Time: {elapsed} | Attempts: {attempts}", "light_yellow"))


# ======================== CLI ========================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Password cracker for RAR/ZIP/7z archives using a wordlist.")
    parser.add_argument("-z", required=True, help="Archive file path (.rar/.zip/.7z)")
    parser.add_argument("-p", required=True, help="Wordlist file path")
    parser.add_argument("-o", required=True, help="Output directory")
    parser.add_argument("-t", type=int, default=4, help="Number of threads (default: 4)")
    args = parser.parse_args()

    crack(args.z, args.p, args.o, args.t)
