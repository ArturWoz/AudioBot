import discord
from discord.ext import commands

import json
import sys

import music_cog

def main():
    config = json.load(open("config.json", encoding='utf-8-sig'))
    TOKEN = config["discord"]["token"]
    admin = config["admin"]

    intents = discord.Intents().all()
    bot = commands.Bot(command_prefix=config["prefix"], description="Plugin-based Discord music bot", intents=intents)

    bot.add_cog(music_cog.Music(bot))

    @bot.command(name='shutdown', help='Shutdown bot by admin.')
    async def shutdown(ctx):
        if str(ctx.message.author.id) in admin:
            await bot.close()
            sys.exit("Shutdown by admin")

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

    bot.run(TOKEN)

if __name__ == '__main__':
    main()
