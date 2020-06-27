# Write your code here
import random
import sys
import sqlite3


class Card:
    def __init__(self, number_self=None, pin_self=None, balance=0):
        self.number = self.generate_number() if number_self is None else number_self
        self.pin = "{:04d}".format(random.randint(0, 9999)) if pin_self is None else pin_self
        self.balance = balance
        # Card.cards.insert(self)
        print("Your card has been created")
        print(f"Your card number:\n{self.number}")
        print(f"Your card PIN:\n{self.pin}")

    def generate_number(self):
        is_valid_generated_num = False
        result = ''
        while is_valid_generated_num is False:
            numbers = [4, 0, 0, 0, 0, 0]
            for i in range(9):
                numbers.append(random.randint(0, 9))
            luhnNum = self.calculate_luhn_num(numbers)
            # print("luhnNum {} and numbers {}".format(luhnNum,numbers))
            numbers.append(luhnNum)
            ss = [str(numbers[i]) for i in range(len(numbers))]
            result = str.join("", ss)
            is_valid = self.check_if_valid(result)
            if is_valid: break
        return result

    def calculate_luhn_num(self, numbers: list):
        l = numbers.copy()
        for i in range(0, len(numbers)):
            if (i + 1) % 2 == 1:
                l[i] *= 2
                if l[i] > 9:
                    l[i] -= 9

        sum_ = sum(l)
        return 10 - sum_ % 10

    @staticmethod
    def addACard():
        Database.insert(Card())

    @staticmethod
    def authen(num, pin):
        return Database.authen(num, pin)

    def logged_in(self):
        while True:
            print("1. Balance")
            print("2. Add income")
            print("3. Do transfer")
            print("4. Close account")
            print("5. Log out")
            print("0. Exit")
            c = int(input())
            if c == 0:
                sys.exit("")
            elif c == 1:
                print(f"Balance: {self.balance}")
            elif c == 2:
                self.add_in_come()
            elif c == 3:
                self.transfer()
            elif c == 4:
                self.close_account()
                break
            elif c == 5:
                break
            # print(self)

    def add_in_come(self):
        print("Enter income:")
        income_ = int(input())
        conn = sqlite3.connect('card.s3db')
        c = conn.cursor()
        c.execute(f"UPDATE card SET balance = balance + {income_} WHERE number = {self.number}")
        conn.commit()
        conn.close()
        self.balance += income_
        print("Income was added!")

    def close_account(self):
        conn = sqlite3.connect('card.s3db')
        c = conn.cursor()
        c.execute(f"DELETE FROM card WHERE number = {self.number}")
        conn.commit()
        conn.close()

    def transfer(self):
        print('Transfer')
        print("Enter card number:")
        transfer_number = input()
        is_valid = self.check_if_valid(transfer_number)
        print(is_valid)
        if is_valid is False:
            print("Probably you made mistake in card number. Please try again!")
            return
        conn_ = sqlite3.connect('card.s3db')
        c_ = conn_.cursor()
        found_card = None
        for found in c_.execute(f"SELECT * FROM card"):
            if found[1] == transfer_number:
                found_card = Card(found[1], found[2], found[3])
                break
        if found_card is None:
            print("Such a card does not exist.")
            return
        print("Enter how much money you want to transfer:")
        count = int(input())
        found_card: Card = found_card
        if count > self.balance:
            print("Not enough money!")
        else:
            c_.execute(
                f"UPDATE card SET balance = balance + {count} WHERE number = {found_card.number}")
            c_.execute(f"UPDATE card SET balance = balance - {count} WHERE number = {self.number}")

        conn_.commit()
        conn_.close()
        self.balance -= count
        print("Success!")

    def check_if_valid(self, transfer_number):
        origin_numbers = list(map(int, list(transfer_number[:len(transfer_number)])))
        numbers_l = list(map(int, list(transfer_number[:len(transfer_number) - 1])))
        print(numbers_l)
        for i in range(0, len(numbers_l)):
            if (i + 1) % 2 == 1:
                numbers_l[i] *= 2
                if numbers_l[i] > 9:
                    numbers_l[i] -= 9

        sum_ = sum(numbers_l)
        print("luhn expect {} ".format((10 - sum_ % 10)))
        print("luhn actual {}".format(origin_numbers[len(origin_numbers) - 1]))
        return (10 - sum_ % 10) == origin_numbers[len(origin_numbers) - 1]


class Database:

    @staticmethod
    def insert(card: Card):
        conn = sqlite3.connect('card.s3db')
        c = conn.cursor()
        c.execute(f"""INSERT INTO card (id, number, pin, balance) 
        VALUES({random.randint(0, 9999)},{card.number},{card.pin},{card.balance} )""")

        conn.commit()
        conn.close()

    @staticmethod
    def create():
        conn = sqlite3.connect('card.s3db')
        c = conn.cursor()
        c.execute(
            '''CREATE TABLE IF NOT EXISTS card (id INTEGER, number text, pin text, balance INTEGER DEFAULT 0)''')
        conn.commit()
        conn.close()

    @staticmethod
    def authen(num, pin):
        conn = sqlite3.connect('card.s3db')
        c = conn.cursor()
        for row in c.execute('SELECT * FROM card'):
            if row[1] == num and row[2] == pin:
                conn.close()
                found_card = Card(row[1], row[2], row[3])

                return found_card
        conn.commit()
        conn.close()
        return None


while True:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    Database.create()
    choice = int(input())
    if choice == 0:
        conn = sqlite3.connect('card.s3db')
        c = conn.cursor()
        for row in c.execute('SELECT * FROM card'):
            print("Row {}".format(row))
        conn.commit()
        conn.close()
        print("Bye!")
        break
    elif choice == 1:
        Card.addACard()
    elif choice == 2:
        number = input("Enter your card number:\n")
        pin = input("Enter your PIN:\n")
        card = Card.authen(number.strip(), pin.strip())
        if card is not None:
            if type(card) is Card:
                card: Card = card
                print("You have successfully logged in!")
                card.logged_in()
        else:
            print("Wrong card number or PIN!")
