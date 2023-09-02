import re
from datetime import datetime
from collections import UserDict
import pickle
import os

class Field:
    def __init__(self, value=None):
        self._value = value

    def validate(self):
        pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.validate()

class Name(Field):
    def validate(self):
        if not self.value:
            raise ValueError("Name is required.")
        if not re.match(r'^[a-zA-Z]+$', self.value):
            raise ValueError("Name should only contain Latin letters.")

class Phone(Field):
    def validate(self):
        if self.value:
            if not re.match(r'^\+\d+$', self.value):
                raise ValueError("Invalid phone number format. It should start with '+' and contain digits.")

    @property
    def value(self):
        return ', '.join(self._value) if self._value else None

    @value.setter
    def value(self, new_value):
        if new_value:
            new_value = new_value.split(', ')
            for number in new_value:
                if not re.match(r'^\+\d+$', number):
                    raise ValueError("Invalid phone number format. It should start with '+' and contain digits.")
        self._value = new_value

class Birthday(Field):
    DATE_FORMAT = "%Y-%m-%d"

    def validate(self):
        if self.value:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', self.value):
                raise ValueError("Invalid birthday format. It should be YYYY-MM-DD.")

    def days_to_birthday(self):
        if self.value:
            today = datetime.today()
            birthday = datetime.strptime(self.value, self.DATE_FORMAT)
            next_birthday = datetime(today.year, birthday.month, birthday.day)

            if next_birthday < today:
                next_birthday = datetime(today.year + 1, birthday.month, birthday.day)

            days_remaining = (next_birthday - today).days
            return days_remaining
        return None

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.fields = {
            "phone": Phone(phone),
            "birthday": Birthday(birthday)
        }

    def add_phone(self, phone_number):
        if "phone" not in self.fields:
            self.fields["phone"] = Phone(phone_number)
        else:
            if self.fields["phone"].value is None:
                self.fields["phone"].value = phone_number
            else:
                current_value = self.fields["phone"].value
                if phone_number not in current_value.split(', '):
                    current_value += ', ' + phone_number
                    self.fields["phone"].value = current_value
                else:
                    raise ValueError("Phone number already exists for this record.")

    def show_birthday(self):
        if "birthday" in self.fields:
            return self.fields["birthday"].value
        return None

class AddressBook(UserDict):
    def __init__(self, page_size=5):
        super().__init__()
        self.page_size = page_size
        self.page = 0

    def add_record(self, record):
        self.data[record.name.value] = record

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]

    def find_records(self, query):
        results = []
        for record in self.data.values():
            match = False
            if query in record.name.value.lower():
                match = True
            phone = record.fields.get("phone")
            if phone and query in phone.value.lower():
                match = True
            if match:
                results.append(record)
        return results


    def __iter__(self):
        self.page = 0
        return self

    def __next__(self):
        start = self.page * self.page_size
        end = start + self.page_size
        page_records = list(self.data.values())[start:end]

        if not page_records:
            raise StopIteration

        self.page += 1
        return page_records
    
def save_data_on_exit(address_book, filename):
    with open(filename, 'wb') as file:
        pickle.dump(address_book, file)    

def load_data_on_start(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    else:
        return AddressBook()
    

def main():
    data_filename = 'address_book_data.pkl'

    address_book = load_data_on_start(data_filename)

    while True:
        command = input("Enter a command: ").strip().lower()

        if command == "hello":
            print("How can I help you?")

        elif command.startswith("add"):
            command_parts = command.split()
            if len(command_parts) >= 2:
                name = command_parts[1]
                phones = []
                birthday = None

                for part in command_parts[2:]:
                    if str(part).startswith("+"):
                        phones.append(part)
                    elif str(part).startswith("b"):
                        birthday = part[1:]

                if name not in address_book:
                    record = Record(name)

                    for phone in phones:
                        record.add_phone(phone)

                    if birthday:
                        record.fields["birthday"].value = birthday

                    address_book.add_record(record)
                    print(f"Contact {name} added.")
                else:
                    print(f"Contact {name} already exists.")
            else:
                print("Invalid format. Please provide at least a name.")

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

        elif command == "show all":
            if not address_book:
                print("---------------")
            else:
                for page_records in address_book:
                    for record in page_records:
                        print(f"Name: {record.name.value}")
                        phone = record.fields.get("phone")
                        if phone:
                            print(f"Phone: {phone.value}")
                        birthday = record.fields.get("birthday")
                        if birthday:
                            print(f"Birthday: {birthday.value}")
                        print("-" * 30)

        elif command.startswith("days to birthday"):
            name = input("Enter the name: ").strip().lower()
            if name in address_book:
                record = address_book[name]
                birthday_field = record.fields.get("birthday")
        
                if birthday_field is not None and birthday_field.value is not None:
                    days_remaining = birthday_field.days_to_birthday()
                    if days_remaining is not None:
                        print(f"Days to birthday for {name}: {days_remaining} days.")
                    else:
                        print(f"No valid birthday date found for {name}.")
                else:
                    print(f"No birthday date found for {name}.")
            else:
                print(f"Contact {name} not found.")
        
        elif command.startswith("find"):
            search_query = input("Enter search query: ").strip().lower()
            matching_records = address_book.find_records(query=search_query)
            if matching_records:
                print("Matching contacts:")
                for record in matching_records:
                    print(f"Name: {record.name.value}")
                    phone = record.fields.get("phone")
                    if phone:
                        print(f"Phone: {phone.value}")
                    birthday = record.fields.get("birthday")
                    if birthday:
                        print(f"Birthday: {birthday.value}")
                    print("-" * 30)
            else:
                print("No matching contacts found.")

        elif command in ["good bye", "close", "exit"]:
            save_data_on_exit(address_book, data_filename)
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()