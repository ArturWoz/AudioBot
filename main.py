import discord
from discord.ext import commands
import json
import sys
from player import *
from plugins import Base

def main():
    config = json.load(open("config.json", encoding='utf-8-sig'))
    TOKEN = config["discord"]["token"]
    admin = config["admin"]

    #Plugin list
    for p in Base.plugins:
        print(p)

    intents = discord.Intents().all()
    bot = commands.Bot(command_prefix=config["prefix"], description="Plugin-based Discord music bot", intents=intents)
    players = {}

    @bot.command(name='join', help='Tells the bot to join the voice channel')
    async def join(ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            pl = Player()
            await pl.join(ctx)
            players[ctx.guild] = pl

    @bot.command(name='play', help='To play song')
    async def play(ctx, plugin, url):
        await players[ctx.guild].play(plugin, url)

    @bot.command(name='list', help='To play a playlist')
    async def playlist(ctx, plugin, url):
        await players[ctx.guild].list(plugin, url)

    @bot.command(name='repeat', help='Toggles repeat mode')
    async def repeat(ctx):
        await players[ctx.guild].repeat()

    @bot.command(name='search', help='To search for song')
    async def search(ctx, plugin, *args):
        arguments = ' '.join(args)
        await players[ctx.guild].search(plugin, arguments)

    @bot.command(name='pause', help='To pause the song')
    async def pause(ctx):
        await players[ctx.guild].pause()

    @bot.command(name='stop', help='To stop the song')
    async def stop(ctx):
        await players[ctx.guild].stop()

    @bot.command(name='skip', help='To skip the song')
    async def skip(ctx):
        await players[ctx.guild].skip()

    @bot.command(name='resume', help='To resume the song')
    async def resume(ctx):
        await players[ctx.guild].resume()

    @bot.command(name='queue', help='To show the song queue')
    async def queue(ctx):
        await players[ctx.guild].queue()

    @bot.command(name='shuffle', help='To shuffle the song queue')
    async def shuffle(ctx):
        await players[ctx.guild].shuffle()

    @bot.command(name='select', help='To select from search results')
    async def select(ctx, no):
        await players[ctx.guild].select(no)

    @bot.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(ctx):
        print(players)
        await players[ctx.guild].leave()
        players.pop(ctx.guild)
        print(players)

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
