import discord
import asyncio

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
    if message.content.startswith('general reposti'):
        await client.send_message(message.channel, 'Hello there!')
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run(TOKEN)