# bot.py
from ntpath import join
import os
from os.path import join,dirname
import discord
from discord.ext import commands
from discord.utils import get
import json
import requests
from dotenv import load_dotenv
from newsapi import NewsApiClient

description = '''Main Discord bot for The Land of the Free!

Hopefully this will do something useful:)
'''
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='>', description=description, intents=intents)


dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_TOKEN')
NEWSKEY=os.getenv('NEWSAPI')


newsapi = NewsApiClient(api_key=NEWSKEY)

members = []


async def getNews():
    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(q='Xbox',
                                            sources='IGN,the-verge',
                                            category='business',
                                            language='en',
                                            country='us')

    # /v2/everything
    all_articles = newsapi.get_everything(q='bitcoin',
                                        sources='bbc-news,the-verge',
                                        domains='bbc.co.uk,techcrunch.com',
                                        from_param='2017-12-01',
                                        to='2017-12-12',
                                        language='en',
                                        sort_by='relevancy',
                                        page=2)

    # /v2/sources
    sources = newsapi.get_sources()

async def getmeme():
    resp = requests.get('https://meme-api.herokuapp.com/gimme')
    return json.loads(resp.content).get('url')

async def getUsers():
    print([member.name for member in members])

@bot.event
async def on_ready():
    print(bot.guilds)
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    
    for guilds in bot.guilds:
        for member in guild.members:
            members.append(member)
    
    print([member.name for member in members])


    print(
        f'{bot.user} (ID: {bot.user.id}) has connected to Discord!\n'
        f'{guild.name} (ID: {guild.id})'
        )


@bot.event
async def on_member_join(member):
    
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to The Land of the Free!'
    )
    print(member.roles)

@bot.event
async def on_reaction_add(reaction, user):

    print(reaction)
    print(user)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    elif "bad bot" in str(message.content).lower():
        print(message.author)
        if str(message.author)[:-5] == "TitanGusang":
            response = 'Bitch'
        else:
            response = "I am sorry for my actions, " + str(message.author)[:-5]

        await message.channel.send(response)

    elif "good bot" in str(message.content).lower():
        response = 'Thank you kind human'
        await message.channel.send(response)

    elif "apologize bot" in str(message.content).lower():
        response = "I am sorry"
        await message.channel.send(response)

    elif 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! :balloon: :birthday:')

    elif str(message.content).lower() == '>suck a dick':
        await message.channel.send('https://tenor.com/view/yes-hamster-carrot-bj-blow-job-gif-15498598')
 
@bot.command(description='Get a random meme!', pass_context=True)
async def meme(ctx):
    url = await getmeme()
    response = "Not here buckaroo"
    if str(ctx.channel) == "memes":
        await ctx.channel.send(url)
    else:
        await ctx.channel.send(response)


bot.run(TOKEN)
