import random
import math
import string
from string import digits
import json
import sqlite3


from Database import create_database
from Database import insert
from Database import Deposit
from Database import check_account
from Database import retrieve_information
from Database import Delete_info
from Database import balance_check
from Database import Withdraw
from Database import authentication
from Database import Transfer

#USed to add a account_balance entry


Balance = 0


#Automatic Account Number Generator
def Account_number() -> str:

    nums = digits
    nums = nums

    listing = list(nums)

    random.shuffle(listing)

    result = ""

    for char in listing:

        result +=char


    account_number = random.sample(result, 3)

    secret = ""
    for number in account_number:
        secret = secret+number

    account_number = "2560"+secret
    return account_number

def Create_Account():
    global Balance

    #Checking for Valid name
    Username = input("Username: ")
    if Username.isalpha():
        pass
    else:
        while Username.isalpha() == False :
            name = input("Use Correct name Format : ")
            if name.isalpha():
                break

    #Age:
    Age = int(input("Enter Age: ")[:2])

    #Email
    Email = input("Email address: ")

    #Mobile
    Mobile_number = input("Phone number: ")

    #Pin
    Pin = input("Enter Prefered Pin: ")

    if len(Pin) == "0000":
        print("Default Pin Can't be used.")
        pin = input("Enter Prefered Pin: ")
    else:
        while len(Pin) != 4:
            print("Pin Must be 4 Digits")
            pin = input("Enter Prefered Pin: ")

            if len(pin) == 4:
                break

    #Random Account Number assingment
    account_no = Account_number()


    account_data = (account_no, Username, Age, Email, Mobile_number, Pin, Balance)
    print(f"""
{'*'*10}
Name: {Username}
New Account No: {account_no}
Mobile NO: {Mobile_number}
Pin No : {Pin}
Age: {Age}
Email: {Email}
{'*'*10}
    

Confirm This Information Correct (Y/N)
""")

    prompt = input("?:")
    if prompt in ["Y", 'y'.lower(), "yes".capitalize(), "yes".upper(), 'yes']:

        if insert(account_data) == True:
            print("Account Created Successfully")

        else:
            print("Error Occured")
            Create_Account()
    else:
        Create_Account()


def deposit(): #setter

    account_number = input("Account Number: ")

    #checking if account exists
    if check_account(account_number) == True:

        amount = int(input("Enter Amount: "))

        if amount != 0:
            Deposit(account_number, amount)

        else:
            while amount == 0:
                amount = int(input("Enter Amount Again: "))

                #Condtion to break out
                if amount != 0:
                    Deposit(account_number, amount)
                    break
    else:
        print(f"Account Number {account_number} Doesn't Exist")


def Check_balance():
    account_number = input("Account Number: ")

    # Checking if account is Valid

    if check_account(account_number):

        ac_bal = balance_check(account_number)
        print(ac_bal)

    else:
        print(f"Account Number {account_number} Doesn't Exist")


def withdraw():

    account_number = input("Account Number: ")

    # checking if account exists
    if check_account(account_number) == True:

        amount = int(input("Enter Amount: "))

        Withdraw(account_number, account_number)

    else:
        print(f"Account Number {account_number} Doesn't Exist")


def transfer():
    account_from = input("Your Account Number: ")

    account_to = input("Reciver's Account Number: ")



    #checking if Both Accounts Exists before making Tranfer otherwise Error

    if check_account(account_from) and check_account(account_to):
        amount = int(input("Enter Amount: "))

        Transfer(account_from=account_from,account_to=account_to,amount=amount)

    else:
        print("Ensure Correct Account Details")

def Statement():
    account_data = {"ID": "", "Name": "", "Account Number": "", "Mobile No": "", "Age": "", "Email": "","Account Balance": ""}

    account_number = input("Account Number: ")

    # checking if account exists
    if check_account(account_number) == True:
        information = retrieve_information(account_number)

        data = []
        for info in information:
            for field in info:
                data.append(field)

        data = tuple(data)
        print(data)


        #These fields should be organises so that when priented they look nice not like it is
        #Organising the data for Presenting

        #for key in account_data:
        #    for value in data:
        #        account_data[key] = value

        #print(account_data)

    else:
        print(f"Account Number {account_number} Doesn't Exist")

def Delete_account():
    account_number = input("Account Number To Delete: ")

    #Checking if account number is Valid

    if check_account(account_number):

        print("\nAre You sure to Continue ? (Y/N")
        prompt = input("Prompt?: Y/N: ")

        if prompt in ["Y", 'y'.lower(), "yes".capitalize(), "yes".upper(), "yes"]:

            Delete_info(account_number)

        else:
            main()

    else:
        print(f"Account Number {account_number} Doesn't Exist")



def Check_value(inpt):

    #This is to check for value error and handle integer inputs
    #in Code
    pass
    """
    while True:
        try:
            inpt = int(input(":"))

        except ValueError as e:
            pass
    """




def main():
    Bank = {}

    Bank[1] = Create_Account

    Bank[2] = deposit

    Bank[3] = Check_balance

    Bank[4] = withdraw

    Bank[5] = transfer

    Bank[6] = Statement

    Bank[7] = Delete_account

    Bank[8] = exit

    print(f'''
{"* "*10}BANK OPERATION MENU{' *'*10}
[1] --> Create Account
[2] --> Deposit Money
[3] --> Check Balance
[4] --> Withdraw Money
[5] --> Transfer Money
[6] --> Request Statement
[7] --> Delete Account
[8] --> Exit
        ''')


    Action = int(input("Enter Prompt: "))

    if Bank.get(Action) != None:
        Bank[Action]()

    else:
        while Bank.get(Action) == None:
            Action = int(input("Enter Valid Prompt: "))

            if Bank.get(Action) != None:
                Bank[Action]()  # Suitable if No adjuments are provided to the functions above
                break


if __name__ == "__main__":
    while True:
        main()


