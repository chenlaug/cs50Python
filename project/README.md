# PyCryptBox

## Video Demo: <URL HERE>

## Description

PyCryptBox is a secure command-line password manager written in Python. It lets you store, retrieve, update, and delete credentials (site, username, password) with real encryption. Access to the application is protected by a master password, and all stored passwords are encrypted with Fernet symmetric encryption.

## Features

- 🔑 Master password protection at startup (PBKDF2-HMAC-SHA256, 3 attempts max)
- 🔐 Add credentials — password is encrypted before storage
- 🔍 Search a credential by site name
- 👁️ View a credential with its decrypted password
- 🗑️ Delete a credential
- 🛠️ Update an existing credential (site, username, or password)
- 📋 List all credentials in a formatted table
- 🌈 Colored terminal interface with `colorama`
- 💾 Credentials persisted to `passwords.json`

## Project Structure

```
project/
├── Data/
│   ├── __init__.py
│   ├── colorManager.py        # Color enum and ColorManager class
│   ├── credential.py          # Credential class with validation
│   ├── menu.py                # Menu class — CLI logic and master password
│   ├── password_manager.py    # PasswordManager — encryption and persistence
│   ├── test_ColorManager.py
│   ├── test_Credential.py
│   ├── test_menu.py
│   └── test_PaswordManager.py
├── project.py                 # Entry point
├── test_project.py
├── requirements.txt
├── README.md
├── key.key                    # Generated on first run
├── master.hash                # Generated on first run
└── passwords.json             # Generated on first run
```

## How It Works

On the **first run**, the app asks you to set a master password. It hashes it with PBKDF2-HMAC-SHA256 (random 16-byte salt, 100 000 iterations) and stores the result in `master.hash`.

On every subsequent run, you have **3 attempts** to enter the correct master password. After 3 failures, the app exits.

Passwords are encrypted with **Fernet** (AES-128-CBC + HMAC). The encryption key is stored in `key.key` and never leaves your machine.

## Why These Choices

- `cryptography` (Fernet) — industry-standard symmetric encryption, simple and secure.
- `hashlib.pbkdf2_hmac` — standard library, no extra dependency, solid for password hashing.
- `colorama` — colored CLI feedback without complexity.
- `tabulate` — readable table display for credential lists.
- Class-based architecture (`Credential`, `PasswordManager`, `Menu`, `ColorManager`) — each class has a single responsibility, easy to test independently.

## Installation

```bash
pip install -r requirements.txt
```

## Run the Program

```bash
python project.py
```

## Run Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=Data --cov=project
```

## Author

- [Laughan Chenevot](https://github.com/chenlaug)
- [GitHub Repository](https://github.com/chenlaug/cs50Python)
- [LinkedIn](https://www.linkedin.com/in/laughan-chenevot/)
