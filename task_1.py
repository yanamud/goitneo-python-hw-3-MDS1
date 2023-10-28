from collections import UserDict
import datetime
from datetime import datetime
from collections import defaultdict
import calendar


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, value):
        res = str(value).replace(',', '').split(' ')
        birthday = str(res[-1])
        if len(birthday) != 10:
            raise ValueError("Please enter birthday in format DD.MM.YYYY")
        
        birthday = birthday.split('.')
        bd = datetime(int(birthday[2]), int(birthday[1]), int(birthday[0]))
        super().__init__(value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not all((len(value) == 10, value.isdigit())):
            raise ValueError("The number should contain 10 digits")
        super().__init__(value)


class Record:
    def __init__(self, name, birthday=None, phone=None):
        self.name = Name(name)
        self.birthday = birthday
        self.phones = [phone] if phone else []

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        print(f"Birthday {birthday} added success to contact {self.name}")

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        print(f"Phone number {phone} added success to contact {self.name}")

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                del self.phones[self.phones.index(p)]
            return 'the phone was removed'
        else:
            return "The entered phone was not found"

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if str(p.value) == str(Phone(old_phone)):
                self.phones.insert(self.phones.index(p)+1, Phone(new_phone))
                del self.phones[self.phones.index(p)]
                print('the phone was changed')
        # else:
            # print("The entered phone was not found")

    def find_phone(self, found_phone):
        for p in self.phones:
            if p.value == found_phone:
                return found_phone

    def __str__(self):
        return f"Contact name: {self.name}, birthday: {self.birthday}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def parse_input(user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return "The entered name was not found"

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return "The record was removed"
        else:
            return "The entered name was not found"

    def get_birthdays_per_week(self):

        dic = defaultdict(list)
        today = datetime.today().date()
        for el in self.data:
            res = str(self.data[el]).replace(',', '').split()
            name = res[2]
            birthday = str(res[4]).split('.')
            bd = datetime(int(birthday[2]), int(birthday[1]), int(birthday[0]))
            birthday = bd.date()

            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year+1)

            delta_days = (birthday_this_year - today).days

            if delta_days < 7:
                if birthday_this_year.weekday() in (5, 6):
                    day = "0" + "_" + calendar.day_name[0]
                else:
                    day = str(birthday_this_year.weekday()) + "_" + \
                        calendar.day_name[birthday_this_year.weekday()]
                dic[day].append(name)

        for key, value in sorted(dic.items()):
            new_key = key[2:]
            new_value = ", ".join(value)
            print(f"{new_key}: {new_value}")

    def main():

        book = AddressBook()
        greet_message = "Welcome to the assistant bot!\n" \
                        "----------------------------------\n" \
                        "Please, enter a command:\n" \
                        "  - 'hello' to start the chat\n" \
                        "  - 'close' or 'exit' to end the chat\n" \
                        "----------------------------------\n" \
                        "                                  \n"

        help_message = "How can I help you?\n" \
            "----------------------------------\n" \
            "Please, enter a command:\n" \
            "  - 'add [username] [phone]' to adde Contact\n" \
            "  - 'change [username] [old phone number] [new phone number]' to update Contact\n" \
            "  - 'phone [username]' to get the phone number\n" \
            "  - 'all' to output all the data\n" \
            "  - 'add-birthday [username] [birthday]' to adde birthday \n" \
            "  - 'show-birthday [username]' to get birthday \n" \
            "  - 'birthdays' to display all birthdays within a week \n" \
            "----------------------------------\n" \
            "                                  \n" \

        print(greet_message)

        while True:
            user_input = input("Enter a command: ")
            command, *args = AddressBook.parse_input(user_input)
            # print(command, *args)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "hello":
                print(help_message)

            elif command == "add":
                record = Record(args[0])
                for name, record in book.data.items():
                    if name == args[0]:
                        print("contact exists ")
                    else:
                        record = Record(args[0])
                record.add_phone(args[1])
                book.add_record(record)

            elif command == "change":
                record = book.find(args[0])
                record.edit_phone(args[1], args[2])

            elif command == "phone":
                record = book.find(args[0])
                rec = str(record).split(',')
                print(f"{rec[0]}, {rec[2]}")


            elif command == "all":
                for name, record in book.data.items():
                    print(name, record)

            elif command == "add-birthday":
                record = Record(args[0])
                for name, record in book.data.items():
                    if name == args[0]:
                        print("contact exists ")
                    else:
                        record = Record(args[0])
                record.add_birthday(args[1])
                book.add_record(record)

            elif command == "show-birthday":
                record = book.find(args[0])
                rec = str(record).split(',')
                print(f"{rec[0]}, {rec[1]}")

            elif command == "birthdays":
                book.get_birthdays_per_week()

            else:
                print("Invalid command.")


if __name__ == '__main__':
    AddressBook.main()
