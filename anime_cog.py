from discord.ext import commands
from anime_ping import find_watchers
import json
from collections import defaultdict

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
