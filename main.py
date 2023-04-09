#!/usr/bin/env python3
import hashlib
import os
from datetime import datetime
from dataclasses import dataclass
import time
from pathlib import Path
import pytz
from sqlite3 import connect
from pathlib import Path
from tqdm import trange


transactions_folder = "transactions"


@dataclass
class BlockData:
    sender: str
    amount: str
    reciever: str
    pre_hash: str
    next_number: int


def genesis_block():
    if not os.path.exists(transactions_folder):
        os.makedirs(transactions_folder)
        with open(f"{transactions_folder}/1.txt", "w") as file:
            file.write("This is genesis block!")
    """
    In short, if there is no transactions folder,
    then we create it in short and add the first
    block to it (in the blockchain it is called genesis block)
    """
    # This func Check whether there is a genesis block(number 1) in transaction folder


def last_number() -> int:
    list_blocks = []
    for file in os.listdir(transactions_folder):
        if file.endswith(".txt"):
            list_blocks.append(int(file.split(".")[0]))
    return (max(list_blocks))
    # This func return the number of last block from transaction folder


def __hash__(last_number) -> str:
    path = f"{transactions_folder}/{last_number}.txt"
    with open(path, "rb") as pre_block:
        pre_block = pre_block.read()
        pre_hash = hashlib.md5(pre_block).hexdigest()
    return (pre_hash)
    # This func return hash of last block


def create_block(block_data: BlockData):
    next_number = block_data.next_number
    creation_timezone = pytz.timezone("Europe/Moscow")
    time_of_creation = datetime.now(creation_timezone)
    time_of_creation = time_of_creation.strftime("%H:%M:%S %Y-%m-%d")
    next_number_path = f"{transactions_folder}/{next_number}.txt"
    with open(next_number_path, "w") as next_block:
        data = [f"From: {block_data.sender}",
                f"Amount: {block_data.amount}",
                f"To whom: {block_data.reciever}",
                f"Time: {time_of_creation}",
                f"Hash: {block_data.pre_hash}"]
        data = "\n".join(data)
        next_block.write(data)
    block_path = f"{transactions_folder}/{next_number}.txt"
    with open(block_path, "rb") as this_block:
        this_block = this_block.read()
        hash_this_block = hashlib.md5(this_block).hexdigest()
    with connect("blockchain.db") as connection:
        cursor = connection.cursor()
        query = """
        INSERT INTO blockchain (block_id, hash)
        VALUES(?,?);
        """
        new_block = [(next_number, hash_this_block)]
        cursor.executemany(query, new_block)
        connection.commit()
        cursor.close()
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print("Block is being created, please wait!")
    for i in trange(100):
        time.sleep(0.01)
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    success_message = [f"All done! Block number {next_number} was created!"]
    success_message.append("Transaction data:")
    success_message.append(f"From: {block_data.sender}")
    success_message.append(f"Amount: {amount}")
    success_message.append(f"To whom: {block_data.reciever}")
    success_message.append(f"Time: {time_of_creation}")
    success_message = "\n".join(success_message)
    return print(success_message)
    # This func create new block and return your transaction data message


def checking_blocks():
    with connect("blockchain.db") as connection:
        cursor = connection.cursor()
        query = """
        SELECT block_id, hash
        FROM blockchain;
        """
        cursor.execute(query)
        block_id_and_hash = {}
        for block_id, current_hash in cursor:
            block_id_and_hash[block_id] = current_hash
        connection.commit()
        cursor.close()
        return block_id_and_hash
    # We get all the recorded blocks with their hashes


def compare_with_db(number_and_hash):
    number_and_hash = number_and_hash
    new_number_and_hash = {}
    for number, _hash in number_and_hash.items():
        block_path = f"{transactions_folder}/{number}.txt"
        with open(block_path, "rb") as file:
            block = file.read()
            hash_block = hashlib.md5(block).hexdigest()
            new_number_and_hash[number] = hash_block
    if number_and_hash == new_number_and_hash:
        result = "Data not changed"
    else:
        result = "Data changed!!!"
    return print(result)
    # And here we open each block (file), calculate its hash and write it
    # to dict, then compare this dict with database


if __name__ == "__main__":
    with connect("blockchain.db") as connection:  # Create an empty database
        cursor = connection.cursor()
        query_start = """
        CREATE TABLE IF NOT EXISTS blockchain(
                block_id INTEGER,
                hash TEXT);
        """
        cursor.execute(query_start)
    try:
        action = int(input("Create or check? 1/2 "))
        if action == 1:
            sender = input("Enter your name: ")
            amount = input("Enter your amount: ")
            reciever = input("Enter to whom: ")
            genesis_block()
            next_block_number = last_number() + 1
            pre_block_hash = __hash__(last_number())

            next_block_args = BlockData(sender=sender,
                                        amount=amount,
                                        reciever=reciever,
                                        pre_hash=pre_block_hash,
                                        next_number=next_block_number)
            next_block = create_block(next_block_args)
        elif action == 2:

            data = checking_blocks()  # reading and returning numbers and hash from database
            compare_with_db(data) # We transfer data from the database and compare them with reading hashes from each file
        else:
            print("Input value wasn't recognised")
    except ValueError:
        print("Error: data must be an integer!")
    except BaseException as e:
        print("Unknown error occured:", str(e))
    finally:
        connection.commit()
        cursor.close()
        for_exit = input("Press to exit...")  # guess what it's for
