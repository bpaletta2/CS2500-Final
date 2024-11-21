import sqlite3
import os
import pwinput
import pandas as pd

from csv_to_sql import csv_to_sql

def read_account(username):
    # If admin, list everything
    if username == "admin":
        cur.execute("SELECT * FROM user_account")
        account = pd.DataFrame(cur.fetchall(), columns=[description[0] for description in cur.description])
        cur.execute("SELECT * FROM bank_account")
        checking = pd.DataFrame(cur.fetchall(), columns=[description[0] for description in cur.description])
        cur.execute("SELECT * FROM credit_card")
        credit = pd.DataFrame(cur.fetchall(), columns=[description[0] for description in cur.description])
        cur.execute("SELECT * FROM purchase")
        purchase = pd.DataFrame(cur.fetchall(), columns=[description[0] for description in cur.description])
        print("User accounts: " + "\n")
        print(account)
        print("")
        print("Checking accounts: " + "\n")
        print(checking)
        print("")
        print("Credit cards: " + "\n")
        print(credit)
        print("")
        print("Purchases: " + "\n")
        print(purchase)
        print("")
    # List specific user info
    else:
        cur.execute(f"SELECT bank_id FROM user_account WHERE username = '{username}'")
        bank_id = cur.fetchone()[0]
        cur.execute(f"SELECT * FROM user_account WHERE username = '{username}'")
        account = pd.DataFrame(cur.fetchall(), columns=[description[0] for description in cur.description])
        cur.execute(f"SELECT * FROM bank_account WHERE bank_id = '{bank_id}'")
        checking = pd.DataFrame(cur.fetchall(), columns=[description[0] for description in cur.description])
        cur.execute(f"SELECT * FROM credit_card WHERE bank_id = '{bank_id}'")
        credit = pd.DataFrame(cur.fetchall(), columns=[description[0] for description in cur.description])
        cur.execute(f"SELECT * FROM purchase WHERE bank_id = '{bank_id}'")
        purchase = pd.DataFrame(cur.fetchall(), columns=[description[0] for description in cur.description])
        print("User accounts: " + "\n")
        print(account)
        print("")
        print("Checking accounts: " + "\n")
        print(checking)
        print("")
        print("Credit cards: " + "\n")
        print(credit)
        print("")
        print("Purchases: " + "\n")
        print(purchase)
        print("")

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
    if not os.path.exists("final_project.db"):
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
            read_account(username)
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

    cur.close()

