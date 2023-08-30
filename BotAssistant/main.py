from collections import UserDict

class Field:
    def __init__(self, value=None):
        self.value = value

    def validate(self):
        pass  # Implement validation logic here if needed

class Name(Field):
    def validate(self):
        if not self.value:
            raise ValueError("Name is required.")

class Phone(Field):
    def validate(self):
        if self.value and not isinstance(self.value, list):
            raise ValueError("Phone must be a list of phone numbers.")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.fields = {
            "phone": Phone()
        }

    def add_phone(self, phone_number):
        if "phone" not in self.fields:
            self.fields["phone"] = Phone([phone_number])
        else:
            if self.fields["phone"].value is None:
                self.fields["phone"].value = [phone_number]
            else:
                self.fields["phone"].value.append(phone_number)

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]

    def find_records(self, **kwargs):
        results = []
        for record in self.data.values():
            match = True
            for key, value in kwargs.items():
                if key in record.fields and record.fields[key].value != value:
                    match = False
                    break
            if match:
                results.append(record)
        return results

def main():
    address_book = AddressBook()

    while True:
        command = input("Enter a command: ").strip().lower()

        if command == "hello":
            print("How can I help you?")
        
        elif command.startswith("add"):
            command_parts = command.split()
            if len(command_parts) >= 3:
                name = command_parts[1]
                phone = " ".join(command_parts[2:])
                
                if name not in address_book:
                    record = Record(name)
                    record.add_phone(phone)
                    address_book.add_record(record)
                    print(f"Contact {name} with phone number {phone} added.")
                else:
                    print(f"Contact {name} already exists.")

        elif command.startswith("change"):
            command_parts = command.split()
            if len(command_parts) >= 3:
                name = command_parts[1]
                phone = " ".join(command_parts[2:])
                
                if name in address_book:
                    record = address_book[name]
                    record.fields["phone"].value = [phone]
                    print(f"Phone number for {name} updated.")
                else:
                    print(f"Contact {name} not found.")
        
        elif command.startswith("phone"):
            command_parts = command.split()
            if len(command_parts) >= 2:
                name = command_parts[1]
                
                if name in address_book:
                    record = address_book[name]
                    phone = record.fields.get("phone")
                    if phone:
                        print(f"The phone number for {name} is {', '.join(phone.value)}.")
                    else:
                        print(f"No phone number found for {name}.")
                else:
                    print(f"Contact {name} not found.")
        
        elif command.startswith("show all"):
            if address_book:
                result = "Contacts:\n"
                for name, record in address_book.items():
                    phone = record.fields.get("phone")
                    phone_str = ", ".join(phone.value) if phone else "No phone"
                    result += f"{name}: {phone_str}\n"
                print(result.strip())
            else:
                print("No contacts found.")

        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
