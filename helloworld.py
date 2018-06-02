import discord
import asyncio
import re
import pythonmessages

TOKEN = 'NDUyNDcwNjUyNTc0NzYwOTgw.DfQ_Vw.irfiJYJDHzEm2B7SN0l4KefnPhg'

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith("!shitpost"):
        try:
            shitpostUrl = pythonmessages.shitpost()
            await client.send_message(shitpostUrl)
        except:
            await client.send_message(message.channel, 'Impossible. Perhaps the archives are incomplete. @USB Connector#3714 might have more info.')
            raise

    if re.search('general reposti', message.content, re.IGNORECASE):
        if re.search('I hate you', message.content, re.IGNORECASE):
            nameToReplyWith = message.author.name
            if(message.author.nick):
                nameToReplyWith = message.author.nick
            await client.send_message(message.channel, 'It\'s over ' + nameToReplyWith + '. I have the high ground!')
        else:
            await client.send_message(message.channel, 'Hello there!')
    
client.run(TOKEN)