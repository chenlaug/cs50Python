import sys

from tabulate import tabulate

from Data.colorManager import Color, ColorManager
from Data.credential import Credential
from Data.password_manager import PasswordManager
from pyfiglet import Figlet




def main() -> None:
    figlet = Figlet()
    print(figlet.renderText("PyCryptBox !"))
    pm = generate_key_password_manager()

    while True:
        menu()
        try:
            use_menu(ColorManager.input("➡️ Enter a command: \n"), pm)
            print(ColorManager.print("...", Color.MAGENTA))
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

def menu() -> None:
    print(ColorManager.print("✅ 1. Add a credential", Color.CYAN))
    print(ColorManager.print("🔍 2. Search for a credential", Color.CYAN))
    print(ColorManager.print("🔍 3. Search for a credential with the true password", Color.CYAN))
    print(ColorManager.print("❌ 4. Delete a credential", Color.CYAN))
    print(ColorManager.print("📋 5. List all credentials", Color.CYAN))
    print(ColorManager.print("🛠️ 6. Update a credentials", Color.CYAN))
    print(ColorManager.print("🚪 7. Exit", Color.CYAN))

def use_menu(command: str, pm: PasswordManager) -> None:
    match command.strip().lower():
        case "1":
            print(ColorManager.print("Add new credentials", Color.BLUE))
            pm.add_credential(
                site=ColorManager.input("Enter the site name: "),
                username=ColorManager.input("Enter the username: "),
                password=ColorManager.input("Enter the password: ")
            )
            pm.save()
        case "2":
            print(ColorManager.print("Search for a credential", Color.BLUE))
            credential = pm.find_credential(ColorManager.input("Enter the site name: "))
            if isinstance(credential, Credential):
                print(ColorManager.print(f"Site: {credential.site} Username: {credential.username} Password: {credential.password}", Color.MAGENTA))
            else:
                print(ColorManager.print(credential, Color.RED))
        case "3":
            print(ColorManager.print("Search for a credential with the true password", Color.BLUE))
            print(pm.show_credential_with_true_password(ColorManager.input("Enter the site name: ")))
        case "4":
            print(ColorManager.print("Delete a credential", Color.RED))
            print(pm.delete_credential(ColorManager.input("Enter the site name: ")))
        case "5":
            print(ColorManager.print("List all credentials", Color.BLUE))
            show_credentials(pm)
        case "6":
            print(ColorManager.print("Update credentials...", Color.BLUE))
            site = ColorManager.input("Enter the site name: ")
            credential = pm.find_credential(site)

            if not isinstance(credential, Credential):
                print(ColorManager.print(credential, Color.RED))
                return None

            print(ColorManager.print(
                f"Current → Site: {credential.site}, Username: {credential.username}, Password: {pm.decrypt_password(credential.password)}",
                Color.MAGENTA))

            print(ColorManager.print("1. Site", Color.CYAN))
            print(ColorManager.print("2. Username", Color.CYAN))
            print(ColorManager.print("3. Password", Color.CYAN))
            print(ColorManager.print("4. All", Color.CYAN))

            while True:
                try:
                    choice = ColorManager.input("What would you like to change? (1/2/3/4): ")
                    if choice not in {"1", "2", "3", "4"}:
                        raise ValueError("Invalid choice. Please enter 1, 2, 3, or 4.")

                    new_values = {}
                    if choice == "1":
                        new_values["site"] = ColorManager.input("Enter new site: ")
                    elif choice == "2":
                        new_values["username"] = ColorManager.input("Enter new username: ")
                    elif choice == "3":
                        new_values["password"] = ColorManager.input("Enter new password: ")
                    elif choice == "4":
                        new_values["site"] = ColorManager.input("Enter new site: ")
                        new_values["username"] = ColorManager.input("Enter new username: ")
                        new_values["password"] = ColorManager.input("Enter new password: ")

                    result = pm.update_credential(site, choice, new_values)
                    print(ColorManager.print(result, Color.GREEN if "successfully" in result else Color.RED))
                    pm.save()
                    break

                except ValueError as e:
                    print(ColorManager.print(f"❌ Error: {e}", Color.RED))
        case "7":
            print(ColorManager.print(" See you soon !", Color.MAGENTA))
            pm.save()
            sys.exit(0)
        case _:
            raise ValueError("❗ Unknown command, please try again.")

def show_credentials(pm: PasswordManager) -> None:
    credentials = pm.list_credentials()
    if credentials:
        data = [[c.site, c.username, c.password] for c in credentials]
        headers = ["Site", "Username", "Password"]
        print(tabulate(data, headers=headers, tablefmt="grid"))
    else:
        print(ColorManager.print("No credentials found.", Color.RED))


def generate_key_password_manager() -> PasswordManager:
    pm = PasswordManager()
    pm.generation_key()
    pm.load_key()
    pm.load()
    return pm



if __name__ == "__main__":
    main()
