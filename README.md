🔓 File Hrack

A fast and colorful archive password testing tool for RAR, ZIP, and 7Z archives using a wordlist.

Created by Sumon523022

---

📌 Features

- ✅ Supports RAR (".rar") archives
- ✅ Supports ZIP (".zip") archives
- ✅ Supports 7Z (".7z") archives
- ✅ Multi-threaded password testing
- ✅ Beautiful colorful terminal interface
- ✅ Progress bar with real-time status
- ✅ Automatically detects archive format
- ✅ Shows total attempts and execution time
- ✅ Password verification using test mode
- ✅ Optional 7Z extraction after finding the password
- ✅ Configurable thread count
- ✅ Works on Linux and Termux

---

📂 Supported Formats

Format| Extension| Supported
RAR| ".rar"| ✅ Yes
ZIP| ".zip"| ✅ Yes
7Z| ".7z"| ✅ Yes

---

📦 Requirements

Python 3.8 or newer

Required Python packages

pip install rarfile pyzipper tqdm

Install Archive Utilities

Debian / Ubuntu / Kali Linux

sudo apt update
sudo apt install unrar p7zip-full -y

Termux

pkg update && pkg upgrade -y
pkg install python unrar p7zip -y
pip install rarfile pyzipper tqdm

---

📁 Project Structure

project/
│
├── File_Hrack.py
├── README.md
├── passwords.txt
│
├── archive.rar
├── archive.zip
└── archive.7z

---

🚀 Usage

Basic Command

python File_Hrack.py -z archive.7z -p passwords.txt -o output

Termux Example

python File_Hrack.py \
-z /storage/emulated/0/BOT_Files/File_password_Hrack/1111.zip \
-p /storage/emulated/0/BOT_Files/File_password_Hrack/10k_password_list.1.txt \
-o /storage/emulated/0/BOT_Files/File_password_Hrack/

---

⚙️ Arguments

Argument| Description| Default
"-z"| Archive file path| Required
"-p"| Password wordlist path| Required
"-o"| Output directory| Required
"-t"| Number of threads| 4

---

📖 Examples

Example 1: RAR

python File_Hrack.py \
-z secret.rar \
-p passwords.txt \
-o output

Example 2: ZIP

python File_Hrack.py \
-z secret.zip \
-p passwords.txt \
-o output

Example 3: 7Z

python File_Hrack.py \
-z secret.7z \
-p passwords.txt \
-o output

Example 4: Using 8 Threads

python File_Hrack.py \
-z archive.7z \
-p passwords.txt \
-o output \
-t 8

---

🔐 7Z Extraction

When the correct password is found for a 7Z archive, the program asks:

? Extract now to output dir? [y/N]:

Enter "y" to extract the archive into the specified output directory.

Enter "n" to skip extraction.

Note: Automatic extraction is currently offered only for 7Z archives.

---

📋 Example Wordlist

123456
password
admin
hello123
qwerty
sumon
bangladesh

---

📺 Example Output

<<< Created by Sumon523022 >>>

Target: secret.7z
Format: .7z

Total passwords: 50000
Threads: 8

Testing passwords in test mode...

Cracking...

Password found: hello123

Time: 00:00:07
Attempts: 2486

? Extract now to output dir? [y/N]:

---

🛠️ How It Works

1. Detects the archive format automatically.
2. Loads passwords from the provided wordlist.
3. Tests passwords using multiple threads.
4. Stops after finding a matching password.
5. Displays the password, execution time, and attempts.
6. Offers extraction for 7Z archives.

---

⚠️ Notes

- Passwords are tested using a wordlist.
- Empty lines inside the wordlist are ignored.
- ZIP support requires "pyzipper".
- RAR support requires "unrar" and optionally "rarfile".
- 7Z support requires the "7z" command ("p7zip").
- ZIP testing currently extracts archive contents into the output directory to verify the password.
- RAR and 7Z use archive test operations.
- Extraction is not automatic for RAR and ZIP archives.
- Thread count can be customized using "-t".

---

💻 Tested Platforms

- Termux (Android)
- Ubuntu
- Debian
- Kali Linux

---

❤️ Author

Created by Sumon523022

---

📜 License

This project is provided for educational and personal use only.

Use it only on archives that you own or have explicit permission to test.

Unauthorized access to password-protected files may be illegal in your jurisdiction.
