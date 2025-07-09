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
    players = []

    @bot.command(name='join', help='Tells the bot to join the voice channel')
    async def join(ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            pl = Player()
            await pl.join(ctx)
            players.append(pl)

    @bot.command(name='play', help='To play song')
    async def play(ctx, plugin, url):
        for pl in players:
            print(pl.ctx.guild)
            if ctx.guild == pl.ctx.guild:
                await pl.play(plugin, url)
                print(len(pl.music_queue))

    @bot.command(name='list', help='To play a playlist')
    async def playlist(ctx, plugin, url):
        for pl in players:
            print(pl.ctx.guild)
            if ctx.guild == pl.ctx.guild:
                await pl.list(plugin, url)
                print(len(pl.music_queue))

    @bot.command(name='repeat', help='Toggles repeat mode')
    async def repeat(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.repeat()

    @bot.command(name='search', help='To search for song')
    async def search(ctx, plugin, *args):
        arguments = ' '.join(args)
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.search(plugin, arguments)

    @bot.command(name='pause', help='To pause the song')
    async def pause(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.pause()

    @bot.command(name='stop', help='To stop the song')
    async def stop(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.stop()

    @bot.command(name='skip', help='To skip the song')
    async def skip(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.skip()

    @bot.command(name='resume', help='To resume the song')
    async def resume(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.resume()

    @bot.command(name='queue', help='To show the song queue')
    async def queue(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.queue()

    @bot.command(name='shuffle', help='To shuffle the song queue')
    async def shuffle(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.shuffle()

    @bot.command(name='select', help='To resume playing')
    async def select(ctx, no):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.select(no)

    @bot.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(ctx):
        print(players)
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.leave()
                players.remove(pl)
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
