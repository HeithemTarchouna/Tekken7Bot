import sqlite3
import csv
import os
import pandas as pd
from scrapper import get_all_characters_names

DATABASE_NAME = 'characters.db'


#
# create a table
def create_table(character_name):
    # create a connection
    database_name = DATABASE_NAME
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), database_name))

    # create a cursor
    c = conn.cursor()

    # create the table
    table_creation_command = f"CREATE TABLE if not exists {character_name}(command text, hit_level text,damage text,start_up_frame text,block_frame text,hit_frame text,counter_hit_frame text,notes text)"
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


def create_db():
    characters = get_all_characters_names()
    # making sure that the there's no - between the names as it causes errors
    for i in range(len(characters)):
        characters[i] = characters[i].replace('-', '_')
    #
    for character in characters:
        create_table(character)


show_tables('akuma')
