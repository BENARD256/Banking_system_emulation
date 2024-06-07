import sqlite3


#BACKEND DATABASE BANKING SYSTEM
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# Table Creation Function

#Account Balance Missiong perimeter
def create_database():
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Bank (
            id INTEGER PRIMARY KEY,
            Account_number TEXT NOT NULL,
            Username TEXT NOT NULL,
            Age INTEGER NOT NULL,
            Email TEXT,
            Mobile_number TEXT,
            Pin INTEGER NOT NULL,
            Account_balance INTEGER
        );
        """)
        connection.commit()
    except sqlite3.Error as e:
        print("Error creating table:", e)

def insert(account_data):

    try:

        cursor.execute(f"SELECT * FROM Bank WHERE Account_number  = ?", (account_data[0],))

        existing = cursor.fetchone()

        if not existing:
            query = f"INSERT INTO Bank (Account_number, Username, Age, Email, Mobile_number, Pin, Account_balance) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query, account_data)

            connection.commit()
            return True

        else:
            print(f"Account {account_data[0]} Already Exists")
            return None


    except sqlite3.Error as e:
        print("Error During Entry:", e)
        return None

def Delete_info(account_number):
    while True:
        pin = int(input("Enter Pin: ")[:4])

        if authentication(account_number, pin):

            try:
                # Check if the account number exists
                cursor.execute("SELECT * FROM Bank WHERE account_number = ? AND Pin =?", (account_number, pin))
                existing_entry = cursor.fetchone()


                if existing_entry:
                    # Delete the account if it exists
                    cursor.execute("DELETE FROM Bank WHERE account_number = ?", (account_number,))
                    connection.commit()
                    print(f"Successfully deleted data for account number {account_number}")

                else:
                    print(f"Account {account_number} Doesn't Exist")
                    return None

            except sqlite3.Error as e:
                print(f"Error {e} while deleting data")
                return None

            break

        else:
            print("Incorrect Pin")


def retrieve_information(account_number):
    account_infomation = ""

    while True:

        pin = int(input("Enter Pin: ")[:4])

        if authentication(account_number,pin)==True:

            try:
                # Check if account exists
                cursor.execute("SELECT * FROM Bank WHERE account_number = ?", (account_number,))
                exists = cursor.fetchone()

                if exists:

                    cursor.execute("SELECT * FROM Bank WHERE account_number = ?", (account_number,))

                    account_info = cursor.fetchall()

                    account_infomation = account_info


                else:
                    print(f"Sorry!  account number {account_number} Doesn't Exist.")
            except sqlite3.Error as e:
                print(f"Error {e} while retrieving data")


            break


        else:
            print("Incorrect Pin")

    return account_infomation

def authentication(account_number, pin):
    #This ensures Authentication
    try:
        cursor.execute("SELECT * FROM Bank WHERE account_number = ? AND pin = ?", (account_number, pin))
        account_info = cursor.fetchone()

        if account_info:
            return True
        else:
            return None

    except sqlite3.Error as e:
        print(f"Error {e} while retrieving data")
        return None

def Deposit(account_number, amount):

    while True:
        pin = int(input("Enter Pin: ")[:4])

        if authentication(account_number, pin):
            try:
                # Retrieve current balance
                cursor.execute(f"SELECT Account_balance FROM Bank WHERE Account_number = {account_number}")
                current_balance = cursor.fetchone()[0]

                print(f"Account Balance: {current_balance}")

                # Update balance
                new_balance = current_balance + amount

                cursor.execute(f"UPDATE Bank SET Account_balance = {new_balance} WHERE Account_number = {account_number}")
                connection.commit()  # Commit the transaction

                print("You have Deposted %d Your new balance is %d" % (amount, new_balance))

            except sqlite3.Error as e:
                print(f"Error {e}  Occured")
                current_balance.rollback()


            break

        else:
            print("Incorrect Pin")

def check_account(account_number):
    #This checks if the account Exists
    try:

        cursor.execute(f"SELECT * FROM Bank WHERE Account_number  = ?", (account_number,))

        existing = cursor.fetchone()

        if existing:
            return True

        else:
            return None

    except sqlite3.Error as e:
        print("Error During Entry:", e)
        return None

def Withdraw(account_number, amount):
    while True:
        pin = int(input("Enter Pin: ")[:4])

        if authentication(account_number, pin):
            try:
                # Retrieve current balance
                cursor.execute(f"SELECT Account_balance FROM Bank WHERE Account_number = {account_number}")
                current_balance = cursor.fetchone()[0]

                if weigh_amount_Balance(amount=amount, balance=current_balance):

                    new_balance = int(current_balance) - int(amount)


                    #Updating DB

                    cursor.execute(f"UPDATE Bank SET Account_balance = {new_balance} WHERE Account_number = {account_number}")
                    connection.commit()  # Commit the transaction

                    print(f"You have Withdrawn Ugx {amount} Your new balance is Ugx {new_balance}")

                else:
                    print("\nAccount Balance insufficient, Balance: UGX %d\n" % (current_balance))
                    return None


            except sqlite3.Error as e:
                print(f"Error {e}  Occured")
                current_balance.rollback()

            break

        else:
            print("Incorrect Pin")


#Checking acount Balacne
def balance_check(account_number):
    while True:
        pin = int(input("Enter Pin: ")[:4])

        if authentication(account_number, pin):
            try:
                # Retrieve Current balance
                cursor.execute(f"SELECT Account_balance FROM Bank WHERE Account_number = {account_number}")
                current_balance = cursor.fetchone()[0]

                return f"Your Account balance is Ugx: {current_balance}"


            except sqlite3.Error as e:
                print(f"Error {e}  Occured")
                current_balance.rollback()

            break

        else:
            print("Incorrect Pin")


#This function is responsible for checking if the withdraw amount is beyond our balance

def weigh_amount_Balance(amount, balance):
    #These values should be treated as intergers to prevent errors in code
    balance = int(balance)
    amount = int(amount)
    while amount == 0:

        if amount != 0 and amount >= 1:
            break

    # Withdraw Condition !
    while True:

        if amount <= balance and amount >= 1:
            return True
            break

        else:
            return False
            Withdraw()


# This is to retrieve the balance check if the amount to send does exceed our balance
# if it doesnt send

def Transfer(account_from, account_to, amount):
    #checking if accounts are same
    if account_from == account_to:
        print("Transaction Fail!, You cant send to same account")

        #This function will be overriden by the implementation
        main()

    else:

        while True:
            pin = int(input("Enter Pin: ")[:4])

            if authentication(account_from, pin):

                try:
                    # Retrieve Current balance
                    cursor.execute(f"SELECT Account_balance FROM Bank WHERE Account_number = {account_from}")
                    current_balance_sender = cursor.fetchone()[0]

                    # Checking if our account Balance is greater than amount to transfer

                    if weigh_amount_Balance(amount=amount, balance=current_balance_sender):

                        #Deducting the amount sent from sender's Account
                        new_balance_sender = current_balance_sender - amount

                        # Updating DB Sender
                        cursor.execute(
                            f"UPDATE Bank SET Account_balance = {new_balance_sender} WHERE Account_number = {account_from}")
                        connection.commit()  # Commit the transaction


                        #Handling the recipeint of the money


                        try:
                            # Retrieve Balance of reciver
                            cursor.execute(f"SELECT Account_balance FROM Bank WHERE Account_number = {account_to}")

                            current_balance_reciever = cursor.fetchone()[0]


                            #Adding the amount to Reciver's Account

                            new_balance_reciver = current_balance_reciever + amount

                            cursor.execute(
                                f"UPDATE Bank SET Account_balance = {new_balance_reciver} WHERE Account_number = {account_to}")
                            connection.commit()  # Commit the transaction


                        except sqlite3.Error as e:
                            print(f"Error {e}  Occured")


                        print(f"You have Sent Ugx {amount} To Account_No: {account_to}, Your new balance is Ugx {new_balance_sender}")



                    else:
                        print("\nTransaction Error: Account Balance insufficient, Balance: UGX %d\n" % (current_balance_sender))
                        return None



                except sqlite3.Error as e:
                    print(f"Error {e}  Occured")


                break




            else:
                print("Incorrect Pin")


#This functino will be overriden in implementation
def main():
    pass