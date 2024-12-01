import sqlite3
import csv
import pandas as pd

def csv_to_sql():
    conn = sqlite3.connect('final_project.db', isolation_level = None)
    cur = conn.cursor()

    file = open('user_account.csv')
    user_account = pd.read_csv('user_account.csv')
    user_account.to_sql('user_account', conn, if_exists='replace', index = False)
    file.close()

    file = open('bank_account.csv')
    bank_account = pd.read_csv('bank_account.csv')
    bank_account.to_sql('bank_account', conn, if_exists='replace', index = False)
    file.close()

    file = open('credit_card.csv')
    credit_card = pd.read_csv('credit_card.csv')
    credit_card.to_sql('credit_card', conn, if_exists='replace', index = False)
    file.close()

    file = open('purchase.csv')
    purchase = pd.read_csv('purchase.csv')
    purchase.to_sql('purchase', conn, if_exists='replace', index = False)
    file.close()