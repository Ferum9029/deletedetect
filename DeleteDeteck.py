import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import time

prefix = ' '
bot = commands.Bot(command_prefix=prefix)
messages = []

minute = 60
hour = minute*60
day = hour*24
week = day*7
month = day*30


async def deleting_old():
    while True:
        for message in messages:
            if not time.time() - message.created_at.timestamp() >= hour:
                break
            messages.remove(message)
        await asyncio.sleep(5)


@bot.event
async def on_ready():
    print("Logged in as")
    await deleting_old()


@bot.event
async def on_message_delete(message):
    message_deleted = get(messages, id=message.id)
    if not message_deleted:
        return
    embed = discord.Embed(title=f"{message_deleted.content}",
                          description=f"Удалил <@{message_deleted.author.id}> в <#{message_deleted.channel.id}>",
                          color=0x80ff00)
    await message.channel.send(embed=embed)
    messages.remove(message_deleted)


@bot.event
async def on_message(message):
    messages.append(message)


bot.run('token')
