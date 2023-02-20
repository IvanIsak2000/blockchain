import hashlib
import sys
import os
import datetime
import time 
from tabulate import tabulate
from tqdm import trange




def get_hash_pre_block():

    block_list_directory = os.curdir + '/block_list'#директория папки для хранения всех блоков 

    blocks = os.listdir(block_list_directory)

    for number in blocks:
        the_number_of_the_most_recent_block = max(number[0])

    with open(f'block_list/{the_number_of_the_most_recent_block}.txt', 'rb') as pre_block:
        pre_block = pre_block.read()#читаем блок в режиме чтения в двоичном коде
        pre_hash_of_block = hashlib.md5(pre_block).hexdigest()#получаем хэш ВСЕГО предыдущего блока

    new_number_of_block = int(the_number_of_the_most_recent_block) + 1

    return pre_hash_of_block,new_number_of_block


def create_block(name, amount, to_whom):#функция для считывания хэша предыдущего блока и создание нового блока 

    pre_hash_and_pre_number = get_hash_pre_block()
    pre_hash = pre_hash_and_pre_number[0]
    new_number_of_block = pre_hash_and_pre_number[1]


    with open(f'block_list/{new_number_of_block}.txt', 'w') as new_block:#начинаем создание нового блока
        os.system('cls')
        print("Creating block!")
        for i in trange(1000):
            time.sleep(0.01)

        current_date_time = datetime.datetime.now()
        current_time = current_date_time.time()

        new_block_text = f'from:{name}\namount:{amount}\nto whom:{to_whom}\ntime:{current_time}\npre_hash{pre_hash}'#создаём текст нового блока:имя,цену,кому, и записываем хэш прошлого блока
        new_block.write(new_block_text)#записываем в новый блок
    os.system('cls')
    print('All done!')

    table = [['From',name],['Amount',amount],['To whom',to_whom],['Time',current_time],['Status','successful']]
    print(tabulate(table))


if __name__ == '__main__':
    name = input('Enter your name: ')
    amount = input('Enter your amount: ')
    to_whom = input('Enter to whom: ')
    create_block(name, amount, to_whom)
