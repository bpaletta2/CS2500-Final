import sqlite3
import os
import pwinput
import pandas as pd
import matplotlib.pyplot as plt

from csv_to_sql import csv_to_sql


if not os.path.exists("final_project.db"):
    csv_to_sql()

conn = sqlite3.connect('final_project.db', isolation_level = None)
cur = conn.cursor()

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

def admin_panel():
    # Lists all tables in the database
    def list_tables():
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

        tables = cur.fetchall()

        i = 1
        for table in tables:
            print(str(i) + ") " + str(table[0]))
            i += 1
        print("")
        print("Select which table you'd like to modify")
        print("")

    # Checks if bank_id already exists
    def bank_id_check(bank_id):
        cur.execute(f"SELECT COUNT(*) FROM user_account WHERE bank_id = '{bank_id}'")
        if cur.fetchone()[0] > 0:
            return True
        cur.execute(f"SELECT COUNT(*) FROM bank_account WHERE bank_id = '{bank_id}'")
        if cur.fetchone()[0] > 0:
            return True
        print("")
        return False

    print("")
    while True:
        try:
            print("a) Add a record")
            print("b) Delete a record")
            print("c) Visualize the database")
            print("e) Exit")
            print("")

            user_choice = input("Enter your choice: ")

            if user_choice == "a":
                print("")
                list_tables()
                try:
                    user_table = int(input("Enter your choice: "))
                    if 1 <= user_table <= 4:
                        print("")
                        bank_id = input("Enter bank id: ")
                        if user_table in (1, 2) and bank_id_check(bank_id):
                            print("Error: bank_id " + bank_id + " already exists in table")
                            continue

                        # Add record to user_account
                        if user_table == 1:
                            username = input("Enter username: ")
                            password = input("Enter password: ")
                            ssn = input("Enter SSN: ")
                            email = input("Enter email: ")
                            cur.execute(f"INSERT INTO user_account (bank_id, username, password, ssn, email)"
                                        f"VALUES ('{bank_id}', '{username}', '{password}', '{ssn}', '{email}')")

                        # Add record to bank_account
                        elif user_table == 2:
                            routing_number = input("Enter routing number: ")
                            account_number = input("Enter account number: ")
                            balance = input("Enter balance: ")
                            cur.execute(f"INSERT INTO bank_account (bank_id, routing_number, account_number, balance)"
                                        f" VALUES ('{bank_id}', '{routing_number}', '{account_number}', '{balance}')")

                        # Add record to credit_card
                        elif user_table == 3:
                            card_number = input("Enter card number: ")
                            card_type = input("Enter card type: ")
                            expiry_date = input("Enter expiry date: ")
                            balance = input("Enter balance: ")
                            cur.execute(f"INSERT INTO credit_card (bank_id, card_number, card_type, expiry_date, balance) "
                                        f"VALUES ('{bank_id}', '{card_number}', '{card_type}', '{expiry_date}', '{balance}')")

                        # Add record to purchase
                        elif user_table == 4:
                            payment_type = input("Enter payment type: ")
                            amount = input("Enter amount: ")
                            merchant = input("Enter merchant: ")
                            cur.execute(f"INSERT INTO purchase (bank_id, payment_type, amount, merchant) "
                                        f"VALUES ('{bank_id}', '{payment_type}', '{amount}', '{merchant}')")

                        conn.commit()
                        print("Record added successfully \n")
                    else:
                        print("Invalid input, try again \n")
                except ValueError:
                    print("Please enter a valid number or 'e' to exit \n")

            elif user_choice == "b":
                print("")
                list_tables()
                try:
                    user_table = int(input("Enter your choice: "))
                    if 1 <= user_table <= 4:
                        bank_id = input("Enter the ID of the record to delete: ")

                        # Remove record from user_account
                        if user_table == 1:
                            cur.execute(f"SELECT * FROM user_account WHERE bank_id = '{bank_id}'")
                            record = cur.fetchone()
                            if record:
                                cur.execute(f"DELETE FROM user_account WHERE bank_id = '{bank_id}'")
                                conn.commit()
                                print("Record deleted successfully from user_account \n")
                            else:
                                print(f"No record with ID {bank_id} found in user_account \n")

                        # Remove record from bank_account
                        elif user_table == 2:
                            cur.execute(f"SELECT * FROM bank_account WHERE bank_id = '{bank_id}'")
                            record = cur.fetchone()
                            if record:
                                cur.execute(f"DELETE FROM bank_account WHERE bank_id = '{bank_id}'")
                                conn.commit()
                                print("Record deleted successfully from bank_account \n")
                            else:
                                print(f"No record with ID {bank_id} found in bank_account \n")

                        # Remove record from credit_card
                        elif user_table == 3:
                            cur.execute(f"SELECT * FROM credit_card WHERE bank_id = '{bank_id}'")
                            record = cur.fetchone()
                            if record:
                                cur.execute(f"DELETE FROM credit_card WHERE bank_id = '{bank_id}'")
                                conn.commit()
                                print("Record deleted successfully from credit_card \n")
                            else:
                                print(f"No record with ID {bank_id} found in credit_card \n")

                        # Remove record from purchase
                        elif user_table == 4:
                            cur.execute(f"SELECT * FROM purchase WHERE bank_id = '{bank_id}'")
                            record = cur.fetchone()
                            if record:
                                cur.execute(f"DELETE FROM purchase WHERE bank_id = '{bank_id}'")
                                conn.commit()
                                print("Record deleted successfully from purchase \n")
                            else:
                                print(f"No record with ID {bank_id} found in purchase \n")
                    else:
                        print("Invalid input, try again \n")
                except ValueError:
                    print("Please enter a valid number or 'e' to exit \n")

            elif user_choice == "c":
                print("")
                bank_account = pd.read_sql_query("SELECT * FROM bank_account", conn)
                credit_card = pd.read_sql_query("SELECT * FROM credit_card", conn)
                purchase = pd.read_sql_query("SELECT * FROM purchase", conn)

                bank_metrics = bank_account.groupby('bank_id')['balance'].agg(['sum', 'mean']).reset_index()
                credit_metrics = credit_card.groupby('bank_id')['balance'].agg(['sum', 'mean']).reset_index()
                purchase_metrics = purchase.groupby('bank_id')['amount'].agg(['count', 'mean']).reset_index()

                fig, axes = plt.subplots(2, 2, figsize=(12, 10))

                # Plot bank_account
                axes[0, 0].bar(bank_metrics['bank_id'], bank_metrics['sum'].astype(int), label='Total Balance', alpha=0.7)
                axes[0, 0].set_title('Bank Account Balances')
                axes[0, 0].set_xlabel('Bank ID')
                axes[0, 0].set_ylabel('Balance')
                axes[0, 0].legend()

                # Plot credit_card
                axes[0, 1].bar(credit_metrics['bank_id'], credit_metrics['sum'].astype(int), label='Total Balance')
                axes[0, 1].bar(credit_metrics['bank_id'], credit_metrics['mean'].astype(int), label='Average Balance', alpha=0.7)
                axes[0, 1].set_title('Credit Card Balances')
                axes[0, 1].set_xlabel('Bank ID')
                axes[0, 1].set_ylabel('Balance')
                axes[0, 1].legend()

                # Plot purchase
                axes[1, 0].bar(purchase_metrics['bank_id'], purchase_metrics['mean'].astype(int), label='Average Purchase Size')
                axes[1, 0].set_title('Average Purchase Size')
                axes[1, 0].set_xlabel('Bank ID')
                axes[1, 0].set_ylabel('Average Purchase Amount')
                axes[1, 0].legend()
                axes[1, 1].pie(purchase_metrics['count'], labels=purchase_metrics['bank_id'], autopct='%1.1f%%')
                axes[1, 1].set_title('Purchase Count by Bank ID')

                plt.tight_layout()
                plt.show()

            elif user_choice == "e":
                return

            else:
                print("Invalid input, try again \n")
        except ValueError:
            print("Please enter a valid number or 'e' to exit \n")

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
    username = login()

    while True:
        try:
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
                admin_panel()
                print("")

            else:
                print("Invalid input, try again")
                print("")
        except ValueError:
            print("Please enter a valid number or 'e' to exit \n")

    cur.close()

