import discord
from discord.ext import commands
import json
import sys

from player import *


def main():
    config = json.load(open("config.json", encoding='utf-8-sig'))
    TOKEN = config["discord"]["token"]
    admin = config["admin"]

    intents = discord.Intents().all()
    bot = commands.Bot(command_prefix=config["prefix"], description="This is a test bot", intents=intents)
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
    async def play(ctx, url):
        for pl in players:
            print(pl.ctx.guild)
            if ctx.guild == pl.ctx.guild:
                await pl.play(url)
                print(len(pl.music_queue))

    @bot.command(name='repeat', help='Toggles repeat mode')
    async def repeat(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.repeat()

    @bot.command(name='local', help='To play song')
    async def local(ctx, url):
         for pl in players:
             if ctx.guild == pl.ctx.guild:
                 await pl.local(url)
                 print(len(pl.music_queue))

    @bot.command(name='search', help='To play song')
    async def search(ctx, *args):
        arguments = ' '.join(args)
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.search(arguments)

    @bot.command(name='pause', help='This command pauses the song')
    async def pause(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.pause()

    @bot.command(name='stop', help='This command pauses the song')
    async def stop(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.stop()

    @bot.command(name='skip', help='This command pauses the song')
    async def skip(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.skip()

    @bot.command(name='resume', help='Resumes the song')
    async def resume(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.resume()

    @bot.command(name='queue', help='Resumes the song')
    async def queue(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.queue()

    @bot.command(name='shuffle', help='Resumes the song')
    async def shuffle(ctx):
        for pl in players:
            if ctx.guild == pl.ctx.guild:
                await pl.shuffle()

    @bot.command(name='select', help='Resumes the song')
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

    # @bot.event
    # async def on_voice_state_update(member, before, after):
    #     if member.id == bot.application_id:
    #         for pl in players:
    #             if member.guild == pl.ctx.guild:
    #                 await pl.leave()
    #                 players.remove(pl)
    #
    #     if after.channel is None:
    #         members = before.channel.members
    #         for person in members:
    #             if not person.bot:
    #                 return
    #         for person in members:
    #             await person.edit(voice_channel=None)
    #             print(players)
    #             for pl in players:
    #                 if member.guild == pl.ctx.guild:
    #                     await pl.leave()
    #                     players.remove(pl)
    #             print(players)

    # @bot.event
    # async def on_message(message):
    #    await bot.process_commands(message)

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
