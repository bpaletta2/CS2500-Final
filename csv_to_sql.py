import sqlite3
import csv
import pandas as pd

def csv_to_sql():
    conn = sqlite3.connect('final_project.db', isolation_level = None)
    cur = conn.cursor()

    file = open('user_account.csv')
    contents = csv.reader(file)
    userData = pd.read_csv('user_account.csv')
    userData.to_sql('user_account', conn, if_exists='replace', index = False)
    file.close()

    file = open('bank_account.csv')
    contents = csv.reader(file)
    followers = pd.read_csv('bank_account.csv')
    followers.to_sql('bank_account', conn, if_exists='replace', index = False)
    file.close()

    file = open('credit_card.csv')
    contents = csv.reader(file)
    posts = pd.read_csv('credit_card.csv')
    posts.to_sql('credit_card', conn, if_exists='replace', index = False)
    file.close()

    file = open('purchase.csv')
    contents = csv.reader(file)
    posts = pd.read_csv('purchase.csv')
    posts.to_sql('purchase', conn, if_exists='replace', index = False)
    file.close()