import hashlib
import sys
import os
from datetime import datetime
import time
import pytz
import ast
from pathlib import Path
import sqlite3

from tqdm import trange


class Blockchain():

    def calculating_last_hash_and_number(self):
        global transactions_folder
        transactions_folder = 'transactions'
        if not os.path.exists(transactions_folder):
            os.makedirs(transactions_folder)
            with open(f"{transactions_folder}/1.txt", "w") as file:
                file.write("This genesis block!")
        list_block = []
        for _file in os.listdir(transactions_folder):
            if _file.endswith(".txt"):
                list_block.append(int(_file.split('.')[0]))

        with open(f'{transactions_folder}/{sorted(list_block)[-1]}.txt', 'rb') as pre_block:
            pre_block = pre_block.read()
            pre_hash = hashlib.md5(pre_block).hexdigest()
        return (pre_hash, max(list_block)+1)

    def create_block(self, from_whom, amount, to_whom, pre_hash, next_number):
        self.from_whom = from_whom
        self.amount = amount
        self.to_whom = to_whom
        self.pre_hash = pre_hash
        self.next_number = next_number

        time_of_creation = datetime.now(
            pytz.timezone('Europe/Moscow')).strftime("%H:%M:%S %Y-%m-%d")

        with open(f'{transactions_folder}/{next_number}.txt', 'w') as next_block:
            data = f'From:{from_whom}\nAmount:{amount}\nTo whom:{to_whom}\nTime:{time_of_creation}\nHash:{pre_hash}'
            next_block.write(data)


        with open(f'{transactions_folder}/{next_number}.txt', 'rb') as this_block:
            this_block = this_block.read()
            hash_this_block = hashlib.md5(this_block).hexdigest()


        with sqlite3.connect("blockchain.db") as db:
            cursor = db.cursor()
            query = """INSERT INTO blockchain(block_id,hash) VALUES(?,?) """
            new_block = [(next_number,hash_this_block)]
            cursor.executemany(query, new_block)
            print('New block in writed!')


        os.system('cls')
        print("Creating block,please waiting!")
        

        for i in trange(100):
            time.sleep(0.01)

        os.system('cls')

        return print(
                    f'All done! Block with number {next_number} is created!\nYour data:\nFrom:{from_whom}\nAmount:{amount}\nTo whom:{to_whom}\nTime:{time_of_creation}')


    def checking_blocks(self):
        global transactions_folder
        transactions_folder = 'transactions'
        with sqlite3.connect('blockchain.db') as db :
            cursor = db.cursor()
            query = """SELECT block_id,hash FROM blockchain"""
            cursor.execute(query)

            block_id_and_hash = {}
            for block_id,_hash in cursor:
                block_id_and_hash[block_id]=_hash

            return  (block_id_and_hash)

    def compare_with_db(self,number_and_hash):
        
        self.number_and_hash = number_and_hash
        new_number_and_hash = {}

        for number,_hash in number_and_hash.items():

            with open(f'{transactions_folder}/{number}.txt','rb') as file:
                block = file.read()
                hash_block = hashlib.md5(block).hexdigest()
                new_number_and_hash[number] = hash_block
        
        return print('Data not changed:',number_and_hash == new_number_and_hash)

                


if __name__ == '__main__':
    move = int(input('Create or check? 1/2'))
    blockchain = Blockchain()

    if move != 2:

        with sqlite3.connect("blockchain.db") as db: #create db for program

            cursor = db.cursor()
            query_start = """ CREATE TABLE IF NOT EXISTS blockchain(
                    block_id INTEGER,
                    hash TEXT
                    ) """
            cursor.execute(query_start)

        from_whom = input('Enter your name: ')
        amount = input('Enter your amount: ')
        to_whom = input('Enter to whom: ')

        

        pre_new_and_next_block_number = blockchain.calculating_last_hash_and_number()

        next_block = blockchain.create_block(
            from_whom,
            amount,
            to_whom,
            pre_new_and_next_block_number[0],
            pre_new_and_next_block_number[1])

    else:
        data = blockchain.checking_blocks()
        blockchain.compare_with_db(data)


    for_exit = input('Press to exit...')
    sys.exit()
