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

bot = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if re.search('general reposti', message.content, re.IGNORECASE):
        if re.search('help me', message.content, re.IGNORECASE):
            #TODO: refactor this to a public JSON file or something to avoid hard cording
            client.send_message(message.channel, "Hello there! I'm General Reposti. You can type !shitpost for me to post a meme, but that's under development")
        elif re.search('I hate you', message.content, re.IGNORECASE):
            nameToReplyWith = message.author.name
            if(message.author.nick):
                nameToReplyWith = message.author.nick
            await client.send_message(message.channel, 'It\'s over ' + nameToReplyWith + '. I have the high ground!')
        else:
            await client.send_message(message.channel, 'Hello there!')

    #process actual commands
    await bot.process_commands(message)

@bot.command(description='Gets the top URL post from r/PrequelMemes and posts it', pass_context=True)
async def shitpost(ctx):
    try:
        shitpostUrl = redditcmds.GetShitPostURL()
        await client.send_message(shitpostUrl)
    except:
        await client.send_message(ctx.message.channel, 'Impossible.\nPerhaps the archives are incomplete.\n<@' + ADMIN_ID + '> is the droid you\'re looking for to help with this message.')
        raise

client.run(BOT_TOKEN)