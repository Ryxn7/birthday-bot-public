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
        activity = discord.Game(name = f"/help")
        await self.client.change_presence(status=discord.Status.online, activity=activity)
        logger.info("Birthday Bot is ready.")


    @discord.slash_command(name="help", description="Here's the help prompt!")
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
            value = "`/add (month) (day) @user` - Command to add a birthday to the database."
                    "\n> Example usage: `/add 06 02 @user`"

                    "\n\n`/countdown @user`" \
                    "\n> Returns the birthdays that have been added to this month."

                    "\n\n`/?when @user`" \
                    "\n> Returns user's birthday." \

                    "\n\n`/invite`" \
                    "\n> Returns Birthday Bot's Invite Link.",
            inline = False
        )

        embed.set_footer(text="By Ryxn and Pancreas <3")
        await ctx.respond(embed=embed)


    @discord.slash_command(name="invite", description="Bot's invite link!")
    async def invite(self, ctx):
        invite_link = database["invite_link"]
        embed = discord.Embed(title="Birthday Bot | Invite Link | :confetti_ball:", color=0xFF69B4)
        embed.add_field(
            name = "Add Birthday Bot to your own server down below!",
            value = f"[Birthday-Bot]({invite_link})!",
            inline = False
        )
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(admin(client))
