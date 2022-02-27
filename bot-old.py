# bot.py
import os
import discord
import json
import requests
from dotenv import load_dotenv
from newsapi import NewsApiClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_TOKEN')
NEWSKEY=os.getenv('NEWSAPI')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

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

@client.event
async def on_ready():
    print(client.guilds)
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    for guilds in client.guilds:
        for member in guild.members:
            members.append(member)
    
    print([member.nick or member.name for member in members])


    print(
        f'{client.user} has connected to Discord!\n'
        f'{guild.name} (id: {guild.id})'
        )
    # async for member in guild.fetch_members(limit=None):
    #     print(f'{member}, {member.id}')


@client.event
async def on_member_join(member):
    
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to The Land of the Free!'
    )
    print(member.roles)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print("CHANNEL: " + str(message.channel))

    
    if str(message.content).lower() == '>meme':
        url = await getmeme()
        response = "Not here buckaroo"
        if str(message.channel) == "memes":
            await message.channel.send(url)
        else:
            await message.channel.send(response)

    elif "bad bot" in str(message.content).lower():
        response = 'Bitch'
        await message.channel.send(response)

    elif "good bot" in str(message.content).lower():
        response = 'Thank you kind human'
        await message.channel.send(response)
        
    elif 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! :ballon: :birthday:')


client.run(TOKEN)
