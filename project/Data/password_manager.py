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
        encrypted_password = self.__encrypt_password(password)
        credential = Credential(site, username, encrypted_password)
        self.credentials.append(credential)
        self.__save()

    def find_credential(self, site: str) -> Credential | None:
        site = site.lower()
        for credential in self.credentials:
            if credential.site == site:
                return credential
        raise ValueError(f"No login information found for the site: {site}")

    def show_credential_with_true_password(self, site: str) ->  str:
        cred = self.find_credential(site)
        return f"{cred.site}, Username: {cred.username}, Password: {self.__decrypt_password(cred.password)}"

    def delete_credential(self, site: str) -> str:
        site = site.lower()
        credential = self.find_credential(site)
        self.credentials.remove(credential)
        self.__save()
        return f"Credentials successfully deleted for the site: {site}"

    def update_credential(self, site: str, newSite:str, username:str, password:str) -> str:
        cred = self.find_credential(site)
        cred.site = newSite.strip() or cred.site
        cred.username = username.strip() or cred.username
        if password.strip():
            cred.password = self.__encrypt_password(password)
        self.__save()
        return f"Credentials successfully updated for the site: {newSite}"

    @staticmethod
    def generation_key():
        if not os.path.exists("key.key"):
            key = Fernet.generate_key()
            with open("key.key", "wb") as key_file:
                key_file.write(key)

    def load_key(self):
        with open("key.key", "rb") as key_file:
            self.key = key_file.read()
            self.fernet = Fernet(self.key)

    def list_credentials(self) -> list[Credential]:
        return list(self.credentials)

    def load(self, filepath="passwords.json"):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"The file {filepath} does not exist.")
        with open(filepath, "r") as f:
            data = json.load(f)
            self.credentials = [Credential.from_dict(entry) for entry in data]

    # private methode         
    def __encrypt_password(self, password: str) -> str:
        encrypted = self.fernet.encrypt(password.encode())
        return encrypted.decode()

    def __decrypt_password(self, token: str) -> str:
        decrypted = self.fernet.decrypt(token.encode())
        return decrypted.decode()

    def __save(self, filepath="passwords.json") -> None:
        data = [credential.to_dict() for credential in self.credentials]
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)