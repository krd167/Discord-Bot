# bot.py
import os
import random
import html
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests as r
import yfinance as yf

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description="test", intents=intents)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


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

        await ctx.send(embed=embed)
    else:
        await ctx.send("API Failed to work")


@bot.command()
async def trivia(ctx):
    await ctx.send("Welcome to Trivia! - Getting a question now!")
    await ctx.send(ctx.message.author.name)

    def check(message):
        return str(message.author) != str(bot.user.name)

    letters = ['a', 'b', 'c', 'd']
    receive = r.get('https://opentdb.com/api.php?amount=1')
    content = receive.json()
    category = content['results'][0]['category']
    difficulty = content['results'][0]['difficulty']
    question = html.unescape(content['results'][0]['question'])
    answers = []
    for i in range(len(content['results'][0]['incorrect_answers'])):
        answers.append(content['results'][0]['incorrect_answers'][i])
    answers.append(content['results'][0]['correct_answer'])
    random.shuffle(answers)
    a = 0
    b = 1
    c = 2
    d = 3
    await ctx.send(f"{question}")
    for i in range(len(answers)):
        await ctx.send(f"{letters[i]}. {answers[i]}")
    msg = await bot.wait_for("message", check=check)
    #msg2 = str(msg.content).lower()
    print(msg)
    print(msg.content)
    #if str(answers[msg2]) == str(content['results'][0]['correct_answer']):
    #    print('you answered correctly')
    #    await ctx.send("You answered correctly")
    #else:
    #    await ctx.send('you answered wrongly')


###@bot.command()
#async def stock(ctx, ticks: str):
#    ticker = yf.Ticker(ticks)
#    currentPrice
#    symbol
###


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))


@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

bot.run(TOKEN)
