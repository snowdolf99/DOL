import csv
import re

from dash_of_legends import dol

def read_csv_file(file_path):
    with open(file_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    return data

def write_csv_file(file_path, data):
    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data)

def is_natural_number(string):
    return bool(re.match('^[1-9][0-9]*$', string))

csv_path = "./my_data.csv"
csv_data = read_csv_file(csv_path)

while True:
    event = input("start, save or quit >> ").lower()

    if event == "start":
        while True:
            diff = input("difficulty ( only natural number ) >> ")
            if is_natural_number(diff):
                break
        diff = int(diff)
        exp = int(csv_data[1][1])
        life = int(csv_data[2][1])
        my_dol = dol(diff, exp, life)
        msg, life = my_dol.dungeon()
        if msg:
            print(f"{diff} clear")
            csv_data[0][1] = max(int(csv_data[0][1]), diff)
            csv_data[1][1] = exp + diff
            csv_data[2][1] = life
        else:
            print(f"{diff} fail")
            csv_data[0][1] = 1
            csv_data[1][1] = 1
            csv_data[2][1] = 10
            write_csv_file(csv_path, csv_data)

    elif event == "save":
        write_csv_file(csv_path, csv_data)
        print("save success")
        for data in csv_data:
            print(f"{data[0]:<6} : {data[1]}")

    elif event == "quit":
        break

    else:
        print("wrong input")