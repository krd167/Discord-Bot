# bot.py
import asyncio
import os
from datetime import datetime
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
import requests as r
import feedparser as fp
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

"""
@bot.command(aliases=["CN", "cn"])
async def chuck(ctx):
    results = r.get("https://api.chucknorris.io/jokes/random")
    if results.status_code == 200:
        try:
            content = results.json()
            embed = discord.Embed(description=content['value'], color=discord.Color.red())
            embed.set_thumbnail(url=content['icon_url'])
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        except Exception:
            await ctx.send('Failed to create Embed')

        try:
            await ctx.send(embed=embed)
        except Exception:
            print("Failed for some reason")
    else:
        try:
            await ctx.send("API Failed to work")
        except Exception:
            print("Failed for some reason")
"""

@tasks.loop(minutes=5)
async def gamerant_feed():
    datafeed = fp.parse('https://gamerant.com/feed')  # RSS feed for gamerant
    with open('latest.json') as json_file:  # function to oppen json file and read in the latest title
        data = json.load(json_file)
    with open('channels.json') as json_file:  # Function to open and read in the channels
        channels = json.load(json_file)
    for item in datafeed.entries:  # big loop to get most recent rss data and post it to discord channels
        if str(item.title) == str(data['latest']):
           break
        #print(item.title)  # Needed for troubleshooting only
        for chan in channels['Gamerant']:  # iterates through channels in the json for "gamerant"
            await asyncio.sleep(2)
            rsswrite = bot.get_channel(int(chan))  # gets the channel number
            message = "@GAMERANT " + item.link  # build the message to send in the channel based on the role
            await rsswrite.send(message)  # posts the article to the correct channel *hopefully*
    data['latest'] = datafeed.entries[0].title  # set the json file to the earliest title
    data = json.dumps(data, indent=4)  # prep to save the json data
    with open("latest.json", "w") as outfile:  # function to write the json data to the file
        outfile.write(data)


@tasks.loop(minutes=10)
async def UpdateChannel():
    channel = bot.get_channel(1057370819719860234)
    print(channel)
    a = datetime(2023, 2, 10, 0, 0, 0)
    b = datetime.now()
    c = a-b
    days = c.days
    hours = int(c.seconds/3600)
    minutes = int((c.seconds - (hours*3600))/60)
    message = str(days) +" Days " + str(hours) + " Hours"
    print(message)
    await channel.edit(name=message)


@UpdateChannel.before_loop
async def before_updatechannel():
    await bot.wait_until_ready()


@gamerant_feed.before_loop
async def before_gamerant_feed():
    await bot.wait_until_ready()

#UpdateChannel.start()
gamerant_feed.start()
bot.run(TOKEN)
