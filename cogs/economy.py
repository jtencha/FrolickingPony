import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
import os
import asyncio
import random
from bot import *
'''
----------------------
TO-DO:
-Add bot money on server addition
'''

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command()
        @commands.cooldown(1, 3600, commands.BucketType.member)
        async def work(ctx):
            id = str(ctx.message.author.id)
            paycheck = random.choice([x for x in range(100, 300)])
            count = 0
            with open("money.txt", "r") as f:
                fl = f.readlines()
                for line in fl:
                    if (line.find(";") == -1 or line.find(":") == -1):
                        continue
                    else:
                        ind = line.index(":")
                        sind = line.index("\n")
                        serverind = line.index(";")
                        userid = line[serverind + 1:ind]
                        if (id == userid):
                            serverid = line[:serverind]
                            if (int(serverid) == ctx.message.guild.id):
                                previous = line[ind + 1:sind]
                                count += 1
                        else:
                            print("Line 35")
                f.close()


            if (count == 0):
                with open("money.txt", "a") as f:
                    set = str(ctx.message.guild.id) + ";" + id + ":" + str(paycheck) + "\n"
                    f.write(set)
                    f.close()
                await ctx.send("You gained {0} :coin: from working.".format(paycheck))
                return
            else:
                tota = int(previous) + int(paycheck)
                with open("money.txt", "r") as f:
                    fl = f.readlines()
                with open("money.txt", "w") as f:
                    for line in fl:
                        ind = line.index(":")
                        serverind = line.index(";")
                        userid = line[serverind + 1:ind]
                        if (id == userid):
                            serverid = line[:serverind]
                            if (int(serverid) == ctx.message.guild.id):
                                total = str(tota)
                                set = str(serverid) + ";" + id + ":" + total + "\n"
                                f.write(set)
                            else:
                                f.write(line)
                        else:
                            f.write(line)
                    f.close()
                await ctx.send("You gained {0} :coin: from working.".format(paycheck))
                return



        @bot.command(aliases = ["bal"])
        async def balance(ctx):
            id = str(ctx.message.author.id)
            amount = 0
            with open("money.txt", "r") as f:
                fl = f.readlines()
                for line in fl:
                    if (line == "" or line == "\n"):
                        continue
                    else:
                        ind = line.index(":") #start of balance
                        sind = line.index("\n") #end of line
                        serverind = line.index(";") #start of user id
                        userid = line[serverind + 1:ind] #inbetween start of userID and start of balance
                        if (id == userid):
                            serverid = line[:serverind]
                            if (int(serverid) == ctx.message.guild.id):
                                amount = line[ind + 1:sind]

                await ctx.send(embed = discord.Embed(title = "{0}'s Balance in {1}".format(ctx.message.author, ctx.guild), description = "{0} :coin:".format(amount), color = 0xff6633))
                f.close()

        @bot.command()
        async def addmoney(ctx, member: discord.Member, uAmount):
            if ctx.message.author.guild_permissions.administrator:
                id = str(member.id)
                try:
                    uAmount = int(uAmount)
                except:
                    await ctx.send(embed = discord.Embed(title = ":x: You must provide an integer amount to add", color = 0xff0000))
                    return

                with open("money.txt", "r") as f:
                    fl = f.readlines()
                    f.close()
                with open("money.txt", "w") as f:
                    count = 0
                    for line in fl:
                        if (line == "" or line == "\n"):
                            continue
                        else:
                            ind = line.index(":")
                            sind = line.index("\n")
                            serverind = line.index(";")
                            userid = line[serverind + 1:ind]
                            if (id == userid):
                                serverid = line[:serverind]
                                if (int(serverid) == ctx.message.guild.id):
                                    amount = line[ind + 1:sind]
                                    newAmount = int(amount) + int(uAmount)
                                    snew = str(newAmount)
                                    set = str(serverid) + ";" + id + ":" + snew + "\n"
                                    f.write(set)
                                    await ctx.send("Successfully added {0} :coin: to {1}'s bank".format(uAmount, member))
                                    count += 1
                            else:
                                f.write(line)

                    if (count == 0):
                        await ctx.send(":x: This user has to run the ?work command in order to be registered in the system. ")
            else:
                await ctx.send(":x: You don't have permission to run this command! Required: Administrator")

        @bot.command(aliases = ["subtractmoney"])
        async def removemoney(ctx, member: discord.Member, uAmount):
            if ctx.message.author.guild_permissions.administrator:
                id = str(member.id)
                try:
                    uAmount = int(uAmount)
                except:
                    await ctx.send(embed = discord.Embed(title = ":x: You must provide an integer amount to remove", color = 0xff0000))
                    return

                with open("money.txt", "r") as f:
                    fl = f.readlines()
                    f.close()
                with open("money.txt", "w") as f:
                    count = 0
                    for line in fl:
                        print("LINE: " + '"' + line + '"')
                        if (line == "" or line == "\n"):
                            continue
                        else:
                            ind = line.index(":")
                            sind = line.index("\n")
                            serverind = line.index(";")
                            userid = line[serverind + 1:ind]
                            if (id == userid):
                                serverid = line[:serverind]
                                if (int(serverid) == ctx.message.guild.id):
                                    amount = line[ind + 1:sind]
                                    newAmount = int(amount) - int(uAmount)
                                    snew = str(newAmount)
                                    set = str(serverid) + ";" + id + ":" + snew + "\n"
                                    f.write(set)
                                    await ctx.send("Successfully removed {0} :coin: from {1}'s bank".format(uAmount, member))
                                    count += 1
                            else:
                                f.write(line + "\n")

                    if (count == 0):
                        await ctx.send(":x: You cannot take money from a user that has none.")
            else:
                await ctx.send(":x: You don't have permission to run this command! Required: Administrator")
#format: serverid;USERID:money\n
        @bot.command(aliases = ["lb"])
        async def leaderboard(ctx):
            embed = discord.Embed(title = "{0}'s Leaderboard".format(ctx.guild), description = "\n", color = 0xff6633)
            with open("money.txt", "r") as f:
                fl = f.readlines()
                count = 1
                for line in fl:
                    if (line == "" or line == "\n"):
                        continue
                    else:
                        ind = line.index(":")
                        serverind = line.index(";")
                        sind = line.index("\n")
                        userid = line[serverind + 1:ind]
                        serverid = line[:serverind]
                        amount = line[ind + 1:sind]
                        if (int(serverid) == ctx.message.guild.id):
                            embed.add_field(name = str(count) + ". ", value = "<@" + str(userid) + ">: " + amount + " :coin:", inline = False)
                            count += 1
                f.close()

            await ctx.send(embed = embed)


        @work.error
        @addmoney.error
        @balance.error
        @removemoney.error
        @leaderboard.error
        async def fail(ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                time = int(round(error.retry_after, 0) / 60)
                await ctx.send(embed = discord.Embed(title = ":x: You are still on cooldown for this command!", description = "You can use this command in {0} minutes".format(time), color = 0xff0000))
            elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Missing member and/or amount", color = 0xff0000))
            else:
                await ctx.send(embed = discord.Embed(title = ":x: Error", description = "{0}".format(error), color = 0xff0000))


def setup(bot):
    bot.add_cog(Economy(bot))
