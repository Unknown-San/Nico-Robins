import asyncio
from aiohttp import ClientSession
from Python_ARQ import ARQ
import random
from pyrogram import filters
from SaitamaRobot import pbot as bot

api_key = ('RIZMUN-PTUQTE-ZDXUWJ-AGZJVR-ARQ') # get it from @arqrobot
api_url = "https://thearq.tech"


@bot.on_message(filters.command('wall'))
async def main(_,message):
    session = ClientSession()
    wall_ = message.text.replace(message.text.split(' ')[0], '')
    arq = ARQ(api_url, api_key, session)
    results = await arq.wall(wall_)
    wallpaper = results.result
    x = random.choice(wallpaper)
    print(x.url_image)
    await message.reply_photo(x.url_image)
    await session.close()
