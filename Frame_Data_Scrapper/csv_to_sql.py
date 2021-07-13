import sqlite3
import csv
import os
import pandas as pd
from scrapper import get_all_characters_names

DATABASE_NAME = 'characters.db'


# create a table
def create_table(character_name):
    # create a connection
    database_name = DATABASE_NAME
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), database_name))

    # create a cursor
    c = conn.cursor()

    # create the table
    table_creation_command = f"CREATE TABLE if not exists {character_name}% (command text, hit_level text,damage text,start_up_frame text,block_frame text,hit_frame text,counter_hit_frame text,notes text)"
    print(table_creation_command)
    c.execute(table_creation_command)

    # adding frame list from the csv to the database
    character_csv_path = character_name.replace('_', '-')  # making sure that the correct name of the file is found
    character_frames_csv_path = os.path.dirname(__file__) + f'/frames/{character_csv_path}.csv'
    df = pd.read_csv(character_frames_csv_path)
    movelist = df.values

    # insert data into the tables
    data_insertion_command = f"INSERT INTO {character_name} VALUES(?,?,?,?,?,?,?,?)"
    c.executemany(data_insertion_command, movelist)

    conn.commit()

    # close the connection
    conn.close()


# Querry the database
def show_tables(table_name):
    # create a connection
    database_name = 'characters.db'
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), database_name))

    # create a cursor
    c = conn.cursor()
    print(c.fetchone())
    command_to_excuted = f"SELECT  * FROM {table_name} "
    c.execute(command_to_excuted)
    results = c.fetchall()
    for item in results:
        print(item)


# create the database
def create_db():
    characters = get_all_characters_names()
    # making sure that the there's no - between the names as it causes errors
    for i in range(len(characters)):
        characters[i] = characters[i].replace('-', '_')
    #
    for character in characters:
        create_table(character)


def show_frames(character_name, move):
    # create a connection
    database_name = 'characters.db'
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), database_name))

    # create a cursor
    c = conn.cursor()
    print(c.fetchone())
    command_to_excuted = f"SELECT  * FROM {character_name} WHERE UPPER(command) LIKE UPPER('{move}') "

    command= ''
    c.execute(command_to_excuted)
    results = c.fetchall()
    # for item in results:
    #    print(item)
    return results


# addes spaces between move commands
def add_space(s1):
    temp = []
    s1 = [s1[i] for i in range(len(s1))]
    for i in range(len(s1) - 1):
        temp.append(s1[i])
        if (s1[i].isalpha() and s1[i + 1].isdigit()) or (s1[i].isdigit() and s1[i + 1].isdigit()):
            temp.append(' ')
    temp.append(s1[-1])
    return ''.join(item for item in temp)


def find_move(character_name, move):
    move = move.strip()
    move = add_space(move)

    if len(move) > 1 and (move[0].upper() == 'D' or move[0].upper() == 'U') and (
            move[1].upper() == 'B' or move[1].upper() == 'F'):
        move = move[0] + '/' + move[1:]

    if len(show_frames(character_name, move.replace(' ', ', '))) > 0:
        result = show_frames(character_name, move.replace(' ', ', '))
        return result

    if len(show_frames(character_name, move=move.replace(' ', '+'))) > 0:
        result = show_frames(character_name, move=move.replace(' ', '+'))
        return result


print(find_move('jack7', '12'))
