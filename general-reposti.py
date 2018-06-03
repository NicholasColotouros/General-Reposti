import asyncio
import dataloader
import discord
import re
import redditfacade
import shlex
import sys

from discord.ext import commands
from subprocess import run

BOT_TOKEN = dataloader.discordData['bot-token']
ADMIN_ID = dataloader.discordData['admin-id']

bot = commands.Bot(command_prefix=dataloader.discordData['cmd-prefix'], description='Hello there! I\'m General Reposti!')

def is_admin(user):
    return user.id == ADMIN_ID

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    # memes
    if re.search('general reposti', message.content, re.IGNORECASE):
        if re.search('I hate you', message.content, re.IGNORECASE):
            nameToReplyWith = message.author.name
            if(message.author.nick):
                nameToReplyWith = message.author.nick
            await bot.send_message(message.channel, 'It\'s over ' + nameToReplyWith + '. I have the high ground!')
        else:
            await bot.send_message(message.channel, 'Hello there!')

    # process actual commands
    await bot.process_commands(message)

@bot.command(description='Gets the top URL post from r/PrequelMemes and posts it', pass_context=True)
async def shitpost(ctx):
    '''Gets a random post from r/PrequelMemes and posts it'''
    try:
        shitpostUrl = redditfacade.GetShitPostURL()
        await bot.say(shitpostUrl)
    except:
        await bot.say('Impossible.\nPerhaps the archives are incomplete.\n<@' + ADMIN_ID + '> is the droid you\'re looking for to help with this message.')
        raise

@bot.command(description='Restarts General Reposti. Only works if you\'re the admin.', pass_context=True)
async def reboot(ctx):
    '''Restarts General Reposti. Only works if you\'re the admin.'''
    if not is_admin(ctx.message.author):
        await bot.say('You are on this counsel, but we do not grant you the rank of master.\nOnly<@' + ADMIN_ID + '> can reboot me.')
    else:
        await bot.say("BRB coming back as a force ghost")
        run(shlex.split(r"""powershell.exe -file "start_bot.ps1" """))
        sys.exit(0)

bot.run(BOT_TOKEN)