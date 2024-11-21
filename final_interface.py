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
        print("User accounts: \n")
        print(account)
        print("")
        print("Checking accounts: \n")
        print(checking)
        print("")
        print("Credit cards: \n")
        print(credit)
        print("")
        print("Purchases: \n")
        print(purchase)
        print("")

def pay_card(username):
    # Find out which cards the current user owns
    cur.execute(f"SELECT cc.balance, cc.card_number, cc.card_type, cc.expiry_date FROM credit_card cc JOIN user_account u ON u.bank_id = cc.bank_id WHERE username = '{username}'")
    cards = cur.fetchall()
    # If there are no cards, say there are no valid cards to pay off
    if not cards:
        print("Error: You have no valid cards to pay off \n")
        return
    else:
        # List each card
        i = 1
        for card in cards:
            print(str(i) + ": " + str(card))
            i += 1
        print("")

        # User must input which card he wants to pay down
        while True:
            user_card_selection = input("Select a card to pay (Type e to exit): ")
            if user_card_selection.lower() == 'e':
                print("")
                return
            try:
                # Once a selection is made, we set the card_number for later query usage
                user_card_selection = int(user_card_selection)
                if 1 <= user_card_selection <= len(cards):
                    card_number = cards[user_card_selection - 1][1]
                    print("You have selected card number: " + str(card_number))
                    print("")
                    break
                else:
                    print("Invalid input, try again \n")
            except ValueError:
                print("Please enter a valid number or 'e' to exit \n")

        while True:
            # Next we prompt the user for how much money they'd like to pay
            print("Balance = $" + str(cards[user_card_selection - 1][0]))
            user_payment = input("How much money would you like to pay? (Type e to exit): ")
            if user_payment.lower() == 'e':
                print("")
                return
            try:
                user_payment = float(user_payment)
                if user_payment > 0:
                    print("You chose to pay $" + str(user_payment))
                    cur.execute(f"SELECT ba.balance FROM bank_account ba JOIN user_account u ON u.bank_id = ba.bank_id WHERE username = '{username}'")
                    bank_balance = cur.fetchall()[0][0]
                    # Here we check if the user has enough money for the payment
                    if float(bank_balance) >= user_payment:
                        # We update the database and subtract the balance of both checking and card
                        cur.execute(f"UPDATE credit_card SET balance = balance - {user_payment} WHERE card_number = '{card_number}'")
                        cur.execute(f"UPDATE bank_account SET balance = balance - {user_payment} WHERE bank_id = (SELECT bank_id FROM user_account WHERE username = '{username}')")
                        cur.execute(f"SELECT ba.balance FROM bank_account ba JOIN user_account u ON u.bank_id = ba.bank_id WHERE username = '{username}'")
                        new_bank_balance = cur.fetchall()[0]
                        cur.execute(f"SELECT balance FROM credit_card WHERE card_number = '{card_number}'")
                        new_credit_balance = cur.fetchall()[0]
                        print("Successfully paid \n")
                        print("Your new bank balance is $" + str("{:.2f}".format(new_bank_balance[0])) + " and your new credit balance is $" + str("{:.2f}".format(new_credit_balance[0])))
                        return
                    # If there isn't enough money, try again with a lower payment
                    else:
                        print("Insufficient funds to pay, try a lower amount \n")
                else:
                    print("Please enter a positive amount.")
            except ValueError:
                print("Please enter a valid number (integer or decimal) or 'e' to exit \n")


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
        if username == "admin":
            print("z) Admin")
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
            pay_card(username)
            print("")

        elif user_input == "e":
            print("")
            print("Exiting app...")
            print("")
            break

        elif user_input == "z" and username == "admin":
            print("")

        else:
            print("Invalid input, try again")
            print("")

    cur.close()

