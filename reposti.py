import asyncio
import dataloader
import discord
import re
import redditfacade
import shlex
import sys

from discord.ext import commands
from prawcore import NotFound
from prawcore import Forbidden
from subprocess import run

BOT_TOKEN = dataloader.discord_data['bot-token']
BOT_ID = dataloader.discord_data['bot-id']
ADMIN_ID = dataloader.discord_data['admin-id']

bot = commands.Bot(command_prefix=dataloader.discord_data['cmd-prefix'], description='Hello there! I\'m General Reposti!')

def is_admin(user):
    return user.id == ADMIN_ID

def is_reposti(user):
    return user.id == BOT_ID

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_error(event):
    print("Error raised: " + event)

@bot.event
async def on_message(message):

    # prevent responding to our own messages
    if is_reposti(message.author):
        return

    # memes
    if re.search('general reposti', message.content, re.IGNORECASE):
        if re.search('I hate you', message.content, re.IGNORECASE):
            recipient_name_to_use = message.author.name
            if(message.author.nick):
                recipient_name_to_use = message.author.nick
            await bot.send_message(message.channel, 'It\'s over ' + recipient_name_to_use + '. I have the high ground!')
        else:
            await bot.send_message(message.channel, 'Hello there!')

    # process actual commands
    await bot.process_commands(message)

@bot.command(description='Gets the top URL post from r/PrequelMemes and posts it', pass_context=True)
async def shitpost(ctx, subreddit : str = '/r/PrequelMemes'):
    #TODO refactor this mess
    '''Gets a random post from r/PrequelMemes and posts it'''
    try:
        if redditfacade.is_valid_subreddit(subreddit):
            if redditfacade.subreddit_exists(subreddit):
                shitpost = redditfacade.get_shitpost(subreddit)
                await bot.say('Post from ' + subreddit + ':\n' + shitpost[0] + '\n' + shitpost[1])
            else:
                await bot.say('Unable to find Subreddit: ' + subreddit)
        else:
            await bot.say('Subreddit must be in the for /r/PrequelMemes, r/PrequelMemes or PrequelMemes')
    except Forbidden:
        await bot.say('Subreddit ' + subreddit + ' is inaccessible. It might be banned or private.')
    except:
        await bot.say('Impossible.\nPerhaps the archives are incomplete.\n<@' + ADMIN_ID + '> is the droid you\'re looking for to help with this message.')
        raise

@bot.command(description='Restarts General Reposti. Only works if you\'re the admin.', pass_context=True)
async def reboot(ctx):
    '''Restarts General Reposti. Only works if you\'re the admin.'''
    if not is_admin(ctx.message.author):
        await bot.say('You are on this counsel, but we do not grant you the rank of master.\nOnly<@' + ADMIN_ID + '> can reboot me.')
    else:
        await bot.say("If you strike me down I shall become more powerful than you can possibly imagine.")
        run(shlex.split(r"""powershell.exe -file "start_bot.ps1" """))
        sys.exit(0)
