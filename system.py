import re
import reposti
import shlex
import sys

from discord.ext import commands
from subprocess import run

@reposti.bot.event
async def on_ready():
    print('Logged in as')
    print(reposti.bot.user.name)
    print(reposti.bot.user.id)
    print('------')

@reposti.bot.event
async def on_error(event):
    print("Error raised: " + event)

@reposti.bot.event
async def on_message(message):

    # prevent responding to our own messages
    if reposti.is_reposti(message.author):
        return

    ctx = await reposti.bot.get_context(message)

    # memes
    if re.search('general reposti', message.content, re.IGNORECASE):
        if re.search('I hate you', message.content, re.IGNORECASE):
            recipient_name_to_use = message.author.name
            if(message.author.nick):
                recipient_name_to_use = message.author.nick
            await ctx.send('It\'s over ' + recipient_name_to_use + '. I have the high ground!')
        else:
            await ctx.send('Hello there!')

    # process actual commands
    await reposti.bot.process_commands(message)

@reposti.bot.command(description='Restarts General Reposti. Only works if you\'re the admin.', pass_context=True)
async def reboot(ctx):
    '''Restarts General Reposti. Only works if you\'re the admin.'''
    if not reposti.is_admin(ctx.author):
        await ctx.send('You are on this counsel, but we do not grant you the rank of master.\nOnly<@' + str(reposti.ADMIN_ID) + '> can reboot me.')
    else:
        await ctx.send("If you strike me down I shall become more powerful than you can possibly imagine.")
        run(shlex.split(r"""powershell.exe -file "start_bot.ps1" """))
        sys.exit(0)

@reposti.bot.event
async def on_command_error(ctx, err):
    ctxstr = 'Error raised by (' + ctx.message.author.name + ') with message (' + ctx.message.content + '):\n'
    fullerr = ctxstr + str(err) + '\n'
    print(fullerr) # TODO log the bottom 2 cases to file
    if isinstance(err, commands.CommandNotFound):
        return
    elif isinstance(err, commands.BadArgument):
        await ctx.send('You had a bad argument when using the command \'' + ctx.command.name + '\'. Try again.')
    else:
        await ctx.send('The command was so intense it made me shid. Help me <@' + str(reposti.ADMIN_ID) + '>.\n' + fullerr)
