def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Invalid input"
    return wrapper

@input_error
def add_contact_handler(contacts, name, phone):
    contacts[name] = phone
    return f"Contact {name} with phone number {phone} added."

@input_error
def change_contact_handler(contacts, name, phone):
    if name in contacts:
        contacts[name] = phone
        return f"Phone number for {name} updated."
    else:
        return f"Contact {name} not found."

@input_error
def phone_handler(contacts, name):
    if name in contacts:
        return f"The phone number for {name} is {contacts[name]}."
    else:
        return f"Contact {name} not found."

@input_error
def show_all_handler(contacts):
    if contacts:
        result = "Contacts:\n"
        for name, phone in contacts.items():
            result += f"{name}: {phone}\n"
        return result.strip()
    else:
        return "No contacts found."


def main():
    contacts = {}

    while True:
        command = input("Enter a command: ").strip().lower()

        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            command_parts = command.split()
            if len(command_parts) >= 3:
                name = command_parts[1]
                phone = " ".join(command_parts[2:])
                result = add_contact_handler(contacts, name, phone)
                print(result)
        elif command.startswith("change"):
            command_parts = command.split()
            if len(command_parts) >= 3:
                name = command_parts[1]
                phone = " ".join(command_parts[2:])
                result = change_contact_handler(contacts, name, phone)
                print(result)
        elif command.startswith("phone"):
            command_parts = command.split()
            if len(command_parts) >= 3:
                name = command_parts[1]
                phone = " ".join(command_parts[2:])
            result = phone_handler(contacts, name)
            print(result)
        elif command.startswith("show all"):
            result = show_all_handler(contacts)
            print(result)
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()