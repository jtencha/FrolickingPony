import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
import os
import asyncio
import random
from typing import Optional
from bot import isBanned

class Functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(aliases = ["av"])
        @bot_has_permissions(manage_webhooks = True)
        async def avatar(ctx, member: Optional[Member]):
            print(type(member))
            #stupid async await
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return

            if member == None:
                user = ctx.message.author
            elif member != None:
                user = member
                if type(user) != discord.Member:
                    await ctx.send(embed = discord.Embed(title = ":x: Could not find the targeted user.", description = "\n", color = 0xff0000))
                    return
            else:
                user = ctx.guild.get_member_named(member)
                if user != discord.Member:
                    await ctx.send(embed = discord.Embed(title = ":x: Could not find the targeted user.", description = "\n", color = 0xff0000))
                    return
            embed = discord.Embed(title = "{0}'s avatar".format(user), description = "\n", color = 0xff6633)
            embed.set_image(url = user.avatar_url)
            await ctx.send(embed = embed)

        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        async def stats(ctx):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            server = ctx.guild
            embed = discord.Embed(title = "{0} Server Stats".format(ctx.guild), description = "\n", color = 0xff6633)
            embed.add_field(name = "Server ID:", value = server.id, inline = True)
            embed.add_field(name = "Members:", value = server.member_count, inline = True)
            embed.add_field(name = "Owner", value = server.owner, inline = True)
            embed.add_field(name = "Channels:", value = len(server.channels), inline = True)
            embed.add_field(name = "Roles:", value = len(server.roles), inline = True)
            embed.add_field(name = "Created on:", value = server.created_at.strftime("%A, %B %d %Y"), inline = True)
            try:
                embed.add_field(name = "Bot Role:", value = server.self_role.mention, inline = True)
            except:
                embed.add_field(name = "Bot Role:", value = "None", inline = True)
            embed.add_field(name = "Banned members", value = len(await server.bans()), inline = True)
            embed.set_thumbnail(url = server.icon_url)
            await ctx.send(embed = embed)

        @stats.error
        async def fail(ctx, error):
            if isinstance(error, BotMissingPermissions):
                await ctx.send(f"I don't have permission to run this command! Required: {' '.join(error.missing_perms)}")
            else:
                embed = discord.Embed(title = ":x: Error", description = "```{0}```".format(error), color = 0xff0000)
                await ctx.send(embed = embed)

        #Bot response time
        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        async def ping(ctx):
            embed = discord.Embed(title = ":ping_pong: Pong!", description = "{0}ms".format(round(bot.latency * 1000)), color = 0xff6633)
            await ctx.send(embed = embed)

        @bot.command(aliases = ["i"])
        @bot_has_permissions(manage_webhooks = True)
        async def invite(ctx):
            embed = discord.Embed(title = "Invite FrolickingPony", url = "https://discord.com/api/oauth2/authorize?client_id=873968526153625690&permissions=1644972474359&scope=bot", description = "Invite the bot with the link above!", color = 0xff6633)
            await ctx.send(embed = embed)

        @bot.command(aliases = ["p"])
        @bot_has_permissions(manage_messages = True, manage_webhooks = True)
        async def poll(ctx, option_one, option_two, option_three = None, option_four = None):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return

            embed = discord.Embed(title = "Poll Created by {0}".format(ctx.message.author), description = "\n", color = 0xff6633)
            embed.add_field(name = "1️⃣ Option One:", value = "{0}".format(option_one), inline = False)
            embed.add_field(name = "2️⃣ Option Two:", value = "{0}".format(option_two), inline = False)
            if option_three != None:
                embed.add_field(name = "3️⃣ Option Three:", value = "{0}".format(option_three), inline = False)
                if option_four != None:
                    embed.add_field(name = "4️⃣ Option Four:", value = "{0}".format(option_four), inline = False)

            #Deletes the command typed by the user.
            await ctx.message.delete()
            poll = await ctx.send(embed = embed)
            await poll.add_reaction("1️⃣")
            await poll.add_reaction("2️⃣")
            if option_three != None:
                await poll.add_reaction("3️⃣")
                if option_four != None:
                    await poll.add_reaction("4️⃣")

        #Checking for garbage
        @poll.error
        async def denied(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send(embed = discord.Embed(title = ":x: Error", description = "You must include at least two poll options!", color = 0xff0000))
            elif isinstance(error, BotMissingPermissions):
                await ctx.send(f"I don't have permission to run this command! Required: {' '.join(error.missing_perms)}")
            else:
                embed = discord.Embed(title = ":x: Error", description = "```{0}```".format(error), color = 0xff0000)
                await ctx.send(embed = embed)

        #info on user
        @bot.command(aliases = ["a"])
        @bot_has_permissions(manage_webhooks = True)
        async def about(ctx, member: Optional[Member]):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return

            if member == None:
                user = ctx.message.author
            elif member != None:
                user = member
                if type(user) != discord.Member:
                    await ctx.send(embed = discord.Embed(title = ":x: Could not find the targeted user.", description = "\n", color = 0xff0000))
                    return
            else:
                user = ctx.guild.get_member_named(member)
                if user != discord.Member:
                    await ctx.send(embed = discord.Embed(title = ":x: Could not find the targeted user.", description = "\n", color = 0xff0000))
                    return

            embed = discord.Embed(title = "{0}".format(user), description = "User information:", color = 0xff6633)
            embed.add_field(name = "Name:", value = user.name, inline = True)
            embed.add_field(name = "User ID:", value = user.id, inline = True)
            embed.add_field(name = "Highest Role:", value = user.top_role.mention)
            embed.add_field(name = "Created Account:", value = user.created_at.strftime("%A, %B %d %Y"))
            embed.add_field(name = "Joined Server:", value = user.joined_at.strftime("%A, %B, %d %Y"))
            perms = []

            if user.guild_permissions.administrator:
                perms.append("Administrator")
            if user.guild_permissions.manage_channels:
                perms.append("Manage Channels")
            if user.guild_permissions.kick_members:
                perms.append("Kick Members")
            if user.guild_permissions.ban_members:
                perms.append("Ban Members")
            if user.guild_permissions.manage_messages:
                perms.append("Manage Messages")

            string = ""
            x = 1;

            if len(perms) == 0:
                string = None
            else:
                for i in perms:
                    if x > len(perms):
                        string += i
                    else:
                        string += i + ", "
                    x += 1

            embed.add_field(name = "Key Permissions: ", value = string, inline = False)
            embed.set_thumbnail(url = user.avatar_url)
            await ctx.send(embed = embed)


        @about.error
        @avatar.error
        async def incorrect(ctx, error):
            if isinstance(error, BotMissingPermissions):
                await ctx.send(f"I don't have permission to run this command! Required: {' '.join(error.missing_perms)}")
            else:
                embed = discord.Embed(title = ":x: Error", description = "{0}".format(error), color = 0xff0000)
                await ctx.send(embed = embed)
                print(error)

        @bot.command(aliases = ["ei"])
        @bot_has_permissions(manage_webhooks = True)
        async def eightball(ctx, question):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            choices = ["No", "I guess", "Absolutely not.", "Ha, you wish", "Yes! Yes! and Yes!", "Unclear. Check back later.", "Without a doubt.", "If you say so", "Sussy", "Kinda sus not gonna lie"]
            await ctx.send(random.choice(choices))

        @eightball.error
        async def bad(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send("You need to ask me something...")
            elif isinstance(error, BotMissingPermissions):
                await ctx.send(f"I don't have permission to run this command! Required: {' '.join(error.missing_perms)}")
            else:
                embed = discord.Embed(title = ":x: Error", description = "```{0}```".format(error), color = 0xff0000)
                await ctx.send(embed = embed)

        @bot.command(aliases = ["e"])
        @bot_has_permissions(manage_webhooks = True)
        async def embed(ctx, title, *, message = "\n"):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            embed = discord.Embed(title = title, description = message, color = 0xff6633)
            embed.set_author(name = "{0}".format(ctx.message.author), icon_url = ctx.message.author.avatar_url)
            await ctx.message.delete()
            await ctx.send(embed = embed)

        @bot.command()
        async def sourcecode(ctx):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            embed = discord.Embed(title = "Source code for RoboticPony:", description = "https://github.com/jtencha/FrolickingPony", color = 0xff6633)
            await ctx.send(embed = embed)

        @bot.command(aliases = ["co"])
        @bot_has_permissions(manage_webhooks = True)
        @commands.cooldown(1, 3600, commands.BucketType.user)
        async def contact(ctx, *, message):
            try:
                if isBanned(str(ctx.message.author.id), 1) != False:
                    await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                    return
                embed = discord.Embed(title = "Contact Developer", description = "Abuse will result in a ban from this command/use of this bot.", color = 0xff0000)
                embed.add_field(name = 'Are you sure that you want to send this message to the developer? Respond with "CONFIRM" (case sensitive).', value = "Your message: {0}".format(message))
                msg = await ctx.send(embed = embed)
                def check(msg):
                    if msg.content != "CONFIRM":
                        raise TypeError
                    else:
                        return msg.content == "CONFIRM"

                await bot.wait_for("message", check = check)
                embed = discord.Embed(title = "Message by {0} ({1}) from {2}:".format(ctx.message.author, ctx.message.author.id, ctx.guild), description = "{0}".format(message), color = 0xff6633)
                channel = bot.get_channel(942166599710965831)
                await channel.send(embed = embed)
                embed = discord.Embed(title = "Message Sent", description = ":white_check_mark: Your message has been sent to the developer.", color = 0x009933)
                await ctx.send(embed = embed)

            except TypeError:
                embed = discord.Embed(title = "Message Terminated", description = ":x: Your message has successfully been terminated.", color = 0xff0000)
                await ctx.send(embed = embed)

        @bot.command(aliases = ["bl"])
        @bot_has_permissions(manage_webhooks = True)
        async def blacklist(ctx, member: discord.Member):
            if str(ctx.message.author.id) == str("687081333876719740"):
                with open("botbanned.txt", "a+") as f:
                    f.write(str(member.id) + "\n")

                embed = discord.Embed(title = "User blacklisted", description = ":white_check_mark: {0} has been banned from using this bot.".format(member.id), color = 0x009933)
                await ctx.send(embed = embed)
                channel = bot.get_channel(942166599710965831)
                await channel.send(embed = embed)
            else:
                await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Only the bot owner can use this command!", color = 0xff0000))
                return

        @bot.command(aliases = ["ubl"])
        @bot_has_permissions(manage_webhooks = True)
        async def unblacklist(ctx, member: discord.Member):
            if str(ctx.message.author.id) == str("687081333876719740"):
                count = 0
                with open("botbanned.txt", "r") as f:
                    fl = f.readlines()
                with open("botbanned.txt", "w") as f:
                    for l in fl:
                        if l.strip("\n") != str(member.id):
                            f.write(l)
                        else:
                            count += 1

                if count == 0:
                    await ctx.send(embed = discord.Embed(title = ":x: Error", description = "This user is not blacklisted.", color = 0xff0000))
                    return
                else:
                    embed = discord.Embed(title = "User unblacklisted", description = ":white_check_mark: {0} is unblacklisted.".format(member.id), color = 0x009933)
                    await ctx.send(embed = embed)
                    channel = bot.get_channel(942166599710965831)
                    await channel.send(embed = embed)
            else:
                await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Only the bot owner can use this command!", color = 0xff0000))
                return

        @bot.command(aliases = ["lbl"])
        @bot_has_permissions(manage_webhooks = True)
        async def listblacklist(ctx):
            if str(ctx.message.author.id) == str("687081333876719740"):
                with open("botbanned.txt", "r+") as f:
                    for line in f:
                        await ctx.send(line)
            else:
                await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Only the bot owner can use this command!", color = 0xff0000))
                return

        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        async def support(ctx):
            await ctx.send("Join this server for official release notes and development programs.")
            await ctx.send("https://discord.gg/ffHUnEy7gM")

        @bot.command(aliases = ["set"])
        @bot_has_permissions(manage_webhooks = True)
        async def settings(ctx, setting = None, new = None):
            if ctx.message.author.guild_permissions.administrator:
                if setting == None and new == None:
                    with open("settings.txt", "r") as f:
                        lines = f.readlines()

                    economyStatus = None
                    modStatus = None
                    aStatus = None
                    dStatus = None

                    for line in lines:
                        #serverid:setting;t/f
                        if (line.find(";") == -1 or line.find(":") == -1):
                            continue
                        else:
                            serverid = line[:line.index(":")]
                            usetting = line[line.index(":") + 1:line.index(";")]
                            status = line[line.index(";") + 1:]
                            if (int(serverid) == ctx.message.guild.id):
                                if usetting.lower() == "economy":
                                    if status == "t\n":
                                        economyStatus = "Enabled"
                                    else:
                                        economyStatus = "Disabled"
                                elif usetting.lower() == "moderation":
                                    if status == "t\n":
                                        modStatus = "Enabled"
                                    else:
                                        modStatus = "Disabled"
                                elif usetting.lower() == "gibamdib":
                                    if status == "t\n":
                                        aStatus = "Enabled"
                                    else:
                                        aStatus = "Disabled"
                                elif usetting.lower() == "developer":
                                    if status == "t\n":
                                        dStatus = "Enabled"
                                    else:
                                        dStatus = "Disabled"


                    embed = discord.Embed(title = "{0} Settings Menu".format(ctx.guild), description = "Change specific settings using `?settings [setting] enable/disable`", color = 0xff6633)
                    embed.add_field(name = "Economy", value = economyStatus, inline = False)
                    embed.add_field(name = "Moderation", value = modStatus, inline = False)
                    embed.add_field(name = 'gibamdib', value = aStatus, inline = False)
                    embed.add_field(name = "Early Access Mode (Developer)", value = dStatus, inline = False)
                    await ctx.send(embed = embed)
                    return
                elif setting != None and new == None:
                    await ctx.send(embed = discord.Embed(title = ":x: Error", description = "You did not provide a status update for {0}".format(setting), color = 0xff0000))
                    return
                else:
                    if (setting == "economy" or setting == "moderation" or setting == "gibamdib" or setting == "developer"):
                        if new == "enable":
                            new = "t"
                        elif new == "disable":
                            new = "f"
                        else:
                            await ctx.send(title = ":x: Error", description = "Invalid status. Only use enable or disable.", color = 0xff0000)
                            return

                        with open("settings.txt", "r") as f:
                            lines = f.readlines()
                        with open("settings.txt", "w") as f:
                            for line in lines:
                                serverid = line[:line.index(":")]
                                usetting = line[line.index(":") + 1:line.index(";")]
                                status = line[line.index(";") + 1:]
                                if (int(serverid) == ctx.message.guild.id):
                                    if usetting.lower() == setting:
                                        f.write(str(ctx.message.guild.id) + ":" + setting + ";" + new + "\n")
                                        await ctx.send(":white_check_mark: Updated {0} status".format(setting))
                                        if usetting.lower() == "developer" and new.lower() == "t":
                                            await ctx.send(embed = discord.Embed(title = ":x: WARNING", description = "Enabling the developer version of the bot grants early access to unreleased features, but since these features haven't been released they are very unstable, and may cause unwanted effects.", color = 0xff0000))
                                    else:
                                        f.write(line)
                                else:
                                    f.write(line)
                    else:
                        await ctx.send(embed = discord.Embed(title = ":x: Error", description = "That setting does not exist!", color = 0xff0000))
                        return
            else:
                await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Only server administrators can configure settings with the bot.", color = 0xff0000))


        @embed.error
        async def fail(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                embed = discord.Embed(title = ":x: Error", description = "You need to give me at least a title to embed!", color = 0xff0000)
                await ctx.send(embed = embed)
            elif isinstance(error, BotMissingPermissions):
                await ctx.send(f"I don't have permission to run this command! Required: {' '.join(error.missing_perms)}")
            else:
                await ctx.send("`{0}`".format(error))

        @contact.error
        async def failed(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                embed = discord.Embed(title = ":x: Error", description = "You did not provide a message!", color = 0xff0000)
                await ctx.send(embed = embed)
            elif isinstance(error, commands.CommandOnCooldown):
                time = int(round(error.retry_after, 0) / 60)
                await ctx.send(embed = discord.Embed(title = ":x: You are still on cooldown for this command!", description = "You can use this command in {0} minutes".format(time), color = 0xff0000))
            elif isinstance(error, BotMissingPermissions):
                await ctx.send(f"I don't have permission to run this command! Required: {' '.join(error.missing_perms)}")
            else:
                embed = discord.Embed(title = ":x: Error", description = "```{0}```".format(error), color = 0xff0000)
                await ctx.send(embed = embed)

        @blacklist.error
        @unblacklist.error
        @settings.error
        async def blackError(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                embed = discord.Embed(title = ":x: Error", description = "You did not give me a user to blacklist!", color = 0xff0000)
                await ctx.send(embed = embed)
            elif isinstance(error, BotMissingPermissions):
                await ctx.send(f"I don't have permission to run this command! Required: {' '.join(error.missing_perms)}")
            else:
                embed = discord.Embed(title = ":x: Error", description = "```{0}```".format(error), color = 0xff0000)
                await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Functions(bot))
