import os
import json
from cryptography.fernet import Fernet

from Data.credential import Credential


class PasswordManager:
    def __init__(self):
        self.credentials: list[Credential] = []
        self.key = None
        self.fernet = None

    def add_credential(self, site: str, username: str, password: str) -> None:
        site = site.lower()
        username = username.strip()
        password = password.strip()
        encrypted_password = self.encrypt_password(password)
        credential = Credential(site, username, encrypted_password)
        self.credentials.append(credential)

    def update_credential(self, site: str, choice: str, new_values: dict) -> str:
        for credential in self.credentials:
            if credential.site == site:
                if choice == "1":
                    credential.site = new_values.get("site", credential.site).lower()
                elif choice == "2":
                    credential.username = new_values.get("username", credential.username)
                elif choice == "3":
                    new_password = new_values.get("password")
                    if new_password:
                        credential.password = self.encrypt_password(new_password)
                elif choice == "4":
                    credential.site = new_values.get("site", credential.site).lower()
                    credential.username = new_values.get("username", credential.username)
                    password = new_values.get("password")
                    if password:
                        credential.password = self.encrypt_password(password)
                else:
                    return "Invalid choice."
                return "Credential updated successfully."
        return f"Identifier not found for the site: {site}"

    def find_credential(self, site: str) -> Credential | str:
        for credential in self.credentials:
            if credential.site == site:
                return credential
        return f"Identifier not found for the site: {site}"

    def delete_credential(self, site: str) -> str:
        for credential in self.credentials:
            if credential.site == site:
                self.credentials.remove(credential)
                return f"Credentials successfully deleted for the site: {site}"
        return f"No login information found for the site: {site}"

    def generation_key(self):
        if not os.path.exists("key.key"):
            key = Fernet.generate_key()
            with open("key.key", "wb") as key_file:
                key_file.write(key)

    def load_key(self):
        with open("key.key", "rb") as key_file:
            self.key = key_file.read()
            self.fernet = Fernet(self.key)

    def list_credentials(self) -> list[Credential]:
        return self.credentials

    def show_credential_with_true_password(self, site: str) -> str:
        cred = self.find_credential(site)
        if isinstance(cred, Credential):
            return f"{cred.site}, Username: {cred.username}, Password: {self.decrypt_password(cred.password)}"
        return "Not found"

    def encrypt_password(self, password: str) -> str:
        encrypted = self.fernet.encrypt(password.encode())
        return encrypted.decode()

    def decrypt_password(self, token: str) -> str:
        decrypted = self.fernet.decrypt(token.encode())
        return decrypted.decode()

    def get_decrypted_password(self, site: str) -> str:
        cred = self.find_credential(site)
        if isinstance(cred, Credential):
            return self.decrypt_password(cred.password)
        return cred

    def save(self, filepath="passwords.json"):
        data = [credential.to_dict() for credential in self.credentials]
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    def load(self, filepath="passwords.json"):
        if not os.path.exists(filepath):
            return
        with open(filepath, "r") as f:
            data = json.load(f)
            self.credentials = [Credential.from_dict(entry) for entry in data]
