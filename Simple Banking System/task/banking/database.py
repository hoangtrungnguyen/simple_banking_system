import sqlite3


def calculate_luhn_num(numbers: list):
    l = numbers.copy()
    for i in range(0, len(numbers)):
        if (i + 1) % 2 == 1:
            l[i] *= 2
            if l[i] > 9:
                l[i] -= 9

    sum_ = sum(l)
    return 10 - sum_ % 10


a = calculate_luhn_num(list(map(int, list("3000003972196503"))))
print(a)


def check_if_valid(transfer_number):
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


b = check_if_valid("40000085555896010")
print(f"Valid {b}")

transfer_number = input()
conn = sqlite3.connect('card.s3db')
c = conn.cursor()
found_card = None
for found in c.execute(f"SELECT number FROM card"):
    print(found)
    # if found == transfer_number:
    #     found_card = found
    #     break

conn.commit()
conn.close()
