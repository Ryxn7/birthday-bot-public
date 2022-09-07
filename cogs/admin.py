import discord
from discord.ext import commands, tasks
from loguru import logger
import json


with open("data/database.json") as d:
    database = json.load(d)


class admin(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        activity = discord.Game(name = f"bd.help")
        await self.client.change_presence(status=discord.Status.online, activity=activity)
        logger.info("Birthday Bot is ready.")
    
    @commands.command(aliases=["h"])
    async def help(self, ctx):

        user = ctx.author
        embed = discord.Embed(
            title = f"Birthday Bot | Help | {user}",
            color = 0xEFBBCD
        )
    
        embed.add_field(
            name = "How to use Birthday Bot",
            value = "Birthday Bot is the bot you need to finally help you keep track of birthdays",
            inline = False
        )

        embed.add_field(
            name = "Commands List",
            value = "`bd.add (month) (day) <@userID>` - Command to add a birthday to the database" \
                    "\n> Aliases: `bd.a (month)`" \
                    "\n> Example usages: `bd.add 06 02 <@123456789012345678>`"

                    "\n\n`bd.countdown <@userID>`" \
                    "\n> Returns the birthdays that have been added to this month" \
                    "\n> Aliases: `bd.c <@userID>`"

                    "\n\n`bd.invite`" \
                    "\n> Returns Birthday Bot's Invite Link" \
                    "\n> Aliases: `bd.i`",
            inline = False
        )

        embed.set_footer(text="By Ryxn and Pancreas <3")
        await ctx.send(embed=embed)
    
    @commands.command(aliases = ["i"])
    async def invite(self, ctx):
        invite_link = database["invite_link"]
        await ctx.reply(f"Add Birthday Bot to your own server using this link!" \
                  f"\n> {invite_link}")
    

def setup(client):
    client.add_cog(admin(client))
