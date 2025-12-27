import discord
from discord.ext import commands
from anime_ping import find_watchers, fetch_user
import json
from collections import defaultdict
from deranged import deranged_meter

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
    async def manga(self, ctx, *args):
        name = ' '.join(args)
        watchers, title = find_watchers(self.servers[ctx.guild.id].keys(), name, 'MANGA')
        await ctx.send(f"Pinging {title} readers:")
        for user in watchers:
            user_id = self.servers[ctx.guild.id][user]
            await ctx.send(f"<@{user_id}>")

    @commands.command(name='fetch', help='Show user stats')
    async def fetch(self, ctx, username=None):
        if username is None:
            try:
                server_dict = self.servers[ctx.guild.id]
                username = (list(server_dict.keys())[list(server_dict.values()).index(16)])
            except:
                ctx.send("No username specified and you do not have added AniList username")
                return

        data = fetch_user(username)

        embed = discord.Embed(
            title=username,
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
        embed.add_field(name="Favourite genres", value="", inline=False)
        embed.add_field(name=anigenres[0].get('genre'), value=anigenres[0].get('meanScore'), inline=True)
        embed.add_field(name=anigenres[1].get('genre'), value=anigenres[1].get('meanScore'), inline=True)
        embed.add_field(name=anigenres[2].get('genre'), value=anigenres[2].get('meanScore'), inline=True)

        mangastats = data.get('statistics').get('manga')
        embed.add_field(name="Manga stats", value="", inline=False)
        embed.add_field(name="Total Manga", value=mangastats.get('count'), inline=True)
        embed.add_field(name="Chapters Read", value=mangastats.get('chaptersRead'), inline=True)
        embed.add_field(name="Mean Score", value=mangastats.get('meanScore'), inline=True)

        mangagenres = mangastats.get('genres')
        embed.add_field(name="Favourite genres", value="", inline=False)
        embed.add_field(name=mangagenres[0].get('genre'), value=mangagenres[0].get('meanScore'), inline=True)
        embed.add_field(name=mangagenres[1].get('genre'), value=mangagenres[1].get('meanScore'), inline=True)
        embed.add_field(name=mangagenres[2].get('genre'), value=mangagenres[2].get('meanScore'), inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='deranged', help="Show user's derangement")
    async def deranged_meter(self, ctx, username=None):
        if username is None:
            try:
                server_dict = self.servers[ctx.guild.id]
                username = (list(server_dict.keys())[list(server_dict.values()).index(16)])
            except:
                ctx.send("No username specified and you do not have added AniList username")
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

        await ctx.send(embed=embed)

