import discord
from discord.ext import commands
import json

import music_cog
import anime_cog

def main():
    config = json.load(open("config.json", encoding='utf-8-sig'))
    TOKEN = config["discord"]["token"]
    admin = config["admin"]

    intents = discord.Intents().all()
    bot = commands.Bot(command_prefix=config["prefix"], description="Plugin-based Discord music bot", intents=intents)

    bot.add_cog(music_cog.Music(bot))
    bot.add_cog(anime_cog.Anime(bot))

    @bot.command()
    async def foo(ctx, arg):
        await ctx.send(arg)

    @bot.listen()
    async def on_message(message):
        if "Panie Otusie, można" in message.content:
            await message.channel.send("Można. Gdyby to było złe, to Ljungbeck stworzyłby świat inaczej.")

    @bot.command(name='shutdown', help='Shutdown bot by admin.')
    async def shutdown(ctx):
        if ctx.message.author.id in admin:
            await ctx.send("Shutting down...")
            await bot.close()
        else:
            await ctx.send("You are not admin, shutdown not executed")

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

    bot.run(TOKEN)

if __name__ == '__main__':
    main()
