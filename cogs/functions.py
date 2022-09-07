import discord
from discord.ext import commands, tasks
from loguru import logger
import asyncio
import base64
import aiohttp
import json
from calendar import month_name
from datetime import datetime, timedelta
import cohere


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


        await self.pushdata()


    # Automatically push new data to Github
    async def pushdata(self):
        filenames = ["data/birthdates.json"]
        for filename in filenames:
            try:
                token = database["github_oath"]
                repo = "Ryxn7/Birthday-Bot"
                branch = "main"
                url = "https://api.github.com/repos/" + repo + "/contents/" + filename

                base64content = base64.b64encode(open(filename, "rb").read())

                async with aiohttp.ClientSession() as session:
                    async with session.get(url + '?ref=' + branch, headers={"Authorization": "token " + token}) as data:
                        data = await data.json()
                sha = data['sha']

                if base64content.decode('utf-8') + "\n" != data['content']:
                    message = json.dumps(
                        {"message": "Automatic data update.",
                        "branch": branch,
                        "content": base64content.decode("utf-8"),
                        "sha": sha}
                    )
                    async with aiohttp.ClientSession() as session:
                        async with session.put(url, data=message, headers={"Content-Type": "application/json",
                                                                           "Authorization": "token " + token}) as resp:
                            print(resp)
                else:
                    print("Nothing to update.")
            except Exception as e:
                logger.exception(e)

 
    @commands.command(aliases=['a'])
    async def add(self, ctx, *desc):
        
        input = list(desc)
        guildID = str(ctx.guild.id)
        try:
            # Format is month/day/userID
            if len(input) != 3:
                return await ctx.reply("Please make sure you are entering the information correctly!")
            else:
                username = input[2]
                month = str(input[0])
                day = str(input[1])
                # Create new key if new guild id found
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


        await self.pushdata()


    # Automatically push new data to Github
    async def pushdata(self):
        filenames = ["data/birthdates.json"]
        for filename in filenames:
            try:
                token = database["github_oath"]
                repo = "Ryxn7/Birthday-Bot"
                branch = "main"
                url = "https://api.github.com/repos/" + repo + "/contents/" + filename

                base64content = base64.b64encode(open(filename, "rb").read())

                async with aiohttp.ClientSession() as session:
                    async with session.get(url + '?ref=' + branch, headers={"Authorization": "token " + token}) as data:
                        data = await data.json()
                sha = data['sha']

                if base64content.decode('utf-8') + "\n" != data['content']:
                    message = json.dumps(
                        {"message": "Automatic data update.",
                        "branch": branch,
                        "content": base64content.decode("utf-8"),
                        "sha": sha}
                    )
                    async with aiohttp.ClientSession() as session:
                        async with session.put(url, data=message, headers={"Content-Type": "application/json",
                                                                           "Authorization": "token " + token}) as resp:
                            print(resp)
                else:
                    print("Nothing to update.")
            except Exception as e:
                logger.exception(e)


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
                
                if time.month == bDay.month:
                    if time.day == bDay.day:
                        await ctx.send(f"Today is {username}'s birthday!")
                else:
                    bDay = datetime(datetime.now().year + 1, int(birthdates[guildID][0][username][0]), int(birthdates[guildID][0][username][1]), 0, 0, 0, 0)
                    diff = bDay-time
                    embed = discord.Embed(title = "**Birthday Countdown**   :cake:", color=0xB9BFFF)
                    embed.add_field(
                    name = f"{username}'s birthday is in: ",
                    value = f"{diff.days} days\n{int(diff.seconds/3600)} hours\n{int(diff.seconds%3600/60)} minutes\n{(diff.seconds%3600)%60} seconds\n{diff.microseconds} microseconds\n",
                    inline = (True)
                    )
                    embed.set_footer(text = "By Ryxn and Pancreas")
                    await ctx.send(embed=embed)
            
        except Exception as e:
            logger.exception(e)
    

    @commands.command()
    async def bdaycd(self, ctx):
        time = datetime.now() - timedelta(hours=4)
        guildID = str(ctx.guild.id)
        for user in birthdates[guildID][0]:
            if time.month == int(birthdates[guildID][0][user][0]) and time.day == int(birthdates[guildID][0][user][1]):
                await ctx.send(f"< {user} > HAPPY BIRTHDAY!")
                await ctx.send("https://c.tenor.com/8GOADtb93zIAAAAM/cat.gif")
                
                with open('cogs/pattern.txt') as f:
                    pattern = f.read()
                p = f"{pattern}\n\nName: < {user} >\nOutput:"
                
                # Sentence generation
                co = cohere.Client('XH6WEkN6940HTNO4hl1517Hpl1pX7gW8hpS3RisW')
                response = co.generate(
                model='xlarge',
                prompt = p,
                max_tokens=100,
                temperature=0.2,
                stop_sequences=['--'],
                k=0,
                p=0)
                await ctx.send(response.generations[0].text)


    @tasks.loop(minutes=1440) #1 day = 1440 minutes
    async def run(self):
        await self.bdaycountdown()

    async def bdaycountdown(self, ctx):
        time = datetime.now()-timedelta(hours=4)
        guildID = str(ctx.guild.id)
        for user in birthdates[guildID][0]:
            if time.month == int(birthdates[guildID][0][user][0]) and time.day == int(birthdates[guildID][0][user][1]):
                await ctx.send(f"{user} HAPPY BIRTHDAY!")
                await ctx.send("https://i.pinimg.com/originals/f8/4b/e4/f84be4356974f6f4c93c1edfdc4e7740.gif")
                
                with open('cogs/pattern.txt') as f:
                    pattern = f.read()
                p = f"{pattern}\n\nName: < {user} >\nOutput:"
                
                # Sentence generation
                co = cohere.Client('XH6WEkN6940HTNO4hl1517Hpl1pX7gW8hpS3RisW')
                response = co.generate(
                model='xlarge',
                prompt = p,
                max_tokens=100,
                temperature=0.2,
                stop_sequences=['--'],
                k=0,
                p=0)
                await ctx.send(response.generations[0].text)
                

def setup(client):
    client.add_cog(functions(client))
