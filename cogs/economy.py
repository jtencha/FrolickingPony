import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
import os
import asyncio
import random
from bot import *

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        @commands.cooldown(1, 3600, commands.BucketType.member)
        async def work(ctx):
            #check if user is banned from the bot
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            #check if economy is enabled in the server
            elif isAllowed("economy", ctx.message.guild.id) == False:
                await ctx.send(embed = discord.Embed(title = ":x: Command Disabled", description = "A server administrator has disabled the economy features of this bot.", color = 0xff0000))
                return
            #both pass? execute command
            else:
                id = str(ctx.message.author.id)
                paycheck = random.choice([x for x in range(100, 300)])
                count = 0
                with open("money.txt", "r") as f:
                    fl = f.readlines()
                    f.close()

                for line in fl:
                    #sanity check
                    if (line.find(";") == -1 or line.find(":") == -1 or line.find("\n") == -1):
                        channel = bot.get_channel(942166599710965831)
                        await channel.send("<@687081333876719740> bot flagged {0}. Review `money.txt`".format(line))
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

                if (count == 0):
                    set = str(ctx.message.guild.id) + ";" + id + ":" + str(paycheck) + "\n"
                    with open("money.txt", "a") as f:
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
                            if (line.find(";") == -1 or line.find(":") == -1):
                                channel = bot.get_channel(942166599710965831)
                                await channel.send("<@687081333876719740> bot flagged {0}. Review `money.txt`".format(line))
                            else:
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
        @bot_has_permissions(manage_webhooks = True)
        async def balance(ctx):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            elif isAllowed("economy", ctx.message.guild.id) == False:
                await ctx.send(embed = discord.Embed(title = ":x: Command Disabled", description = "A server administrator has disabled the economy features of this bot.", color = 0xff0000))
                return
            else:
                id = str(ctx.message.author.id)
                amount = 0
                with open("money.txt", "r") as f:
                    fl = f.readlines()
                    f.close()

                for line in fl:
                    if (line.find(";") == -1 or line.find(":") == -1 or line.find("\n") == -1):
                        channel = bot.get_channel(942166599710965831)
                        await channel.send("<@687081333876719740> bot flagged {0}. Review `money.txt`".format(line))
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
                                return

                await ctx.send(embed = discord.Embed(title = "{0}'s Balance in {1}".format(ctx.message.author, ctx.guild), description = "0 :coin:", color = 0xff6633))

        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        async def addmoney(ctx, member: discord.Member, uAmount):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            elif str(member.id) == str(873968526153625690):
                await ctx.send("Beep Boop! Sorry, but you can't give me money.")
                return
            elif isAllowed("economy", ctx.message.guild.id) == False:
                await ctx.send(embed = discord.Embed(title = ":x: Command Disabled", description = "A server administrator has disabled the economy features of this bot.", color = 0xff0000))
                return
            else:
                if ctx.message.author.guild_permissions.administrator:
                    id = str(member.id)
                    try:
                        uAmount = int(uAmount)
                    except:
                        await ctx.send(embed = discord.Embed(title = ":x: You must provide an integer amount to add", color = 0xff0000))
                        return

                    if int(uAmount) > 10000:
                        await ctx.send(":x: You can only add up to 10,000 :coin: at a time!")
                        return
                    elif int(uAmount) < 1:
                        await ctx.send(":x: Invalid amount provided.")
                        return

                    with open("money.txt", "r") as f:
                        fl = f.readlines()
                        f.close()
                    with open("money.txt", "w") as f:
                        count = 0
                        for line in fl:
                            if (line.find(";") == -1 or line.find(":") == -1 or line.find("\n") == -1):
                                channel = bot.get_channel(942166599710965831)
                                await channel.send("<@687081333876719740> bot flagged {0}. Review `money.txt`".format(line))
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
                                else:
                                    f.write(line)

                        if (count == 0):
                            await ctx.send(":x: Due to sourecode quirks, this user has to run the ?work command in order to be registered in the system to receive money.")
                else:
                    await ctx.send(":x: You don't have permission to run this command! Required: Administrator")

        @bot.command(aliases = ["subtractmoney"])
        @bot_has_permissions(manage_webhooks = True)
        async def removemoney(ctx, member: discord.Member, uAmount):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            elif str(member.id) == str(873968526153625690):
                await ctx.send("Beep Boop! Sorry, but you cannot take money from me.")
                return
            elif isAllowed("economy", ctx.message.guild.id) == False:
                await ctx.send(embed = discord.Embed(title = ":x: Command Disabled", description = "A server administrator has disabled the economy features of this bot.", color = 0xff0000))
                return

            if ctx.message.author.guild_permissions.administrator:
                id = str(member.id)
                try:
                    uAmount = int(uAmount)
                except:
                    await ctx.send(embed = discord.Embed(title = ":x: You must provide an integer amount to remove", color = 0xff0000))
                    return

                if int(uAmount) > 10000:
                      await ctx.send(":x: You can only remove up to 10,000 :coin: at a time!")
                      return
                elif int(uAmount) < 1:
                    await ctx.send(":x: Invalid amount provided.")
                    return

                with open("money.txt", "r") as f:
                    fl = f.readlines()
                    f.close()
                with open("money.txt", "w") as f:
                    count = 0
                    for line in fl:
                        if (line.find(";") == -1 or line.find(":") == -1 or line.find("\n") == -1):
                            channel = bot.get_channel(942166599710965831)
                            await channel.send("<@687081333876719740> bot flagged {0}. Review `money.txt`".format(line))
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
                                f.write(line)

                    if (count == 0):
                        await ctx.send(":x: You cannot take money from a user that has none.")
            else:
                await ctx.send(":x: You don't have permission to run this command! Required: Administrator")
#format: serverid;USERID:money\n
        @bot.command(aliases = ["lb"])
        @bot_has_permissions(manage_webhooks = True)
        async def leaderboard(ctx):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            elif isAllowed("economy", ctx.message.guild.id) == False:
                await ctx.send(embed = discord.Embed(title = ":x: Command Disabled", description = "A server administrator has disabled the economy features of this bot.", color = 0xff0000))
                return


            people = []
            amounts = []

            with open("money.txt", "r") as f:
                fl = f.readlines()
                f.close()

            count = 1
            for line in fl:
                if (line.find(";") == -1 or line.find(":") == -1 or line.find("\n") == -1):
                    channel = bot.get_channel(942166599710965831)
                    await channel.send("<@687081333876719740> bot flagged {0}. Review `money.txt`".format(line))
                else:
                    ind = line.index(":")
                    serverind = line.index(";")
                    sind = line.index("\n")
                    userid = line[serverind + 1:ind]
                    serverid = line[:serverind]
                    amount = line[ind + 1:sind]

                    if (int(serverid) == ctx.message.guild.id):
                        people.append(line)
                        print("Added " + line)
                        amounts.append(amount)
                        print("Added " + amount)


            amounts.sort(reverse = True)
            amounts.sort(reverse = True, key = len)

            print(amounts)
            i = 1

            ordered = []
            for y in amounts:
                for x in people:
                    if (line.find(";") == -1 or line.find(":") == -1 or line.find("\n") == -1):
                        channel = bot.get_channel(942166599710965831)
                        await channel.send("<@687081333876719740> bot flagged {0}. Review `money.txt`".format(line))
                    else:
                        ind = x.index(":")
                        serverind = x.index(";")
                        sind = x.index("\n")
                        userid = x[serverind + 1:ind]
                        amount = x[ind + 1:sind]
                        print(amount + " vs. " + y)
                        if (amount == y):
                            add_field = ("**" + str(i) + ".** <@" + str(userid) + ">: " + amount + " :coin: \n")
                            ordered.append(add_field)
                            i+= 1

            order = ""
            for line in ordered:
                order += line

            await ctx.send(embed = discord.Embed(title = "{0}'s Leaderboard".format(ctx.guild), description = order, color = 0xff6633))

        @bot.command(aliases = ["d"])
        @bot_has_permissions(manage_webhooks = True)
        @commands.cooldown(1, 3600, commands.BucketType.member)
        async def dice(ctx, uamount: int):
            id = str(ctx.message.author.id)

            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            elif isAllowed("economy", ctx.message.guild.id) == False:
                await ctx.send(embed = discord.Embed(title = ":x: Command Disabled", description = "A server administrator has disabled the economy features of this bot.", color = 0xff0000))
                return
            else:
                if int(uamount) > 300:
                    await ctx.send(":x: You cannot bet more than 300 :coin: at a time!")
                    dice.reset_cooldown(ctx)
                elif int(uamount) < 100:
                    await ctx.send(":x: You must bet at least 100 :coin:!")
                    dice.reset_cooldown(ctx)
                else:
                    with open("money.txt", "r") as f:
                        fl = f.readlines()
                        f.close()

                    for line in fl:
                        if (line.find(";") == -1 or line.find(":") == -1 or line.find("\n") == -1):
                            channel = bot.get_channel(942166599710965831)
                            await channel.send("<@687081333876719740> bot flagged {0}. Review `money.txt`".format(line))
                        else:
                            ind = line.index(":")
                            sind = line.index("\n")
                            serverind = line.index(";")
                            userid = line[serverind + 1:ind]
                            if (id == userid):
                                serverid = line[:serverind]
                                if (int(serverid) == ctx.message.guild.id):
                                    amount = line[ind + 1:sind]
                                    if amount > uamount:
                                        await ctx.send(":x: You do not have enough money to do this!")
                                        dice.reset_cooldown(ctx)
                                        return

                    list = [x for x in range(1, 7)]
                    p_one = random.choice(list)
                    p_two = random.choice(list)
                    p = int(p_one + p_two)

                    comp_one = random.choice(list)
                    comp_two = random.choice(list)

                    c = int(comp_one + comp_two)

                    await ctx.send(":game_die: You roll a **{0}** and a **{1}** for a total of **{2}** ...".format(p_one, p_two, (p_one + p_two)))
                    await asyncio.sleep(2)
                    await ctx.send(":game_die: I roll a **{0}** and a **{1}** for a total of **{2}**...".format(comp_one, comp_two, (comp_one + comp_two)))
                    await asyncio.sleep(2)

                    if p > c:
                        await ctx.send("Your score is higher than mine! You won **{0}** :coin:!".format(uamount))
                        set = int(uamount)
                    elif p < c:
                        await ctx.send("My score is higher than yours :smirk:. You lost **{0}** :coin:".format(uamount))
                        set = -1 * int(uamount)
                    else:
                        await ctx.send("Fine... we'll call it a draw.")
                        set = 0

                    with open("money.txt", "r") as f:
                        fla = f.readlines()
                        f.close()

                    with open("money.txt", "w") as f:
                        for line in fla:
                            if (line.find(";") == -1 or line.find(":") == -1 or line.find("\n") == -1):
                                channel = bot.get_channel(942166599710965831)
                                await channel.send("<@687081333876719740> bot flagged {0}. Review `money.txt`".format(line))
                            else:
                                ind = line.index(":")
                                sind = line.index("\n")
                                serverind = line.index(";")
                                userid = line[serverind + 1:ind]
                                if (int(id) == int(userid)):
                                    serverid = line[:serverind]
                                    amount = line[ind + 1:sind]
                                    if (int(serverid) == ctx.message.guild.id):
                                        newAmount = int(amount) + int(set)
                                        snew = str(newAmount)
                                        f.write(str(serverid) + ";" + userid + ":" + snew + "\n")
                                    else:
                                        f.write(line)
                                else:
                                    f.write(line)

        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        @commands.cooldown(1, 86400, commands.BucketType.member)
        async def daily(ctx):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            elif isAllowed("economy", ctx.message.guild.id) == False:
                await ctx.send(embed = discord.Embed(title = ":x: Command Disabled", description = "A server administrator has disabled the economy features of this bot.", color = 0xff0000))
                return
            else:
                sum = random.choice([x for x in range(50, 200)])
                count = 0
                with open("money.txt", "r") as f:
                    fl = f.readlines()
                    f.close()

                with open("money.txt", "w") as f:
                    for line in fl:
                        if (line.find(";") == -1 or line.find(":") == -1 or line.find("\n") == -1):
                            channel = bot.get_channel(942166599710965831)
                            await channel.send("<@687081333876719740> bot flagged {0}. Review `money.txt`".format(line))
                        else:
                            ind = line.index(":")
                            sind = line.index("\n")
                            serverind = line.index(";")
                            userid = line[serverind + 1:ind]
                            if (str(ctx.message.author.id) == userid):
                                serverid = line[:serverind]
                                if (int(serverid) == ctx.message.guild.id):
                                    amount = line[ind + 1:sind]
                                    new = int(amount) + sum
                                    snew = str(new)
                                    f.write(str(serverid) + ";" + userid + ":" + snew + "\n")
                                    await ctx.send("You claimed your daily pay of {0} :coin:.".format(sum))
                                    count = 1
                                else:
                                  f.write(line)
                            else:
                              f.write(line)

                    if count == 0:
                        f.write(str(ctx.message.guild.id) + ";" + str(ctx.message.author.id) + ":" + str(sum) + "\n")
                        await ctx.send("You claimed your daily pay of {0} :coin:.".format(sum))

        @work.error
        @addmoney.error
        @balance.error
        @removemoney.error
        @leaderboard.error
        @dice.error
        @daily.error
        #@number.error
        async def fail(ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                time = int(round(error.retry_after, 0) / 60)
                await ctx.send(embed = discord.Embed(title = ":x: You are still on cooldown for this command!", description = "You can use this command in {0} minutes".format(time), color = 0xff0000))
            elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Missing member and/or amount", color = 0xff0000))
            elif isinstance(error, BotMissingPermissions):
                await ctx.send(f"I don't have permission to run this command! Required: {' '.join(error.missing_perms)}")
            else:
                await ctx.send(embed = discord.Embed(title = ":x: Fatal Error", description = "An internal error prevented the bot from finishing your request. Please try again later.\n\nReference: `{0}`".format(error), color = 0xff0000))
                #print(error)
                channel = bot.get_channel(942166599710965831)
                await channel.send("<@687081333876719740> error thrown in {0}".format(ctx.message.guild))

def setup(bot):
    bot.add_cog(Economy(bot))
