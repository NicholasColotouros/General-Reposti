import asyncio
import dataloader
import discord

from discord.ext import commands

BOT_TOKEN = dataloader.discord_data['bot-token']
BOT_ID = dataloader.discord_data['bot-id']
ADMIN_ID = dataloader.discord_data['admin-id']

bot = commands.Bot(command_prefix=dataloader.discord_data['cmd-prefix'], description='Hello there! I\'m General Reposti!')

def is_admin(user):
    return user.id == ADMIN_ID

def is_reposti(user):
    return user.id == BOT_ID
