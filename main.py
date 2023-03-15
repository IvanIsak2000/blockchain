import hashlib
import sys
import os
from datetime import datetime
import time
import pytz
import ast
import re
from pathlib import Path

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

        new_number_of_block = max(list_block) + 1

        with open(f'{transactions_folder}/{sorted(list_block)[-1]}.txt', 'rb') as pre_block:
            pre_block = pre_block.read()
            pre_hash = hashlib.md5(pre_block).hexdigest()
        return (pre_hash, new_number_of_block)

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

        os.system('cls')
        print("Creating block,please waiting!")

        for i in trange(100):
            time.sleep(0.01)

        return print(
            f'All done! Block with number {next_number} is created!\nYour data:\nFrom:{from_whom}\nAmount:{amount}\nTo whom:{to_whom}\nTime:{time_of_creation}')


if __name__ == '__main__':
    from_whom = input('Enter your name: ')
    amount = input('Enter your amount: ')
    to_whom = input('Enter to whom: ')

    blockchain = Blockchain()

    pre_new_and_next_block_number = blockchain.calculating_last_hash_and_number()

    next_block = blockchain.create_block(
        from_whom,
        amount,
        to_whom,
        pre_new_and_next_block_number[0],
        pre_new_and_next_block_number[1])

    for_exit = input('Enter to exit...')
    sys.exit()
