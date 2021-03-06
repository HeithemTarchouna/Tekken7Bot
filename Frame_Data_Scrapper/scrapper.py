from bs4 import BeautifulSoup
import requests
import os
import urllib.request
import pandas as pd


def get_character_frames(char_name):
    data_frames = []
    fid = urllib.request.urlopen(f'https://rbnorway.org/{char_name}-t7-frames/')

    webpage = fid.read().decode('utf-8', errors='ignore')
    columns = ['Command', 'Hit level', 'Damage', 'Start up frame', 'Block frame	', 'Hit frame', 'Counter hit frame',
               'Notes']

    soup = BeautifulSoup(webpage, 'lxml')

    for row in soup.find_all('tr'):
        col_num = 0
        all_row = []

        for data in row.find_all('td')[0:8]:

            all_row.append(data.text)
            col_num = col_num + 1
            if len(all_row) == 8:
                data_frames.append(all_row)

    df = pd.DataFrame(data=data_frames, columns=columns)
    df.to_csv(f'{os.path.dirname(__file__)}/frames/{char_name}.csv', index=False)


def get_all_characters_names():
    characters_html_content = requests.get('https://altarofgaming.com/tekken-7-characters-roster/').text

    character_soup = BeautifulSoup(characters_html_content, 'lxml')
    character_list_html = character_soup.find('ul', class_='toc_list')

    character_list_items_html = character_list_html.find_all('li')
    character_list = []

    for item in character_list_items_html:
        character_list.append(item.text.replace(item.text.split(' ')[0], '').strip().replace(' ', '-'))
    character_list[19] = 'Jack7'  # correct a spelling error of the name to match the rbnorway character name
    character_list.remove('Panda')
    return character_list


def get_all_character_frames_to_csv():
    print(get_all_characters_names())
    characters = get_all_characters_names()
    parent_directory = os.path.dirname(__file__)
    directory = 'frames'
    os.mkdir(os.path.join(parent_directory, directory))
    for character_name in characters:
        get_character_frames(character_name)
