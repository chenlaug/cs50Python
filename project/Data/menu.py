import sys
import os
import hashlib

from Data.password_manager import PasswordManager
from Data.colorManager import Color, ColorManager
from Data.credential import Credential
from pyfiglet import Figlet
from tabulate import tabulate

class Menu:
    def __init__(self):
        pass

    def init(self) -> None:
        figlet = Figlet()
        print(figlet.renderText("PyCryptBox !"))
        self.__check_master_password()
        pm = self.__generate_key_password_manager()
        while True:
            self.__menu()
            try:
                self.__use_menu(int(ColorManager.input("Enter a command: \n")), pm)
            except ValueError as e:
                print()
                print(ColorManager.print(f"❌ Error: {e}", Color.RED))
            except KeyboardInterrupt:
                print()
                print(ColorManager.print("❌ Interrupted by user, exiting...", Color.RED))
                sys.exit(1)
            except EOFError:
                print()
                print(ColorManager.print("❌ End of file reached, exiting...", Color.RED))
                sys.exit(1)
            except FileNotFoundError as e:
                print()
                print(ColorManager.print(f"❌ Error: {e}", Color.RED))
    @staticmethod
    def __menu() -> None:
        print(ColorManager.print("✅ 1. Add a credential", Color.CYAN))
        print(ColorManager.print("🔍 2. Search for a credential", Color.CYAN))
        print(ColorManager.print("🔍 3. Search for a credential with the true password", Color.CYAN))
        print(ColorManager.print("❌ 4. Delete a credential", Color.CYAN))
        print(ColorManager.print("📋 5. List all credentials", Color.CYAN))
        print(ColorManager.print("🛠️ 6. Update a credentials", Color.CYAN))
        print(ColorManager.print("🚪 7. Exit", Color.CYAN))
        return None

    def __use_menu(self,command:int, pm:PasswordManager) -> None:
        match command:
            case 1:
                print(ColorManager.print("Add new credentials", Color.BLUE))
                pm.add_credential(
                    site=ColorManager.input("Enter the site name: "),
                    username=ColorManager.input("Enter the username: "),
                    password=ColorManager.input("Enter the password: ")
                )
                print(ColorManager.print("New credentials added", Color.GREEN))
                return None
            case 2:
                print(ColorManager.print("Search for a credential", Color.BLUE))
                credential = pm.find_credential(ColorManager.input("Enter the site name: "))
                if isinstance(credential, Credential):
                    print(ColorManager.print(f"Site: {credential.site} Username: {credential.username} Password: ****",
                                             Color.MAGENTA))
                return None
            case 3:
                print(ColorManager.print("Search for a credential with the true password", Color.BLUE))
                print(pm.show_credential_with_true_password(ColorManager.input("Enter the site name: ")))
                return None
            case 4:
                print(ColorManager.print("Delete a credential", Color.RED))
                print(pm.delete_credential(ColorManager.input("Enter the site name: ")))
                return None
            case 5:
                print(ColorManager.print("List all credentials", Color.BLUE))
                self.__show_credentials(pm)
                return None
            case 6:
                print(ColorManager.print("Update credentials...", Color.BLUE))
                print(ColorManager.print(pm.update_credential(ColorManager.input("Enter the site name: ", ),
                                                              ColorManager.input("Enter the new site: "),
                                                              ColorManager.input("Enter the new username: "),
                                                              ColorManager.input("Enter the new password: ")), Color.MAGENTA))
                return None
            case 7:
                print(ColorManager.print(" See you soon !", Color.MAGENTA))
                sys.exit(0)
            case _:
                raise ValueError("Invalid command, please enter a number between 1 and 7")
        return None

    @staticmethod
    def __show_credentials(pm:PasswordManager)-> None:
        credentials = pm.list_credentials()
        if credentials:
            data = [[c.site, c.username, c.password] for c in credentials]
            headers = ["Site", "Username", "Password"]
            print(tabulate(data, headers=headers, tablefmt="grid"))
        else:
            print(ColorManager.print("No credentials found.", Color.RED))

    def __check_master_password(self) -> None:
        if not os.path.exists("master.hash"):
            self.__setup_master_password()
        else:
            self.__verify_master_password()

    @staticmethod
    def __setup_master_password() -> None:
        print(ColorManager.print("No master password found. Please set one.", Color.YELLOW))
        password = ColorManager.input("Set a master password: ")
        salt = os.urandom(16)
        key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
        with open("master.hash", "wb") as f:
            f.write(salt + key)
        print(ColorManager.print("Master password set successfully.", Color.GREEN))

    @staticmethod
    def __verify_master_password() -> None:
        with open("master.hash", "rb") as f:
            data = f.read()
        salt, stored_key = data[:16], data[16:]
        for attempt in range(3):
            password = ColorManager.input("Enter master password: ")
            key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
            if key == stored_key:
                print(ColorManager.print("Access granted.", Color.GREEN))
                return
            remaining = 2 - attempt
            if remaining > 0:
                print(ColorManager.print(f"Wrong password. {remaining} attempt(s) left.", Color.RED))
        print(ColorManager.print("Too many failed attempts. Exiting.", Color.RED))
        sys.exit(1)

    @staticmethod
    def __generate_key_password_manager() -> PasswordManager:
        pm = PasswordManager()
        pm.generation_key()
        pm.load_key()
        pm.load()
        return pm