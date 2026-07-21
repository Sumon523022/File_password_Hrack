# 🔓 File Hrack

A fast and colorful password testing tool for **RAR** and **ZIP** archives using a wordlist.

Created by **Sumon523022**

---

## 📌 Features

- ✅ Supports **RAR (.rar)** archives
- ✅ Supports **ZIP (.zip)** archives
- ✅ Multi-threaded password testing
- ✅ Beautiful colorful terminal interface
- ✅ Progress bar with real-time status
- ✅ Automatically detects archive format
- ✅ Shows total attempts and execution time
- ✅ Safe password testing
- ✅ Works on Linux and Termux

---

# 📂 Supported Formats

| Format | Supported |
|---------|-----------|
| RAR (.rar) | ✅ Yes |
| ZIP (.zip) | ✅ Yes |

---

# 📦 Requirements

Python 3.8 or newer

Required packages:

```bash
pip install rarfile pyzipper tqdm
```

For RAR archives, install **unrar**.

### Debian / Ubuntu

```bash
sudo apt install unrar
```

### Termux

```bash
pkg install unrar
```

---

# 📁 Project Structure

```
project/
│
├── file_hrack.py
├── README.md
├── passwords.txt
├── archive.rar
└── archive.zip
```

---

# 🚀 Usage

```
python file_hrack.py -z ARCHIVE -w WORDLIST -o OUTPUT_FOLDER
```

---

# ⚙ Arguments

| Argument | Description |
|----------|-------------|
| -z | Archive file (.rar or .zip) |
| -w | Password wordlist |
| -o | Output directory |
| -t | Number of threads (Default: 4) |

---

# 📖 Examples

## Example 1 (RAR)

```bash
python file_hrack.py \
-z secret.rar \
-w passwords.txt \
-o output
```

---

## Example 2 (ZIP)

```bash
python file_hrack.py \
-z secret.zip \
-w passwords.txt \
-o output
```

---

## Example 3 (Using 8 Threads)

```bash
python file_hrack.py \
-z archive.rar \
-w passwords.txt \
-o output \
-t 8
```

---

# 📋 Example Wordlist

```
123456
password
admin
hello123
qwerty
sumon
bangladesh
```

---

# 📺 Example Output

```
Created by Sumon523022

Target : secret.rar
Format : .rar

Total Passwords : 50000
Threads : 8

Cracking...
█████████████████████████

Password found:
hello123

Time:
00:00:07

Attempts:
2486
```

---

# 🛠 How It Works

1. Detects the archive format.
2. Loads every password from the wordlist.
3. Tests passwords using multiple threads.
4. Stops immediately when the correct password is found.
5. Displays execution time and total attempts.

---

# ⚠ Notes

- Passwords are tested only.
- Archives are **not extracted automatically**.
- ZIP support requires **pyzipper**.
- RAR support requires **unrar**.
- Empty lines inside the wordlist are ignored.

---

# 💻 Tested On

- Termux
- Ubuntu
- Debian
- Kali Linux

---

# ❤️ Author

**Created by Sumon523022**

---

# 📜 License

This project is provided for **educational and personal use only**.

Use it only on archives that you own or have explicit permission to test.

Unauthorized access to password-protected files may be illegal in your jurisdiction.