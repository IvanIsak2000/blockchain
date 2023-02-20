import hashlib
import sys
import os



def create_block(name, amount, to_whom):#функция для считывания хэша предыдущего блока и создание нового блока 
    block_list_directory = os.curdir + '/block_list'#директория папки для хранения всех блоков 

    blocks = os.listdir(block_list_directory)

    #определяем максимальный номер блока в папке
    for number in blocks:
        the_number_of_the_most_recent_block = max(number[0])

    new_number_of_block = int(the_number_of_the_most_recent_block) + 1#прибавляем единицу к последнему числу блока

    with open(f'block_list/{new_number_of_block}.txt', 'w') as new_block:#начинаем создание нового блока

        with open(f'block_list/{the_number_of_the_most_recent_block}.txt', 'rb') as pre_block:
            pre_block = pre_block.read()#читаем блок в режиме чтения в двоичном коде
            pre_hash = hashlib.md5(pre_block).hexdigest()#получаем хэш ВСЕГО предыдущего блока
            print(f'pre hash: {pre_hash}')#выводим хэш прошлого блока

        new_block_text = f'from:{name}\namount:{amount}\nto whom:{to_whom}\npre_hash{pre_hash}'#создаём текст нового блока:имя,цену,кому, и записываем хэш прошлого блока
        new_block.write(new_block_text)#записываем в новый блок
        print('All done!')


if __name__ == '__main__':
    name = input('Enter your name: ')
    amount = input('Enter your amount: ')
    to_whom = input('Enter to whom: ')
    create_block(name, amount, to_whom)
