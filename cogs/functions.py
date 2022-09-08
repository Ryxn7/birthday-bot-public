import discord
from discord.ext import commands, tasks
from loguru import logger
import json
from datetime import datetime, timedelta
import cohere
from utils.utils import Utils


with open("data/database.json") as d:
    database = json.load(d)

with open("data/birthdates.json") as b:
    birthdates = json.load(b)

class functions(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guildID = str(guild.id)
        birthdates[guildID] = [0]
        birthdates[guildID][0] = {}

        with open('data/birthdates.json', 'w') as z:
            json.dump(birthdates,z,indent=4)

        await Utils.pushdata()


    @commands.command(aliases=['a'])
    async def add(self, ctx, *desc):
        
        input = list(desc)
        guildID = str(ctx.guild.id)
        try:
            # Format is month/day/userID
            if len(input) != 3:
                return await ctx.reply("Please enter (month) (day) (@user)!")
            else:
                username = input[2]
                month = str(input[0])
                day = str(input[1])
                # Create new dictionary for new userID
                if username not in birthdates[guildID][0]:
                    birthdates[guildID][0][username] = []
                birthdates[guildID][0][username].append(month)
                birthdates[guildID][0][username].append(day)
                await ctx.send(username + "'s birthday was added to the Bot")
        except Exception as e:
            logger.exception(e)
            return await ctx.send("```You entered the information incorrectly \:( Please try the command again.```")
            
        with open('data/birthdates.json', 'w') as z:
            json.dump(birthdates,z,indent=4)

        await Utils.pushdata()


    @commands.command(name='?')
    async def viewbday(self, ctx, *username):
        name = list(username)
        guildID = str(ctx.guild.id)
        try:
            if len(name) != 1 or name[0] == "":
                errormsg = "Please enter an @user"
                await ctx.reply(errormsg)
            else:
                user = name[0]
                month = birthdates[guildID][0][user][0]
                day = birthdates[guildID][0][user][1]

                m, d = Utils.dateFormatter(self, month, day)

                embed = discord.Embed(title = "**Birthday**", color=0xf01e2c)
                embed.add_field(
                    name = ":partying_face:",
                    value = f"{user}'s birthday is on {m}/{d}!",
                    inline = False
                )
                await ctx.send(embed=embed)
        except Exception as e:
            logger.exception(e)
            await ctx.send(f"{user}'s birthday was not found on the database.")


    @commands.command(aliases=['c'])
    async def countdown(self, ctx, *desc):

        input = list(desc)
        guildID = str(ctx.guild.id)
        try:
            if len(input) != 1:
                    return await ctx.reply("Please make sure you are entering the information correctly!")
            else:
                username = input[0]
                time = datetime.now()-timedelta(hours=4)
                bDay = datetime(datetime.now().year, int(birthdates[guildID][0][username][0]), int(birthdates[guildID][0][username][1]), 0, 0, 0, 0)
                diff = bDay-time
                if time.month < bDay.month:
                    embed = discord.Embed(title = "**Birthday Countdown**", color=0xB9BFFF)
                    embed.add_field(
                        name = ":cake:",
                        value = f"***{username}'s birthday is in:*** \n{diff.days} days\n{int(diff.seconds/3600)} hours\n{int(diff.seconds%3600/60)} minutes\n{(diff.seconds%3600)%60} seconds\n{diff.microseconds} microseconds\n",
                        inline = True
                    )
                    embed.set_footer(text = "By Ryxn and Pancreas")
                    await ctx.send(embed=embed)
                elif time.month == bDay.month:
                    if time.day == bDay.day:
                        await ctx.send(f"Today is {username}'s birthday!")
                    elif time.day < bDay.day:
                        embed = discord.Embed(title = "**Birthday Countdown**", color=0xB9BFFF)
                        embed.add_field(
                            name = ":cake:",
                            value = f"***{username}'s birthday is in:*** \n{diff.days} days\n{int(diff.seconds/3600)} hours\n{int(diff.seconds%3600/60)} minutes\n{(diff.seconds%3600)%60} seconds\n{diff.microseconds} microseconds\n",
                            inline = True
                        )
                        embed.set_footer(text = "By Ryxn and Pancreas")
                        await ctx.send(embed=embed)
                    else:
                        bDay = datetime(datetime.now().year + 1, int(birthdates[guildID][0][username][0]), int(birthdates[guildID][0][username][1]), 0, 0, 0, 0)
                        diff = bDay-time
                        embed = discord.Embed(title = "**Birthday Countdown**", color=0xB9BFFF)
                        embed.add_field(
                            name = ":cake:",
                            value = f"***{username}'s birthday is in:*** \n{diff.days} days\n{int(diff.seconds/3600)} hours\n{int(diff.seconds%3600/60)} minutes\n{(diff.seconds%3600)%60} seconds\n{diff.microseconds} microseconds\n",
                            inline = True
                        )
                        embed.set_footer(text = "By Ryxn and Pancreas")
                        await ctx.send(embed=embed)
                else:
                    bDay = datetime(datetime.now().year + 1, int(birthdates[guildID][0][username][0]), int(birthdates[guildID][0][username][1]), 0, 0, 0, 0)
                    diff = bDay-time
                    embed = discord.Embed(title = "**Birthday Countdown**", color=0xB9BFFF)
                    embed.add_field(
                        name = ":cake:",
                        value = f"***{username}'s birthday is in:*** \n{diff.days} days\n{int(diff.seconds/3600)} hours\n{int(diff.seconds%3600/60)} minutes\n{(diff.seconds%3600)%60} seconds\n{diff.microseconds} microseconds\n",
                        inline = True
                    )
                    embed.set_footer(text = "By Ryxn and Pancreas")
                    await ctx.send(embed=embed)
        except Exception as e:
            logger.exception(e)


    @commands.command()
    async def shout(self, ctx):
        time = datetime.now() - timedelta(hours=4)
        guildID = str(ctx.guild.id)
        for user in birthdates[guildID][0]:
            if time.month == int(birthdates[guildID][0][user][0]) and time.day == int(birthdates[guildID][0][user][1]):
                await ctx.send(f"Happy Birthday {user}!!!")
                await ctx.send("https://c.tenor.com/8GOADtb93zIAAAAM/cat.gif")
                
                with open('cogs/pattern.txt') as f:
                    pattern = f.read()
                p = f"{pattern}\n\nName: < {user} >\nOutput:"
                
                # Sentence generation
                co = cohere.Client(database["cohere_token"])
                response = co.generate(
                model='xlarge',
                prompt = p,
                max_tokens=100,
                temperature=0.2,
                stop_sequences=['\n'],
                k=0,
                p=0)
                await ctx.send(response.generations[0].text)


    @tasks.loop(minutes=1440) #1 day = 1440 minutes
    async def run(self):
        await self.bdayshout()

    async def bdayshout(self, ctx):
        time = datetime.now()-timedelta(hours=4)
        guildID = str(ctx.guild.id)
        for user in birthdates[guildID][0]:
            if time.month == int(birthdates[guildID][0][user][0]) and time.day == int(birthdates[guildID][0][user][1]):
                await ctx.send(f"{user} HAPPY BIRTHDAY!")
                await ctx.send("https://i.pinimg.com/originals/f8/4b/e4/f84be4356974f6f4c93c1edfdc4e7740.gif")
                
                with open('cogs/pattern.txt') as f:
                    pattern = f.read()
                p = f"{pattern}\n\nName: {user} \nOutput:"
                
                # Sentence generation
                co = cohere.Client('XH6WEkN6940HTNO4hl1517Hpl1pX7gW8hpS3RisW')
                response = co.generate(
                model='xlarge',
                prompt = p,
                max_tokens=100,
                temperature=0.2,
                stop_sequences=['\n'],
                k=0,
                p=0)
                await ctx.send(response.generations[0].text)
                

def setup(client):
    client.add_cog(functions(client))
