import discord
import pytubefix as pytube
from pytubefix import Playlist
import random
import asyncio
import os

from spotify import *


def url_from_yt_object(youtube):
    start = 'videoId='
    end = '>'
    s = str(youtube)
    s2 = 'https://www.youtube.com/watch?v=' + s[s.find(start) + len(start):s.rfind(end)]
    print(s2)
    return s2


class Player:
    def __init__(self):
        self.music_queue = []
        self.v_client = None
        self.ctx = None
        self.playing = None
        self.search_results = None
        self.two_mins = 0
        self.repeat_state = False

    def run(self, music):
        self.v_client.play(discord.FFmpegPCMAudio(source=music), after=self.next)

    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        self.ctx = ctx
        await channel.connect()
        try:
            self.v_client = ctx.message.guild.voice_client
        except Exception as e:
            string = str(e)
            await self.ctx.send("**ERROR: **" + string)
            print("The error is: ", string)

    async def spotify(self, url):
        tracks = getTracks(url)
        print("Searching songs...")
        for i in tracks:
            print(i)
            s = pytube.Search(i, "WEB") #, use_oauth=True, allow_oauth_cache=True)
            try:
                await self.youtube(s.videos[0])
            except Exception as e:
                string = str(e)
                await self.ctx.send("**ERROR: **" + string)
                print("The error is: ", string)
            # await asyncio.sleep(20)
        await self.ctx.send('Added Spotify playlist to queue')
        return

    async def youtube(self, video):
        try:
            file = video.streams.filter(only_audio=True)[0]
            name = os.path.join("youtube", file.default_filename)
            file.download(output_path="youtube")
            if not self.v_client.is_playing():
                self.run(name)
                await self.ctx.send('**Now playing:** ' + name)
                self.playing = name
            else:
                await self.ctx.send('**Added to queue:** ' + name)
                self.music_queue.append(name)
        except Exception as e:
            string = str(e)
            await self.ctx.send("**ERROR: **" + string)
            print("The error is: ", string)

    async def play(self, url):
        if 'spotify' in url:
            await self.spotify(url)
            return
        if 'list' in url:
            if 'watch' not in url:
                playlist = Playlist(url)
                for url in playlist.videos:
                    await self.youtube(url)
                await self.ctx.send('Added Youtube playlist to queue')
                return
        try:
            async with self.ctx.typing():
                file = pytube.YouTube(url, "WEB") #, use_oauth=True, allow_oauth_cache=True)
                await self.youtube(file)
        except Exception as e:
            string = str(e)
            await self.ctx.send("**ERROR: **" + string)
            print("The error is: ", string)

    async def local(self, name):
        name = os.path.join("local", name)
        try:
            async with self.ctx.typing():
                if not self.v_client.is_playing():
                    self.run(name)
                    await self.ctx.send('**Now playing:** ' + name)
                    self.playing = name
                else:
                    await self.ctx.send('**Added to queue:** ' + name)
                    self.music_queue.append(name)
        except Exception as e:
            string = str(e)
            await self.ctx.send("**ERROR: **" + string)
            print("The error is: ", string)

    def next(self, err=None):
        if self.repeat_state:  # Check if repeat is enabled
            self.run(self.playing)
        elif len(self.music_queue) > 0:
            filename = self.music_queue[0]
            self.music_queue.pop(0)
            self.run(filename)
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
        outputs = [
            '**Playing now: **' + self.playing + "\n" + "**In queue:** \n"]
        rows = []
        for f in self.music_queue:
            rows.append('**' + str(i + 1) + '.** ' + f + "\n")
            i = i + 1
        i = 0
        for r in rows:
            if len(outputs[i]) + len(r) < 4096:
                outputs[i] = outputs[i] + r
            else:
                i = i + 1
                outputs.append(r)
        for o in outputs:
            embed = discord.Embed()
            embed.description = o
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
        s = pytube.Search(query, "WEB")#, use_oauth=True, allow_oauth_cache=True)
        self.search_results = s
        output = ''
        for i in range(10):
            url = url_from_yt_object(s.videos[i])
            title = s.videos[i].title
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
        url = url_from_yt_object(self.search_results.videos[no])
        await self.play(url)
