# nathan-bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('NATHAN_DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# [ "Name" : ["Name", "Wins", "WinPercent", "KOs"], ...]
records = {}

total = 0

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


async def printStatement():
    global total, records
    place = 1
    records = dict(sorted(records.items(), reverse=True, key=lambda item: int(item[1][1])))

    mymessage = "{0:8}  | {1:5}  | {2:6} | {3:4}\r\n".format('Name', 'Wins', 'Win % ', 'KOs')
    mymessage = mymessage + "---------------------------------\r\n"
    for record in records.values():
        mymessage = mymessage + "{0:10}|  {1:5} | {2:6} | {3:4}\r\n".format(record[0], record[1], record[2], record[3])

    totMessage = "\nTotal: {total}".format(total = total)

    #Group
    finalMessage = mymessage + totMessage
    
    return finalMessage

async def writeScores():
    global total, records
    fo = open("Leaderboard.txt", "w")

    # [ "Name" : ["Name", "Wins", "WinPercent", "KOs"], ...]
    for record in records.values():
        fo.write(record[0] + "," + str(record[1]) + "," + str(record[3])+"\n")

    fo.close()

async def updatePercentages():
    global records, total

    for record in records.values():
        winPercent = (int(record[1]) / total )*100
        record[2] = str(round(winPercent,2)) + "%"


async def addPercentages():
    global records, total

    for record in records.values():
        winPercent = (int(record[1]) / total )*100
        record.insert(2, str(round(winPercent,2)) + "%")


async def readScores():
    global records
    fo = open("Leaderboard.txt", "r")

    for line in fo.readlines():
        temp = line.strip('\n\r').split(",")
        records[temp[0]] = temp
    fo.close()


async def initValues():
    global records, total

    total = 0
    records = {}
    #initalize records
    await readScores()

    #initalize total
    for record in records.values():
        total = total + int(record[1])

    #Add the percentages
    await addPercentages()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    #

    

@client.event
async def on_message(message):
    global total, records

    #init the scores
    print("----- Init Values ------")
    await initValues()

    sendMessage = False

    if message.author == client.user:
        return

    #Bryson Wins
    if message.content.upper() == '>B':
        records.get('Bryson')[1] = str(int(records.get('Bryson')[1]) + 1)
        total = total + 1
        sendMessage = True
    if message.content.upper() == '>B-':
        records.get('Bryson')[1] = str(int(records.get('Bryson')[1]) - 1)
        total = total - 1
        sendMessage = True

    #Nathan Wins
    if message.content.upper() == '>NG':
        records.get('Nathan')[1] = str(int(records.get('Nathan')[1]) + 1)
        total = total + 1
        sendMessage = True
    if message.content.upper() == '>NG-':
        records.get('Nathan')[1] = str(int(records.get('Nathan')[1]) - 1)
        total = total - 1
        sendMessage = True

    #Nate Wins
    if message.content.upper() == '>NR':
        records.get('Nate')[1] = str(int(records.get('Nate')[1]) + 1)
        total = total + 1
        sendMessage = True
    if message.content.upper() == '>NR-':
        records.get('Nate')[1] = str(int(records.get('Nate')[1]) - 1)
        total = total - 1
        sendMessage = True

    #Jack Wins
    if message.content.upper() == '>J':
        records.get('Jack')[1] = str(int(records.get('Jack')[1]) + 1)
        total = total + 1
        sendMessage = True
    if message.content.upper() == '>J-':
        records.get('Jack')[1] = str(int(records.get('Jack')[1]) - 1)
        total = total - 1
        sendMessage = True


    #Bryon KO
    if message.content.upper() == '>BKO':
        records.get('Bryson')[3] = str(int(records.get('Bryson')[3]) + 1)
        sendMessage = True
    if message.content.upper() == '>BKO-':
        records.get('Bryson')[3] = str(int(records.get('Bryson')[3]) - 1)
        sendMessage = True

    #Nathan KO
    if message.content.upper() == '>NGKO':
        records.get('Nathan')[3] = str(int(records.get('Nathan')[3]) + 1)
        sendMessage = True
    if message.content.upper() == '>NGKO-':
        records.get('Nathan')[3] = str(int(records.get('Nathan')[3]) - 1)
        sendMessage = True

    #Nate KO
    if message.content.upper() == '>NRKO':
        records.get('Nate')[3] = str(int(records.get('Nate')[3]) + 1)
        sendMessage = True
    if message.content.upper() == '>NRKO-':
        records.get('Nate')[3] = str(int(records.get('Nate')[3]) - 1)
        sendMessage = True

    #Jack KO
    if message.content.upper() == '>JKO':
        records.get('Jack')[3] = str(int(records.get('Jack')[3]) + 1)
        sendMessage = True
    if message.content.upper() == '>JKO-':
        records.get('Jack')[3] = str(int(records.get('Jack')[3]) - 1)
        sendMessage = True
        

    if message.content.upper() == '>SCORES':
        sendMessage = True

    if sendMessage:
        await updatePercentages()
        await writeScores()

        toSend = await printStatement()
        await message.channel.send("```" + toSend + "```")


client.run(TOKEN)
