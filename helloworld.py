import discord
from discord.ext import commands
import asyncio
import re
import redditcmds

TOKEN = 'NDUyNDcwNjUyNTc0NzYwOTgw.DfQ_Vw.irfiJYJDHzEm2B7SN0l4KefnPhg'
client = discord.Client()

bot = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    try:
        # meme text
        if re.search('general reposti', message.content, re.IGNORECASE):
            if re.search('I hate you', message.content, re.IGNORECASE):
                nameToReplyWith = message.author.name
                if(message.author.nick):
                    nameToReplyWith = message.author.nick
                await client.send_message(message.channel, 'It\'s over ' + nameToReplyWith + '. I have the high ground!')
            else:
                await client.send_message(message.channel, 'Hello there!')

        #process actual commands
        await bot.process_commands(message)
    except:
        await client.send_message(message.channel, 'Impossible.\nPerhaps the archives are incomplete.\n<@96369236611457024> might have more info on this issue.')
        raise

@bot.command(description='Gets the top URL post from r/PrequelMemes and posts it', pass_context=True)
async def shitpost(ctx):
    await client.send_message(ctx.message.channel, 'doot')
    try:
        shitpostUrl = redditcmds.GetShitPostURL()
        await client.send_message(shitpostUrl)
    except:
        await client.send_message(ctx.message.channel, 'Impossible.\nPerhaps the archives are incomplete.\n<@96369236611457024> might have more info on this issue.')
        raise

client.run(TOKEN)