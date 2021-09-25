import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
import os
import asyncio

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        def getTime(time):
            if ("d" in time):
                popped = time.strip("d")
                final = 60 * 60 * int(popped) * 24
                return final
            elif ("h" in time):
                popped = time.strip("h")
                final = 60 * 60 * int(popped)
                return final
            elif ("m" in time):
                popped = time.strip("m")
                final = 60 * int(popped)
                return final
            else:
                raise ValueError

        def standardError(error):
            embed = discord.Embed(title = ":x: Error", description = "```{0}```".format(error), color = 0xff0000)
            return embed
        
        def defaultError(error):
            embed = discord.Embed(title = ":x:" + error, description = "\n", color = 0xff0000)
            return embed

        @bot.command(aliases = ["m"])
        @bot_has_permissions(manage_messages = True)
        async def mute(ctx, member: discord.Member, time = "10m", *, reason = "Not Specified"):
            if ctx.message.author.guild_permissions.mute_members:
                moderator = ctx.message.author
                server = ctx.guild

                muterole = discord.utils.get(member.guild.roles, name = "Muted")
                if not muterole:
                    muterole = await server.create_role(name = "Muted", permissions = discord.Permissions(send_messages = False, read_messages = True), color = 0x555353)
                    for channel in ctx.guild.channels:
                        locked = channel.overwrites_for(muterole)
                        locked.send_messages = False
                        await channel.set_permissions(muterole, overwrite = locked)

                if muterole in member.roles:
                    await ctx.send("This user is already muted.")
                    return
                elif moderator == member:
                    await ctx.send("You cannot mute yourself!")
                    return
                else:
                    try:
                        toSleep = getTime(time)

                        await member.add_roles(muterole)
                        await ctx.send("{0} has been muted for {1} for {2}.".format(member, time, reason))
                        try:
                            await member.send("You have been muted for {0} by {1} in {2} for {3}.".format(time, moderator, server, reason))
                        except discord.Forbidden:
                            await ctx.send("I can't DM this user.")
                        except discord.HTTPException:
                            await ctx.send("Unknown error - DM failed.")

                        await asyncio.sleep(toSleep)
                        try:
                            await member.remove_roles(muterole)
                            await member.send("You have been unmuted in {0}.".format(server))
                        except:
                            pass

                    except ValueError:
                        await ctx.send(embed = discord.Embed(title = ":x: Command Failed", description = time + "is not a valid length! Use ?help mute for a guideline.", color = 0xff0000))
                    except discord.Forbidden:
                        await ctx.send(embed = defaultError("I wasn't able to mute this user."))
                        return
            else:
                await ctx.send(embed = discord.Embed(title = ":x: You don't have permission to run this command!", description = "\n", color = 0xff0000))
                return



        #Check that mute works every time a channel is created
        @bot.event
        async def on_guild_channel_create(ctx):
            server = ctx.guild
            muterole = discord.utils.get(server.roles, name = "Muted")
            if not muterole:
                muterole = await server.create_role(name = "Muted", permissions = discord.Permissions(send_messages = False, read_messages = True))
            for channel in ctx.guild.channels:
                locked = channel.overwrites_for(muterole)
                locked.send_messages = False
                await channel.set_permissions(muterole, overwrite = locked)

        #remove the mute role from a member
        #Will only unmute if user has "muterole"
        @bot.command(aliases = ["um"])
        @bot_has_permissions(manage_messages = True)
        async def unmute(ctx, member: discord.Member, *, reason = "Not Specified"):
            if ctx.message.author.guild_permissions.mute_members:
                moderator = ctx.message.author
                server = ctx.guild
                try:
                    muterole = discord.utils.get(member.guild.roles, name = "Muted")
                    if muterole not in member.roles:
                        await ctx.send("This user is already unmuted.")
                        return
                    else:
                        await member.remove_roles(muterole)
                        await ctx.send("{0} has been unmuted for {1}.".format(member, reason))
                #todo: create a function that can auto create roles
                except AttributeError:
                    await ctx.send('Could not find a role named "Muted"')
                except discord.Forbidden:
                    await ctx.send(embed = defaultError("I wasn't able to unmute this user."))
                    return
                try:
                    await member.send("You have been unmuted by {0} in {1} for {2}.".format(moderator, server, reason))
                except discord.Forbidden:
                    await ctx.send("I can't DM this user.")
                except discord.HTTPException:
                    await ctx.send("Unknown error - DM failed.")
            else:
                await ctx.send(embed = discord.Embed(title = ":x: You don't have permission to run this command!", description = "\n", color = 0xff0000))
                return

        #kicks a member
        @bot.command(aliases = ["k"])
        @bot_has_permissions(ban_members = True)
        async def kick(ctx, member: discord.Member, *, reason = "Not Specified"):
            if ctx.message.author.guild_permissions.kick_members:
                moderator = ctx.message.author
                server = ctx.guild
                #sanity check
                if moderator == member:
                    await ctx.send("You cannot kick yourself!")
                    return
                try:
                    await member.kick(reason = reason)
                except discord.Forbidden:
                    await ctx.send(embed = defaultError("I wasn't able to kick this user."))
                    return
                try:
                    await member.send("You have been kicked from {0} by {1} for {2}.".format(server, moderator, reason))
                except discord.Forbidden:
                    await ctx.send("I can't DM this user. ")
                except discord.HTTPException:
                    await ctx.send("Unknown error - DM failed.")

                await ctx.send("{0} has been kicked for {1}.".format(member, reason))
            else:
                await ctx.send(embed = discord.Embed(title = ":x: You don't have permission to run this command!", description = "\n", color = 0xff0000))
                return

        #ban a member
        #todo: make temp bans
        #will probs make another command so I don't have to deal with conflicts
        @bot.command(aliases = ["b"])
        @bot_has_permissions(ban_members = True)
        async def ban(ctx, member: discord.Member, *, reason = "Not Specified"):
            if ctx.message.author.guild_permissions.ban_members:
                moderator = ctx.message.author
                server = ctx.guild
                #another sanity check... you would think this wouldn't be neccessary
                if moderator == member:
                    await ctx.send("You cannot ban yourself!")
                    return
                try:
                    await member.ban(reason = reason)
                except discord.Forbidden:
                    await ctx.send(embed = defaultError("I wasn't able to ban this user."))
                    return
                try:
                    await member.send("You have been banned from {0} by {1} for {2}.".format(server, moderator, reason))
                except discord.Forbidden:
                    await ctx.send("I can't DM this user.")
                except discord.HTTPException:
                    await ctx.send("Unknown error - DM failed.")

                await ctx.send("{0} has been banned for {1}.".format(member, reason))
            else:
                await ctx.send(embed = discord.Embed(title = ":x: You don't have permission to run this command!", description = "\n", color = 0xff0000))


        @bot.command(aliases = ["tb"])
        @bot_has_permissions(ban_members = True)
        @guild_only()
        async def tempban(ctx, member: discord.Member, time, *, reason = "Not specified"):
            if ctx.message.author.guild_permissions.ban_members:
                moderator = ctx.message.author
                server = ctx.guild
                if moderator == member:
                    await ctx.send("You cannot ban yourself!")
                    return
                try:
                    await member.ban(reason = reason)
                except discord.Forbidden:
                    await ctx.send(embed = defaultError("I wasn't able to tempban this user."))
                    return
                try:
                    await member.send("You have been tempbanned for {0} from {0} by {1} for {2}.".format(time, server, moderator, reason))
                except discord.Forbidden:
                    await ctx.send("I can't DM this user.")
                except discord.HTTPException:
                    await ctx.send("Unknown error - DM failed.")
                await ctx.send("{0} has been tempbanned {1} for {1}.".format(member, time, reason))

                toSleep = getTime(time)

                await asyncio.sleep(toSleep)
                memberID = await bot.fetch_user(member.id)
                await ctx.guild.unban(memberID)

            else:
                await ctx.send(embed = discord.Embed(title = ":x: You don't have permission to run this command!", description = "\n", color = 0xff0000))
                return

        #unban a Member
        #todo: bot unbans but returns an error
        @bot.command(aliases = ["ub"])
        @bot_has_permissions(ban_members = True)
        @guild_only()
        async def unban(ctx, id: int):
            if ctx.message.author.guild_permissions.ban_members:
                userid = await bot.fetch_user(id)
                await ctx.guild.unban(userid)
                await ctx.send("{0} has been unbanned by {1}.".format(userid, ctx.message.author))
            else:
                await ctx.send("You don't have permission to run this command!")

        #set a nickname of a member
        @bot.command(aliases = ["n"])
        @bot_has_permissions(manage_nicknames = True)
        async def nick(ctx, member: discord.Member, *, nickname = None):
            if ctx.message.author.guild_permissions.manage_nicknames:
                if nickname == None:
                    await member.edit(nick = None)
                    await ctx.send("{0}'s nickname has been reset.".format(member))
                    try:
                        locknick = discord.utils.get(member.guild.roles, name = "Nickname Banned")
                        await member.remove_roles(locknick)
                    except:
                        return

                elif len(nickname) > 32:
                    await ctx.send("Nicknames must be shorter than 32 characters!")
                    return
                else:
                    try:
                        await member.edit(nick = nickname)
                        await ctx.send("{0}'s name has been changed to {1} by {2}.".format(member, nickname, ctx.message.author))
                    except discord.HTTPException:
                        await ctx.send(embed = discord.Embed(title = ":x: Command Failed", description = "Check that the bot role is hoisted high enough and that your role is higher than the targeted user.", color = 0xff0000))
            else:
                await ctx.send(embed = discord.Embed(title = ":x: You don't have permission to run this command!", description = "\n", color = 0xff0000))

        #set a user's nickname as something for x amount of time
        #assigns a role banning them fron changing their name
        #won't work if the user has perms to manage other nicknames other than theirs
        @bot.command(aliases = ["sn"])
        @bot_has_permissions(manage_nicknames = True, manage_roles = True)
        async def setnick(ctx, member: discord.Member, time, *, nickname = None):
            if ctx.message.author.guild_permissions.manage_nicknames:
                locknick = discord.utils.get(member.guild.roles, name = "Nickname Banned")
                moderator = ctx.message.author
                server = ctx.guild
                if not locknick:
                    locknick = await server.create_role(name = "Nickname Banned", permissions = discord.Permissions(change_nickname = False, read_messages = True), color = 0x555353)
                    for channel in ctx.guild.channels:
                        locked = channel.overwrites_for(locknick)
                        locked.change_nickname = False
                        await channel.set_permissions(locknick, overwrite = locked)
                    await ctx.send("Configured role for lock.")

                if moderator == member:
                    await ctx.send("I don't think you want to do this...")
                    return
                
                elif nickname == None:
                    await member.remove_roles(locknick)
                    await ctx.send("{0}'s name has been unlocked.".format(member))
                    await member.edit(nick = None)
                    try:
                        await member.send("Your nickname in {0} is now unlocked.".format(server))
                    except:
                        print("fail")

                    return

                elif len(nickname) > 32:
                    await ctx.send("Nicknames must be shorter than 32 characters!")
                    return

                elif locknick in member.roles:
                    await ctx.send("This user is already locked.")
                    return

                try:
                    if ("h" in time):
                        popped = time.strip("h")
                        if int(popped) > 23:
                            await ctx.send("Use d to set days")
                            return
                        final = 60 * 60 * int(popped)
                        await member.add_roles(locknick)
                        await member.edit(nick = nickname)
                        await ctx.send("{0}'s named has been locked for {1} hours.".format(member, popped))
                        await asyncio.sleep(final)
                        await member.remove_roles(locknick)
                        try:
                            await member.send("Your nickname in {0} is now unlocked.".format(server))
                        except:
                            print("fail")
                    elif ("d" in time):
                        popped = time.strip("d")
                        if int(popped) > 90:
                            await ctx.send("You can only setnicks for 90 days, at most.")
                            return
                        final = 60 * 60 * int(popped) * 24
                        await member.add_roles(locknick)
                        await member.edit(nick = nickname)
                        await ctx.send("{0}'s named has been locked for {1} days.".format(member, popped))
                        await asyncio.sleep(final)
                        try:
                            await member.remove_roles(locknick)
                            await member.send("Your nickname in {0} is now unlocked.".format(server))
                        except:
                            print("fail")
                except ValueError:
                    await ctx.send(embed = discord.Embed(title = ":x: Command Failed", description = time + "is not a valid length! Use ?help mute for a guideline.", color = 0xff0000))
                    return
            else:
                await ctx.send(embed = discord.Embed(title = ":x: You don't have permission to run this command!", description = "\n", color = 0xff0000))
                return

        #detailed error return- it's a wonky command
        @setnick.error
        async def fail(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send(embed = discord.Embed(title = ":x: Missing an Argument", description = "Missing a required field. Format is: `setnick [user] [time] (nickname) - leave the nickname blank to terminate the timer and reset nickname.`", color = 0xff0000))

            else:
                await ctx.send(embed = standardError(error))


        @unban.error
        async def failed(ctx, error):
            if isinstance(error, discord.ext.commands.BadArgument):
                await ctx.send(embed = discord.Embed(title = ":x: Bad Argument Error", description = "This command does not accept mentions. Please use an ID.", color = 0xff0000))
            elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
                await ctx.send(embed = discord.Embed(title = ":x: Execute Error", description = "This user is not banned from this server.", color = 0xff0000))
            else:
                await ctx.send(embed = standardError(error))

        #return an error if something wonky happened
        @kick.error
        @ban.error
        @tempban.error
        @mute.error
        @unmute.error
        @nick.error
        async def fail(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send(embed = discord.Embed(title = ":x: You did not include a user!", description = "\n", color = 0xff0000))
            elif isinstance(error, discord.ext.commands.BadArgument):
                await ctx.send(embed = discord.Embed(title = ":x: Could not find the targeted user.", description = "\n", color = 0xff0000))
            else:
                await ctx.send(embed = standardError(error))

def setup(bot):
    bot.add_cog(ModCommands(bot))
