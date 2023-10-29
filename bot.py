from models import AddressBook, Record

def input_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError as e:
            return e
        except ValueError as e:
            return e
    return wrapper


#parsing of the entered command
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


#adding new contact
@input_errors
def add_contact(*args, contacts):
    name = args[0]
    phone = args[1]
    contacts.add_record(Record(name, phone=phone))
    return "Contact added."


#changing contact
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


#phone number output
@input_errors
def show_phone(*args, contacts):
    name = args[0]
    if name in contacts.keys():
        return contacts[name]
    else:
        return "The entered name was not found"


#output all data   
@input_errors
def show_all(*args, contacts):
    return contacts


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

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()