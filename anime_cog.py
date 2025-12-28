import discord
from discord.ext import commands
from anime_ping import find_watchers, fetch_user, get_media
import json
from collections import defaultdict
from deranged import deranged_meter
import datetime
import re
# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>')

def cleanhtml(raw_html):
  return re.sub(CLEANR, '', raw_html)

def date_to_unix(date):
    day = date.get('day') if date.get('day') is not None else 0
    month = date.get('month') if date.get('month') is not None else 0
    year = date.get('year') if date.get('year') is not None else 0
    try:
        date_obj = datetime.date(year, month, day)
        datetime_obj = datetime.datetime.combine(date_obj, datetime.time())
    except:
        return 0
    return int(datetime_obj.timestamp())

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.servers = defaultdict(dict)

        config = json.load(open("config.json", encoding='utf-8-sig'))
        self.admin = config["admin"]

        try:
            with open('anilist.json', 'r') as file:
                self.servers.update(json.load(file))
            print(self.servers)
        except:
            print("No Anilist JSON!")

        # self.servers = {511898314564960256: {}}

    @commands.command(name='add-anilist', help='Adds anilist username for anime pings')
    async def add(self, ctx, username):
        self.servers[str(ctx.guild.id)][username] = ctx.message.author.id
        with open('anilist.json', 'w', encoding='utf-8') as f:
            json.dump(self.servers, f, ensure_ascii=False, indent=4)
        await ctx.send(f"Added {username} to this server!")

    @commands.command(name='remove-anilist', help='Removes anilist username from anime pings')
    async def remove(self, ctx, username):
        print(self.servers[str(ctx.guild.id)])
        if self.servers[str(ctx.guild.id)][username] == ctx.message.author.id or ctx.message.author.id in self.admin:
            self.servers[str(ctx.guild.id)].pop(username)
            with open('anilist.json', 'w', encoding='utf-8') as f:
                json.dump(self.servers, f, ensure_ascii=False, indent=4)
            await ctx.send(f"Removed {username} from this server!")
        else:
            await ctx.send(f"You have not registered as {username} and you are not admin")


    @commands.command(name='aniping', help='Ping users who watched an anime')
    async def aniping(self, ctx, *args):
        name = ' '.join(args)
        watchers, title = find_watchers(self.servers[ctx.guild.id].keys(), name, 'ANIME')
        await ctx.send(f"Pinging {title} watchers:")
        for user in watchers:
            user_id = self.servers[ctx.guild.id][user]
            await ctx.send(f"<@{user_id}>")

    @commands.command(name='mangaping', help='Ping users who read a manga')
    async def mangaping(self, ctx, *args):
        name = ' '.join(args)
        watchers, title = find_watchers(self.servers[ctx.guild.id].keys(), name, 'MANGA')
        await ctx.send(f"Pinging {title} readers:")
        for user in watchers:
            user_id = self.servers[ctx.guild.id][user]
            await ctx.send(f"<@{user_id}>")

    async def default_username(self, ctx):
        try:
            server_dict = self.servers[str(ctx.guild.id)]
            user = ctx.message.author.id
            print(server_dict)
            username = (list(server_dict.keys())[list(server_dict.values()).index(user)])
            return username
        except Exception as e:
            print(e)
            await ctx.send("No username specified and you do not have added AniList username")
            return None

    @commands.command(name='fetch', help='Show user stats')
    async def fetch(self, ctx, username=None):
        if username is None:
            username = await self.default_username(ctx)
        if username is None:
            return

        data = fetch_user(username)

        embed = discord.Embed(
            title=username,
            url=f"https://anilist.co/user/{username}",
            color=discord.Colour.blurple(),
            description=f"Created at: <t:{data.get('createdAt')}:d>"
        )
        embed.set_thumbnail(url=data.get('avatar').get('medium'))
        embed.set_image(url=data.get('bannerImage'))

        anistats = data.get('statistics').get('anime')
        embed.add_field(name="Anime stats", value="", inline=False)
        embed.add_field(name="Total Anime", value=anistats.get('count'), inline=True)
        embed.add_field(name="Days Watched", value=round((anistats.get('minutesWatched')/60/24), 2), inline=True)
        embed.add_field(name="Mean Score", value=anistats.get('meanScore'), inline=True)

        anigenres = anistats.get('genres')
        embed.add_field(name="Most watched genres", value="", inline=False)
        embed.add_field(name=anigenres[0].get('genre'), value=anigenres[0].get('count'), inline=True)
        embed.add_field(name=anigenres[1].get('genre'), value=anigenres[1].get('count'), inline=True)
        embed.add_field(name=anigenres[2].get('genre'), value=anigenres[2].get('count'), inline=True)

        mangastats = data.get('statistics').get('manga')
        embed.add_field(name="Manga stats", value="", inline=False)
        embed.add_field(name="Total Manga", value=mangastats.get('count'), inline=True)
        embed.add_field(name="Chapters Read", value=mangastats.get('chaptersRead'), inline=True)
        embed.add_field(name="Mean Score", value=mangastats.get('meanScore'), inline=True)

        mangagenres = mangastats.get('genres')
        embed.add_field(name="Most read genres", value="", inline=False)
        embed.add_field(name=mangagenres[0].get('genre'), value=mangagenres[0].get('count'), inline=True)
        embed.add_field(name=mangagenres[1].get('genre'), value=mangagenres[1].get('count'), inline=True)
        embed.add_field(name=mangagenres[2].get('genre'), value=mangagenres[2].get('count'), inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='deranged', help="Show user's derangement")
    async def deranged_meter(self, ctx, username=None):
        if username is None:
            username = await self.default_username(ctx)
        if username is None:
            return

        abso, rel, worst, avatar = deranged_meter(username)

        embed = discord.Embed(
            title=username + "'s deranged meter",
            color=discord.Colour.blurple(),
        )

        embed.set_thumbnail(url=avatar)
        embed.add_field(name="Absolute deranged meter:", value=abso, inline=True)
        embed.add_field(name="Relative deranged meter:", value=rel, inline=True)
        embed.add_field(name="The most deranged anime:", value=f"{worst[1]} - {worst[0]}", inline=True)

        embed.add_field(name="", value=f"[User's AniList page](https://anilist.co/user/{username})", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='anime', help="Show anime details")
    async def anime(self, ctx, *args):
        media_name = ' '.join(args)
        data = get_media(media_name, "ANIME")

        name = data.get('title')
        title = ""
        if name.get('english') is not None:
            title = name.get('english')
        elif name.get('romaji') is not None:
            title = name.get('romaji')
        elif name.get('native') is not None:
            title = name.get('native')

        cover = data.get('coverImage')
        color_hex = cover.get('color', '#5865F2')
        color_hex = color_hex if color_hex is not None else "#5865F2"
        color_dec = int(color_hex[1:], 16)
        color_dc = discord.Colour(color_dec)

        embed = discord.Embed(
            title=title,
            color=color_dc,
        )

        if data.get('season') is not None:
            embed.add_field(name="Season", value=f"{data.get('season')} {data.get('seasonYear')}", inline=True)
        if data.get('status') == 'FINISHED':
            if data.get('episodes') is not None and data.get('episodes') > 1:
                embed.add_field(name="Length", value=f"{data.get('duration')}min x {data.get('episodes')} episodes", inline=True)
            else:
                embed.add_field(name="Length", value=f"{data.get('duration')}min", inline=True)
        else:
            embed.add_field(name="Status", value=data.get('status').replace('_', ' ').capitalize(), inline=True)
        embed.add_field(name="Genres", value=f"{' '.join(data.get('genres'))}", inline=True)
        embed.add_field(name="Description", value=cleanhtml(data.get('description'))[:1023], inline=False)
        embed.add_field(name="", value=f"[AniList page]({data.get('siteUrl')})", inline=False)

        embed.set_image(url=cover.get('large'))
        await ctx.send(embed=embed)

    @commands.command(name='manga', help="Show manga details")
    async def manga(self, ctx, *args):
        media_name = ' '.join(args)
        data = get_media(media_name, "MANGA")

        name = data.get('title')
        title = ""
        if name.get('english') is not None:
            title = name.get('english')
        elif name.get('romaji') is not None:
            title = name.get('romaji')
        elif name.get('native') is not None:
            title = name.get('native')

        cover = data.get('coverImage')
        color_hex = cover.get('color', '#5865F2')
        color_hex = color_hex if color_hex is not None else "#5865F2"
        color_dec = int(color_hex[1:], 16)
        color_dc = discord.Colour(color_dec)

        embed = discord.Embed(
            title=title,
            color=color_dc,
        )

        start_timestamp = date_to_unix(data.get('startDate'))

        embed.add_field(name="Status", value=data.get('status').replace('_', ' ').capitalize(), inline=True)
        if start_timestamp != 0:
            embed.add_field(name="Start Date", value=f"<t:{start_timestamp}:d>", inline=True)
            if data.get('status') == 'FINISHED':
                end_timestamp = date_to_unix(data.get('endDate'))
                embed.add_field(name="End Date", value=f"<t:{end_timestamp}:d>", inline=True)
                embed.add_field(name="Length", value=f"{data.get('volumes')} volumes, {data.get('chapters')} chapters", inline=False)

        embed.add_field(name="Genres", value=f"{' '.join(data.get('genres'))}", inline=False)
        embed.add_field(name="Description", value=cleanhtml(data.get('description'))[:1023], inline=False)
        embed.add_field(name="", value=f"[AniList page]({data.get('siteUrl')})", inline=False)

        embed.set_image(url=cover.get('large'))
        await ctx.send(embed=embed)
