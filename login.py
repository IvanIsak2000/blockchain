import dearpygui.dearpygui as dpg
import sqlite3
import os
import sys
import hashlib
import re

from string import *
import dearpygui.dearpygui as dpg
from genp import password_generation


dpg.create_context()
dpg.create_viewport()

dpg.create_viewport(title='Account', width=800, height=600)
with dpg.window(show=False) as main_window:

    dpg.add_text('You have successfully logged into your account!')

    def login():

        dpg.configure_item(main_window, show=True)

        dpg.set_primary_window(main_window, True)

        dpg.configure_item(login_window, show=False)


dpg.create_viewport(title='Blockchain', width=700, height=600)
with dpg.window(label=None, width=500, height=550, tag='Primary Window') as login_window:

    with sqlite3.connect("blockchain_accounts.db") as db:
        cursor = db.cursor()
        query_start = """ CREATE TABLE IF NOT EXISTS accounts(
            login TEXT,
            hash TEXT
            ) """
        cursor.execute(query_start)
        print('db OK')

    def login_in_account(user_name, user_password):
        user_name = dpg.get_value('account-name')

        user_password = dpg.get_value('account-password')

        user_password = str(hash(user_password))  # hashed password

        with sqlite3.connect('blockchain_accounts.db') as db:
            cursor = db.cursor()
            query_check = """ SELECT login,hash FROM accounts"""
            cursor.execute(query_check)

            successful_login = False

            for login_in_db, hash_in_db in cursor:
                if user_name == login_in_db and user_password == hash_in_db:
                    successful_login = True
                    print('Logined!')
                    login()

                else:
                    print('Wrong data!')

    def create_account():
        new_login = dpg.get_value('login')
        new_password = password_generation(True, True, False, 25)

        password_hash = str(hash(new_password))  # hashed password

        with sqlite3.connect('blockchain_accounts.db') as db:
            cursor = db.cursor()
            query_check = """SELECT login,hash FROM accounts"""
            cursor.execute(query_check)
            print(cursor)
            found_duplicate_login = False
            spec_symbols_in_new_login = False

            for account_name_from_db, account_password_from_db in cursor:
                if account_name_from_db == new_login:
                    found_duplicate_login = True

            if not found_duplicate_login:

                if len(new_login) > 6 and len(
                        new_login) < 20 and new_login.isalpha():
                    with sqlite3.connect("blockchain_accounts.db") as db:

                        cursor = db.cursor()
                        query = """INSERT INTO accounts(login,hash) VALUES(?,?) """
                        new_account = [(new_login, password_hash)]
                        cursor.executemany(query, new_account)
                        print('Data added!')
                        print(
                            f'CREATE NEW ACCOUNT!\nLogin:{new_login}\nPassword:{new_password}')
                else:
                    print('Not vaild data!')

    with dpg.menu_bar():
        with dpg.menu(label='Login'):
            dpg.add_text('\nLogin')
            user_name = (dpg.add_input_text(tag='account-name'))
            user_password = (dpg.add_input_text(tag='account-password'))

            dpg.add_button(label='OK', callback=login_in_account)

        with dpg.menu(label='Create account'):
            dpg.add_text('Enter your new account name:')

            dpg.add_input_text(tag='login')
            dpg.add_button(label='Create account?', callback=create_account)
            with dpg.tooltip('login'):
                dpg.add_text(
                    '''Your login must be more than 6 and less than 20 characters, must not contain spaces and special characters!''')


dpg.set_primary_window(login_window, True)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('Primary Window', True)
dpg.start_dearpygui()
dpg.destroy_context()
