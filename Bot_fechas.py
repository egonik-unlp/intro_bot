import os 
import json
import discord
from dotenv import load_dotenv
from collections import Counter
import requests
from functools import wraps 
from datetime import datetime

JSON_URL = 'https://raw.githubusercontent.com/egonik-unlp/intro_bot/main/prueba.json'

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN2")
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()
counter = Counter()

dates_aux = requests.get(JSON_URL).json()
format_fechas = lambda x: datetime.strptime(x, "%d/%m/%Y")
dates = {k:format_fechas(v) for k,v in dates_aux.items()}

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

def logger(counter):
    @wraps
    def logger_wrapper(func):
        def counter_wrapper(*args, **kwargs):
            func()
            counter[func.__name__] += 1
            with open('counter.json', 'w') as file:
                json.dump(counter, file)
        return counter_wrapper
    return logger_wrapper
    


def parser(func):
    @wraps
    def dec_fechas(func):
        content = func(fechas)
        return tuple([(f'{k} ->{v}') for k,v in content.items()])
    return dec_fechas

@logger(counter)
@parser(dates)
def fecha(fechas):
    return {k:datetime.strftime(v, "%d/%m/%Y") for k,v in fechas.items()}



@parser(dates)
def cuanto_falta(fechas):
    return {k: f' faltan {(v - datetime.now()).days} dias' for k,v in fechas.items() if (v - datetime.now()).days > 0 }



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == 'fecha!':
        response = fecha()
        await message.channel.send('\n'.join(response))
    if message.content == 'cuanto!':
        response = cuanto_falta()
        await message.channel.send('\n'.join(response))


client.run(TOKEN)
