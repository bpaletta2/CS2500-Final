import sqlite3
import csv
import time
import pandas as pd 
import numpy as np
import datetime
import pwinput

from csv_to_sql import csv_to_sql

def login():
    username_check = False
    while username_check == False:
        username = input("Enter your username: ")
        cur.execute(f"SELECT * FROM user_account WHERE username = '{username}'")
        f = cur.fetchall()
        if len(f) == 0:
            print("User doesn't exist")
        if len(f) != 0:
            username_check = True

    while True:
        password = pwinput.pwinput("Enter password: ")
        cur.execute(f"SELECT password FROM user_account WHERE username =  '{username}'")
        f = cur.fetchone()
        if password == f[0]:
            print("Successful login\n")
            return username
        else:
            print("Incorrect password")

if __name__ == "__main__":
    csv_to_sql()
    conn = sqlite3.connect('final_project.db', isolation_level = None)
    cur = conn.cursor()
    username = login()

    while True:
        print("a) Read all user information")
        print("b) Modify Account")
        print("c) Deposit / withdraw money")
        print("d) Make a credit payment")
        print("e) Exit")
        # print("z) Admin")
        print("")

        user_input = input("Enter your choice: ")

        if user_input == "a":
            print("")

        elif user_input == "b":
            print("")

        elif user_input == "c":
            print("")

        elif user_input == "d":
            print("")

        elif user_input == "e":
            print("")
            print("Exiting app...")
            print("")
            break

        # elif user_input == "z":
        #     print("")

        else:
            print("Invalid input, try again")
            print("")

    cur.commit()
    cur.close()

