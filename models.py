from collections import UserDict
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
        self.phones = [Phone(phone)] if phone else []

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
    
    def __str__(self) -> str:
        return "\n".join(str(rec) for rec in self.values())


if __name__ == '__main__':
    AddressBook.main()
