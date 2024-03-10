import pickle
from datetime import datetime, timedelta

class Birthday:
    def __init__(self, value):
        try:
            self.__value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    @property
    def value(self):
        return self.__value


class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []
        self.birthday = None

    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def add_phone(self, phone):
        if len(phone) == 10 and phone.isdigit():
            self.phones.append(phone)
            return True
        else:
            print("Invalid phone number format. Use 10 digits.")
            return False


class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name):
        return Record(name)

    def find_contact(self, name):
        for contact in self.contacts:
            if contact.name == name:
                return contact
        return None

    def get_upcoming_birthdays(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []
        for contact in self.contacts:
            if contact.birthday:
                if contact.birthday.value.month == next_week.month and \
                        contact.birthday.value.day >= next_week.day:
                    upcoming_birthdays.append(contact)
        return upcoming_birthdays

    def add_birthday(self, name, value):
        contact = self.find_contact(name)
        if contact:
            contact.add_birthday(value)
        else:
            print("Contact not found.")

    def show_birthday(self, name):
        contact = self.find_contact(name)
        if contact and contact.birthday:
            print(f"{contact.name}'s birthday: {contact.birthday.value.strftime('%d.%m.%Y')}")
        else:
            print("Birthday not found.")

    def birthdays(self):
        upcoming_birthdays = self.get_upcoming_birthdays()
        if upcoming_birthdays:
            print("Upcoming birthdays:")
            for contact in upcoming_birthdays:
                print(f"{contact.name}'s birthday: {contact.birthday.value.strftime('%d.%m.%Y')}")
        else:
            print("No upcoming birthdays.")

    def add_phone(self, name, phone):
        contact = self.find_contact(name)
        if contact:
            if contact.add_phone(phone):
                print(f"Phone {phone} added for {name}.")
            else:
                print("Failed to add phone number.")
        else:
            print("Contact not found.")

def add_birthday(args, book):
    if len(args) != 2:
        print("Invalid command format. Use: add-birthday [name] [DD.MM.YYYY]")
        return
    name, value = args
    book.add_birthday(name, value)


def show_birthday(args, book):
    if len(args) != 1:
        print("Invalid command format. Use: show-birthday [name]")
        return
    name = args[0]
    book.show_birthday(name)


def birthdays(args, book):
    book.birthdays()


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def main():
    book = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            if len(args) != 2:
                print("Invalid command format. Use: add [name] [phone]")
                continue
            name, phone = args
            contact = book.find_contact(name)
            if contact:
                if contact.add_phone(phone):
                    print(f"Contact {name} added with phone {phone}.")
                else:
                    print("Failed to add contact.")
            else:
                contact = book.add_contact(name)
                if contact:
                    if contact.add_phone(phone):
                        book.contacts.append(contact)
                        print(f"Contact {name} added with phone {phone}.")
                    else:
                        print("Failed to add contact.")
                else:
                    print("Failed to add contact.")

        elif command == "change":
            if len(args) != 2:
                print("Invalid command format. Use: change [name] [new_phone]")
                continue
            name, new_phone = args
            book.add_phone(name, new_phone)

        elif command == "phone":
            if len(args) != 1:
                print("Invalid command format. Use: phone [name]")
                continue
            name = args[0]
            contact = book.find_contact(name)
            if contact:
                if contact.phones:
                    print(f"{contact.name}'s phone numbers: {', '.join(contact.phones)}")
                else:
                    print(f"No phone numbers found for {contact.name}.")
            else:
                print("Contact not found.")

        elif command == "all":
            for contact in book.contacts:
                print(contact.name)

        elif command == "add-birthday":
            add_birthday(args, book)

        elif command == "show-birthday":
            show_birthday(args, book)

        elif command == "birthdays":
            birthdays(args, book)

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
