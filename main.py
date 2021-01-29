import discord
import requests
import os
import json
from discord.ext import commands
from keep_alive import keep_alive

PREFIX = ("$")
bot = commands.Bot(command_prefix=PREFIX, description='Hi')

client = discord.Client()

from datetime import datetime, timedelta
HOUR = timedelta(hours=1)
last_update = datetime.now()

def get_value():
  response = requests.get("https://financialmodelingprep.com/api/v3/profile/GME?apikey=" + os.getenv('API'))
  json_data = json.loads(response.text)
  gmeprice = json_data[0]['price']
  return gmeprice

init = False

if init != True:
  value = get_value()
  init = True

now = datetime.now()
if now - last_update > HOUR:
    value = get_value()
    last_update = now

@client.event 
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  gme_string = str(value)
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="GME @ $" + gme_string))
  #await client.change_presence(status=discord.Status.idle, activity=discord.Game("GME @ $" + gme_string))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('$gmestock'):
    gmestock = get_value()
    await message.channel.send(gmestock)


keep_alive()

client.run(os.getenv('TOKEN'))