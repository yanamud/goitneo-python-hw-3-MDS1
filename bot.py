from models import AddressBook, Record
from collections import defaultdict
from datetime import datetime
import calendar


def input_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError as e:
            return e
        except ValueError as e:
            return e
    return wrapper

# parsing of the entered command


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# adding new contact


@input_errors
def add_contact(*args, contacts):
    name = args[0]
    phone = args[1]
    if name in contacts:
        contacts[name].add_phone(args[1])
        return "Contact updated."
    else:
        contacts.add_record(Record(name, phone=phone))
        return "Contact added."

# changing contact


@input_errors
def change_contact(*args, contacts):
    name = args[0]
    old_phone = args[1]
    new_phone = args[2]

    if name in contacts:
        rec = contacts[name]
        rec.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        return "The entered name was not found"

# phone number output


@input_errors
def show_phone(*args, contacts):
    name = args[0]
    if name in contacts.keys():
        res = contacts[name]
        record = str(res).split(',')
        return (f"{record[0]}, {record[2]}")
    else:
        return "The entered name was not found"

# output all data


@input_errors
def show_all(*args, contacts):
    return contacts

# adding birthday


@input_errors
def add_birthday(*args, contacts):
    name = args[0]

    if name in contacts.keys():
        contacts[name].add_birthday(args[1])
        return (f"Birthday {args[1]} added success to contact {name}")
    else:
        contacts.add_record(Record(name, birthday=args[1]))
        return "Contact added."

# birthday output


@input_errors
def show_birthday(*args, contacts):
    name = args[0]
    if name in contacts.keys():
        res = contacts[name]
        record = str(res).split(',')
        return (f"{record[0]}, {record[1]}")
    else:
        return "The entered name was not found"

 # output the list of birthdays during the week


@input_errors
def get_birthdays_per_week(*args, contacts):

    dic = defaultdict(list)
    today = datetime.today().date()
    for key, value in contacts.items():
        lst = str(value).replace(',', '').replace("'", '').split()
        res = str(lst).replace(',', '').split()
        name = key
        birthday = str(res[4]).replace("'", '').split("-")
        bd = datetime(int(birthday[0]), int(birthday[1]), int(birthday[2]))
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

    DELIMITER_LEN = 50

    contacts = AddressBook()

    greeting_message_parts = (
        "Welcome to the assistant bot!",
        "-" * DELIMITER_LEN,
        "Please, enter a command:",
        "  - 'hello' to start the chat",
        "  - 'close'/'exit' to end the chat",
        "-" * DELIMITER_LEN
    )

    hello_message_parts = (
        "How can I help you?",
        "-" * DELIMITER_LEN,
        "Please, enter a command:",
        "  - 'add [username] [phone]' to added Contact",
        "  - 'change [username] [old phone] [new phone number]' to update Contact",
        "  - 'phone [username]' to get the phone number",
        "  - 'all' to output all the data",
        "  - 'add-birthday [username] [birthday]' to adde birthday",
        "  - 'show-birthday [username]' to get birthday",
        "  - 'birthdays' to display all birthdays within a week",
        "-" * DELIMITER_LEN
    )

    print("\n".join(greeting_message_parts))

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("\n".join(hello_message_parts))

        elif command == "add":
            print(add_contact(*args, contacts=contacts))

        elif command == "change":
            print(change_contact(*args, contacts=contacts))

        elif command == "phone":
            print(show_phone(*args, contacts=contacts))

        elif command == "all":
            print(show_all(contacts=contacts))

        elif command == "add-birthday":
            print(add_birthday(*args, contacts=contacts))

        elif command == "show-birthday":
            print(show_birthday(*args, contacts=contacts))

        elif command == "birthdays":
            print(get_birthdays_per_week(contacts=contacts))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
