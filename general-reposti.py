import asyncio
import discord
import json
import re
import redditcmds

from discord.ext import commands

with open('secret/data.json') as f:
    data = json.load(f)

BOT_TOKEN = data['discord']['bot-token']
ADMIN_ID = data['discord']['admin-id']

client = discord.Client()
bot = commands.Bot(command_prefix='!', description='Hello there! I\'m General Reposti!\nMy only command is #Shitpost but it doesn\'t work right now.')

@bot.event
async def on_message(message):
    # memes
    if re.search('general reposti', message.content, re.IGNORECASE):
        if re.search('I hate you', message.content, re.IGNORECASE):
            nameToReplyWith = message.author.name
            if(message.author.nick):
                nameToReplyWith = message.author.nick
            await client.send_message(message.channel, 'It\'s over ' + nameToReplyWith + '. I have the high ground!')
        else:
            await client.send_message(message.channel, 'Hello there!')

    # process actual commands
    await bot.process_commands(message)

@bot.command(description='Gets the top URL post from r/PrequelMemes and posts it', pass_context=True)
async def shitpost(ctx):
    try:
        shitpostUrl = redditcmds.GetShitPostURL()
        await bot.say(shitpostUrl)
    except:
        await bot.say('Impossible.\nPerhaps the archives are incomplete.\n<@' + ADMIN_ID + '> is the droid you\'re looking for to help with this message.')
        raise

bot.run(BOT_TOKEN)