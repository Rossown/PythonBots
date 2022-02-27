# bot.py
from dis import disco
import os
from os.path import join,dirname
from unicodedata import name
import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
from dotenv import load_dotenv
from newsapi import NewsApiClient
import json
import requests
import logging

loggingFile = join(dirname(__file__), "..", "logs", "discord.log")
logging.basicConfig(filename=loggingFile, filemode='w', format='%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

description = '''Main Discord bot for The Land of the Free!

Hopefully this will do something useful:)'''

intents = discord.Intents.default()
intents.members = True


dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_TOKEN')
NEWSKEY=os.getenv('NEWSAPI')


newsapi = NewsApiClient(api_key=NEWSKEY)

members = []

bot = commands.Bot(command_prefix='>', description=description, intents=intents)


# async def getNews():
#     # /v2/top-headlines
#     top_headlines = newsapi.get_top_headlines(q='Xbox',
#                                             sources='IGN,the-verge',
#                                             category='business',
#                                             language='en',
#                                             country='us')

#     # /v2/everything
#     all_articles = newsapi.get_everything(q='bitcoin',
#                                         sources='bbc-news,the-verge',
#                                         domains='bbc.co.uk,techcrunch.com',
#                                         from_param='2017-12-01',
#                                         to='2017-12-12',
#                                         language='en',
#                                         sort_by='relevancy',
#                                         page=2)

#     # /v2/sources
#     sources = newsapi.get_sources()


# CUSTOM METHODS
async def getmeme():
    resp = requests.get('https://meme-api.herokuapp.com/gimme')
    return json.loads(resp.content).get('url')

async def getUsers():
    print([member.name for member in members])


# COMMANDS

@bot.command(name='meme', description='Get a random meme!', pass_context=True)
async def meme(ctx):
    logger.info(f'{ctx.author.name} has requested a meme')
    url = await getmeme()
    response = "Not here buckaroo"
    if str(ctx.channel) == "memes" or str(ctx.channel) == "dev":
        await ctx.send(url)
    else:
        await ctx.send(response)


@bot.command(name='test', description='Testing method', pass_context=True)
@has_permissions(manage_roles=True)
async def test(ctx, argMember: discord.Member, argRole: discord.Role):
    logger.info(f'Inside test method.')

    member = argMember
    roles = argRole

    logger.info(f'ARG: {argRole}')
    logger.info(f'MEMBER: {member}')
    logger.info(f'Role: {roles}')
    await member.add_roles(roles)

    logger.info(f'{member} wants roll: {roles}')
    await ctx.send(f'{member}: now has the {roles} role!')
@test.error
async def test_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permissions to do that!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send('I cound not find that member or role...')
    else:
        logger.error(str(error))


@bot.command(name='info', description='Get information about a user.', pass_context=True)
async def info(ctx, *, member: discord.Member):
    """Tells you some info about the member."""
    fmt = '{0} joined on {0.joined_at} and has {1} roles.'
    await ctx.send(fmt.format(member, len(member.roles)))
@info.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I cound not find that member...')

# EVENTS
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
    logger.info(f'{bot.user} (ID: {bot.user.id}) has connected to Discord!')


@bot.event
async def on_member_join(member):
    logger.info(f'{member.name} (AKA {member.display_name}) has joined the server')

    #Auto add as a citizen
    roleToAdd = get(member.guild.roles, name="Citizen")
    await member.add_roles(roleToAdd)

    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to The Land of the Free!'
    )
    logger.info(f'{member.name} was assigned the following roles: {member.roles}')

# @bot.event
# async def on_reaction_add(reaction, user):

#     print(reaction)
#     print(user)

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     elif "bad bot" in str(message.content).lower():
#         print(message.author)
#         if str(message.author)[:-5] == "TitanGusang":
#             response = 'Bitch'
#         else:
#             response = "I am sorry for my actions, " + str(message.author)[:-5]

#         await message.channel.send(response)

#     elif "good bot" in str(message.content).lower():
#         response = 'Thank you kind human'
#         await message.channel.send(response)

#     elif "apologize bot" in str(message.content).lower():
#         response = "I am sorry"
#         await message.channel.send(response)

#     elif 'happy birthday' in message.content.lower():
#         await message.channel.send('Happy Birthday! :balloon: :birthday:')

#     elif str(message.content).lower() == '>suck a dick':
#         await message.channel.send('https://tenor.com/view/yes-hamster-carrot-bj-blow-job-gif-15498598')
 

bot.run(TOKEN)
