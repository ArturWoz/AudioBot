from discord.ext import commands
from player import *
from plugins import Base


class Music (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

        # Plugin list
        for p in Base.plugins:
            print(p)

    @commands.command(name='join', help='Tells the bot to join the voice channel')
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            pl = Player()
            await pl.join(ctx)
            self.players[ctx.guild] = pl

    @commands.command(name='play', help='To play song')
    async def play(self, ctx, plugin, url):
        await self.players[ctx.guild].play(plugin, url)

    @commands.command(name='list', help='To play a playlist')
    async def playlist(self, ctx, plugin, url):
        await self.players[ctx.guild].list(plugin, url)

    @commands.command(name='repeat', help='Toggles repeat mode')
    async def repeat(self, ctx):
        await self.players[ctx.guild].repeat()

    @commands.command(name='search', help='To search for song')
    async def search(self, ctx, plugin, *args):
        arguments = ' '.join(args)
        await self.players[ctx.guild].search(plugin, arguments)

    @commands.command(name='pause', help='To pause the song')
    async def pause(self, ctx):
        await self.players[ctx.guild].pause()

    @commands.command(name='stop', help='To stop the song')
    async def stop(self, ctx):
        await self.players[ctx.guild].stop()

    @commands.command(name='skip', help='To skip the song')
    async def skip(self, ctx):
        await self.players[ctx.guild].skip()

    @commands.command(name='resume', help='To resume the song')
    async def resume(self, ctx):
        await self.players[ctx.guild].resume()

    @commands.command(name='queue', help='To show the song queue')
    async def queue(self, ctx):
        await self.players[ctx.guild].queue()

    @commands.command(name='shuffle', help='To shuffle the song queue')
    async def shuffle(self, ctx):
        await self.players[ctx.guild].shuffle()

    @commands.command(name='select', help='To select from search results')
    async def select(self, ctx, no):
        await self.players[ctx.guild].select(no)

    @commands.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(self, ctx):
        print(self.players)
        await self.players[ctx.guild].leave()
        self.players.pop(ctx.guild)
        print(self.players)