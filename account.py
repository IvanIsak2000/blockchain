#!/usr/bin/env python3
import dearpygui.dearpygui as dpg
from sqlite3 import connect
import os
import sys
import hashlib
import dearpygui.dearpygui as dpg
from genp import password_generation


def db_check():
    with connect("blockchain_accounts.db") as connection:
        cursor = connection.cursor()
        query_start = """
        CREATE TABLE IF NOT EXISTS accounts(
            login TEXT,
            hash TEXT);
            """
        cursor.execute(query_start)
        connection.commit()
        cursor.close()
        return print("database OK")


def login_in_account(login, user_password):
    user_login = dpg.get_value("login")
    user_password = dpg.get_value("password")
    hash_new_password = str(hashlib.md5(str.encode(user_password)).hexdigest())
    with connect("blockchain_accounts.db") as connection:
        cursor = connection.cursor()
        query_check = """
        SELECT login, hash
        FROM accounts;
        """
        cursor.execute(query_check)
        for login_from_db, hash_from_db in cursor:
            if user_login == login_from_db and hash_new_password == hash_from_db:
                try:
                    os.system('cls')
                except:
                    os.system('clear')
                return successful_login()
            else:
                return print("Wrong data!")
        connection.commit()
        cursor.close()


def create_account():
    new_login = dpg.get_value("new_login")
    new_password = password_generation(True, True, False, 25)
    password_hash = str((hashlib.md5(str.encode(new_password)).hexdigest()))
    new_account_message = ["CREATE NEW ACCOUNT!"]
    new_account_message.append(f"Login:{new_login}")
    new_account_message.append(f"Password:{new_password}")
    new_account_message = "\n".join(new_account_message)
    with connect("blockchain_accounts.db") as connection:
        cursor = connection.cursor()
        query_check = """
        SELECT login, hash
        FROM accounts;
        """
        cursor.execute(query_check)
        found_duplicate_login = False
        for account_name_from_db, account_password_from_db in cursor:
            if account_name_from_db == new_login:
                found_duplicate_login = True
        if not found_duplicate_login:
            if 20 > len(new_login) > 6 and new_login.isalpha():
                with connect("blockchain_accounts.db") as connection:
                    cursor = connection.cursor()
                    query = """
                    INSERT INTO accounts(login, hash)
                    VALUES(?,?);
                    """
                    new_account = [(new_login, password_hash)]
                    cursor.executemany(query, new_account)
                    print(new_account_message)
            else:
                print("Not vaild data!")
        else:
            print("This login already exists!")
        connection.commit()
        cursor.close()
        
dpg.create_context()
dpg.create_viewport()

with dpg.window(show=False,) as account_window:
    dpg.add_text("You have successfully logged into your account!")

    def successful_login():
        dpg.configure_item(account_window, show=True)
        dpg.set_primary_window(account_window, True)
        dpg.configure_item(login_window, show=False)

dpg.create_viewport(title="Blockchain", width=700, height=600)
with dpg.window(label=None, tag="Primary Window") as login_window:
    db_check()
    with dpg.menu_bar():
        with dpg.menu(label="Login"):
            dpg.add_text("\nLogin")
            login = (dpg.add_input_text(tag="login"))
            user_password = (dpg.add_input_text(tag="password"))
            dpg.add_button(label="OK", callback=login_in_account)
        with dpg.menu(label="Create account"):
            dpg.add_text("Enter your new account name:")
            dpg.add_input_text(tag="new_login")
            dpg.add_button(label="Create account?", callback=create_account)
            with dpg.tooltip("login"):
                login_message = "Your login must be more than 6 and less "
                login_message += "than 20 characters, must not contain spaces "
                login_message += "special characters!"
                dpg.add_text(login_message)


dpg.set_primary_window(login_window, True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
