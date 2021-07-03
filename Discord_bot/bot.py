import discord
import os
import requests
import json

client = discord.Client()


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + f" _{json_data[0]['a']}"
    return quote


@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)


client.run('ODYwMjUwNjc5NzI1MTI5NzY4.YN4g4A.ahJLT6FNp1pesxJsf7CnxxDWo0Y')
# client.run(os.getenv('TOKEN'))
