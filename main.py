import discord
import pytube
from discord.ext import commands
from pytube import Playlist
import random
import asyncio

token_file = open("token.txt", "r")
TOKEN = token_file.read()


def url_from_yt_object(youtube):
    start = 'videoId='
    end = '>'
    s = str(youtube)
    s2 = 'https://www.youtube.com/watch?v=' + s[s.find(start) + len(start):s.rfind(end)]
    print(s2)
    return s2


def main():
    intents = discord.Intents().all()

    bot = commands.Bot(command_prefix='%', description="This is a test bot", intents=intents)

    players = []

    class Player:
        def __init__(self):
            self.music_queue = []
            self.v_client = None
            self.ctx = None
            self.playing = None
            self.search_results = None
            self.two_mins = 0
            self.repeat_state = False

        async def join(self, ctx):
            print("BBB")
            channel = ctx.message.author.voice.channel
            print("BBB")
            self.ctx = ctx
            print("BBB")
            await channel.connect()
            print("BBB")
            try:
                self.v_client = ctx.message.guild.voice_client
            except:
                await self.ctx.send("ERROR")
            print("BBB")

        async def play(self, url):
            if 'list' in url:
                if 'watch' not in url:
                    playlist = Playlist(url)
                    for url in playlist.video_urls:
                        print(url)
                        await self.play(url)
                    return
            url = url.split('&', 1)[0]
            try:
                async with self.ctx.typing():
                    yt = pytube.YouTube(url, use_oauth=True, allow_oauth_cache=True)
                    streams = yt.streams.filter(only_audio=True)
                    filename = streams[0]
                    if not self.v_client.is_playing():
                        self.v_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename.url,
                                                                  before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), after=self.next)
                        await self.ctx.send('**Now playing:** {}'.format(filename.title))
                        self.playing = filename
                    else:
                        await self.ctx.send('**Added to queue:** {}'.format(filename.title))
                        self.music_queue.append(filename)
            except Exception as e:
                string = str(e)
                print("The error is: ", string)

        # async def local(self, filename):
        #     if not self.v_client.is_playing():
        #         try:
        #             async with self.ctx.typing():
        #                 self.v_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename),
        #                                    after=self.next)
        #             await self.ctx.send('**Now playing:** {}'.format(filename))
        #             self.playing = filename
        #         except:
        #             await self.ctx.send("The bot is not connected to a voice channel.")
        #     else:
        #         await self.ctx.send('**Added to queue:** {}'.format(filename))
        #         self.music_queue.append(filename)

        def next(self, err=None):
            if self.repeat_state:  # Check if repeat is enabled
                self.v_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=self.playing.url,
                                                          before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"),
                                   after=self.next)
            elif len(self.music_queue) > 0:
                filename = self.music_queue[0]
                self.music_queue.pop(0)
                self.v_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename.url,
                                                          before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"),
                                   after=self.next)
                self.playing = filename
            else:
                self.playing = None

        async def repeat(self):
            if not self.v_client.is_playing() and not self.v_client.is_paused():
                await self.ctx.send("No song is currently playing. Repeat mode cannot be enabled.")
                return

            self.repeat_state = not self.repeat_state
            if self.repeat_state:
                await self.ctx.send("Repeat mode enabled.")
            else:
                await self.ctx.send("Repeat mode disabled.")

        async def queue(self):
            i = 0
            output = '**Playing now:' + '.** [' + self.playing.title + "](" + self.playing.url + ") \n"
            output = output + "In queue: \n"
            for f in self.music_queue:
                output = output + '**' + str(i + 1) + '.** [' + f.title + "](" + f.url + ") \n"
                i = i + 1
            embed = discord.Embed()
            embed.description = output
            # embed.set_footer(text='Use %select. Will expire in 2 minutes.')
            embed.title = 'Queue:'
            await self.ctx.send(embed=embed)

        async def pause(self):
            if self.v_client.is_playing():
                await self.v_client.pause()
            else:
                await self.ctx.send("The bot is not playing anything at the moment.")

        async def resume(self):
            if self.v_client.is_paused():
                await self.v_client.resume()
            else:
                await self.ctx.send("The bot was not paused.")

        async def stop(self):
            self.music_queue = []
            if self.v_client.is_playing():
                self.v_client.stop()
            else:
                await self.ctx.send("The bot is not playing anything at the moment.")

        async def skip(self):
            if self.v_client.is_playing():
                self.v_client.stop()
            else:
                await self.ctx.send("The bot is not playing anything at the moment.")

        async def leave(self):
            if self.v_client.is_connected():
                await self.v_client.disconnect()
            else:
                await self.ctx.send("The bot is not connected.")

        async def shuffle(self):
            random.shuffle(self.music_queue)
            await self.ctx.send("Shuffled queue!")

        async def search(self, query):
            s = pytube.Search(query)
            self.search_results = s
            output = ''
            for i in range(10):
                url = url_from_yt_object(s.results[i])
                title = s.results[i].title
                output = output + '**' + str(i + 1) + '.** [' + title + "](" + url + ") \n"
            embed = discord.Embed()
            embed.description = output
            embed.set_footer(text='Use %select. Will expire in 2 minutes.')
            embed.title = 'Search results:'
            await self.ctx.send(embed=embed)
            self.two_mins = self.two_mins + 1
            await asyncio.sleep(120)
            self.two_mins = self.two_mins - 1
            if self.two_mins == 0:
                self.search_results = None

        async def select(self, no):
            no = int(no) - 1
            url = url_from_yt_object(self.search_results.results[no])
            await self.play(url)

    @bot.command(name='join', help='Tells the bot to join the voice channel')
    async def join(ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            print("AAAA")
            pl = Player()
            print("AAAA")
            await pl.join(ctx)
            print("AAAA")
            players.append(pl)
            print("AAAA")
            print(pl)

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

    # @bot.command(name='local', help='To play song')
    # async def local(ctx, url):
    #     for pl in players:
    #         if ctx.guild == pl.ctx.guild:
    #             await pl.local(url)
    #             print(len(pl.music_queue))

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

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

    @bot.event
    async def on_voice_state_update(member, before, after):
        if after.channel is None:
            members = before.channel.members
            for person in members:
                if not person.bot:
                    return
            for person in members:
                await person.edit(voice_channel=None)
                print(players)
                for pl in players:
                    if member.guild == pl.ctx.guild:
                        await pl.leave()
                        players.remove(pl)
                print(players)

    # @bot.event
    # async def on_message(message):
    #    await bot.process_commands(message)

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
