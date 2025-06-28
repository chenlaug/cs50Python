# PyCryptBox
## Video Demo:  <URL HERE>
## Description:
    This project is a secure password manager developed in Python. It enables users to safely store, retrieve, add, update, and delete credentials (including website, username, and password) using encryption. The program runs in a command-line interface with a user-friendly menu, enhanced by colored output and tabular formatting for better readability.
## Features:
- 🔐 Add new credentials (site, username, password)
- 🔍 Search credentials by site name or username
- 🗑️ Delete credentials from the list
- 🧠 Encrypt and decrypt passwords using the `cryptography` library
- 📋 Display credentials in a clean table format using `tabulate`
- 🛠️ Update existing credentials (site, username, or password)
- 🌈 Colorful terminal interface with `colorama`

## Project Structure:
```md
├── Data
│   ├── ColorEnum.py
│   ├── Credential.py
│   └── PasswordManager.py
├── project.py
├── README.md
├── requirements.txt
├── key.key
└── passwords.json

1 Directory, 8 files
```

## Why these Choices ?
- `cryptography` ensures secure and industry-standard encryption.
- `colorama` improves the user experience with colored CLI feedback.
- `tabulate` displays credentials in a readable table format.
- Using classes and separation of concerns makes the code modular and maintainable.
- Tests ensure reliability and catch regressions early.

## Installation:
 ````bash
    pip install -r requirements.txt
 ````

## Run the Program:
```bash
    python project.py
```

## Run tests:
```bash
    pytest
```

## Author:
- [Laughan Chenevot](<https://github.com/chenlaug>)
- [GitHub Repository](<https://github.com/chenlaug/cs50Python>)
- [LinkedIn Profile](<https://www.linkedin.com/in/laughan-chenevot/>)

