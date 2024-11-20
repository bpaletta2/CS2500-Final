import sqlite3
import csv
import time
import pandas as pd 
import numpy as np
import datetime
import pwinput

def login():
    check = False
    checkTwo = False
    username = ""
    while check == False:
        print("Enter your username: ")
        username = input()
        s = "SELECT * FROM users WHERE username =  '" + username + "'"
        cur.execute(s)
        f = cur.fetchall()
        if len(f) == 0:
            print("User not found")
        if len(f) != 0:
            check = True

    while checkTwo == False:
        password = pwinput.pwinput(prompt="Enter your password: ")
        s = "SELECT password FROM users WHERE username =  '" + username + "'"
        cur.execute(s)
        f = cur.fetchall()
        pass2 = f[0]
        result = ''.join(pass2)

        if password == result:
            print("Successful Login\n")
            return username
        else:
            print("Access Denied")

if __name__ == "__main__":
    conn = sqlite3.connect('final_project.db', isolation_level = None)
    cur = conn.cursor()
    login()
