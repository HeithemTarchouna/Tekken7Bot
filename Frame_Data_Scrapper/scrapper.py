from bs4 import BeautifulSoup
import requests
import os
import urllib.request
import pandas as pd


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_character_frames(char_name):
    fid = urllib.request.urlopen(f'https://rbnorway.org/{char_name}-t7-frames/')

    webpage = fid.read().decode('utf-8', errors='ignore')
    columns = ['Command', 'Hit level', 'Damage', 'Start up frame', 'Block frame	', 'Hit frame', 'Counter hit frame',
               'Notes']
    all_row = []

    soup = BeautifulSoup(webpage, 'lxml')

    for row in soup.find_all('tr'):
        for data in row.find_all('td'):
            all_row.append(data.text)
    data = list(divide_chunks(all_row, 8))
    print(data)
    df = pd.DataFrame(data=data, columns=columns)
    df.to_csv(f'{os.path.dirname(__file__)}/frames/{char_name}.csv', index=False)


def get_all_characters_names():
    characters_html_content = requests.get('https://altarofgaming.com/tekken-7-characters-roster/').text

    character_soup = BeautifulSoup(characters_html_content, 'lxml')
    character_list_html = character_soup.find('ul', class_='toc_list')

    character_list_items_html = character_list_html.find_all('li')
    character_list = []

    for item in character_list_items_html:
        character_list.append(item.text.replace(item.text.split(' ')[0], '').strip().replace(' ', '-'))
    return character_list


print(get_all_characters_names())
characters = get_all_characters_names()
characters[19] = 'jack7'
characters.remove('Panda')

parent_directory = os.path.dirname(__file__)
directory = 'frames'
os.mkdir(os.path.join(parent_directory, directory))

for character_name in characters:
    get_character_frames(character_name)
