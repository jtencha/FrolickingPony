import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
from secret import token
import os
import asyncio
import random

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command()
        @bot_has_permissions(manage_messages = True)
        async def mute(ctx, member: discord.Member, time = None, *, reason = "Not Specified"):
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
                        #TODO - get rid of this spaghetti crap
                        if (time == None):
                            print("No time provided.")
                            await member.add_roles(muterole)
                            await ctx.send("{0} has been muted for {1}.".format(member, reason))
                            try:
                                await member.send("You have been muted by {0} in {1} for {2}.".format(moderator, server, reason))
                            except discord.Forbidden:
                                await ctx.send("I can't DM this user.")
                            except discord.HTTPException:
                                await ctx.send("Unknown error - DM failed.")
                        elif ("h" in time):
                            popped = time.strip("h")
                            final = 60 * 60 * int(popped)
                            await member.add_roles(muterole)
                            await ctx.send("{0} has been muted for {1} hours for {2}.".format(member, popped, reason))
                            try:
                                await member.send("You have been muted for {0} hour(s) by {1} in {2} for {3}.".format(popped, moderator, server, reason))
                            except discord.Forbidden:
                                await ctx.send("I can't DM this user.")
                            except discord.HTTPException:
                                await ctx.send("Unknown error - DM failed.")
                            await asyncio.sleep(final)
                            await member.remove_roles(muterole)
                            await member.send("You have been unmuted in {0}.".format(server))
                        elif ("m" in time):
                            popped = time.strip("m")
                            final = 60 * int(popped)
                            await member.add_roles(muterole)
                            await ctx.send("{0} has been muted for {1} minutes for {2}.".format(member, popped, reason))
                            try:
                                await member.send("You have been muted for {0} minute(s) by {1} in {2} for {3}.".format(popped, moderator, server, reason))
                            except discord.Forbidden:
                                await ctx.send("I can't DM this user.")
                            except discord.HTTPException:
                                await ctx.send("Unknown error - DM failed.")
                            await asyncio.sleep(final)
                            await member.remove_roles(muterole)
                            await member.send("You have been unmuted in {0}.".format(server))
                        else:
                            await ctx.send((time) + " is not a valid length!")
                            return
                    except ValueError:
                        await ctx.send("An error occured. Please check to make sure you provided a valid length.")
                        return
                    except discord.Forbidden:
                        await ctx.send("I was unable to mute this user.")
                        return
            else:
                await ctx.send("You don't have permission to run this command!")
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

        #function unMute
        #Will only unmute if user has "muterole"
        #It will still return an error if the mute role isn't present.
        @bot.command()
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
                except AttributeError:
                    await ctx.send('Please configure a role named "Muted" for the bot to use.')
                except discord.Forbidden:
                    await ctx.send("I was unable to unmute this user.")
                    return
                try:
                    await member.send("You have been unmuted by {0} in {1} for {2}.".format(moderator, server, reason))
                except discord.Forbidden:
                    await ctx.send("I can't DM this user.")
                except discord.HTTPException:
                    await ctx.send("Unknown error - DM failed.")
            else:
                await ctx.send("You don't have permission to run this command!")
                return

        #Function kickMembers
        #Kicks a member and DMs them.
        #Returns if the targeted user is too powerful or the bot lacks perms.
        @bot.command()
        @bot_has_permissions(ban_members = True)
        async def kick(ctx, member: discord.Member, *, reason = "Not Specified"):
            if ctx.message.author.guild_permissions.kick_members:
                moderator = ctx.message.author
                server = ctx.guild
                #Will still kick and return a custom error if DM fails.
                if moderator == member:
                    await ctx.send("You cannot kick yourself!")
                    return
                try:
                    await member.kick(reason = reason)
                except discord.Forbidden:
                    await ctx.send("I was unable to kick this user.")
                    return
                try:
                    await member.send("You have been kicked from {0} by {1} for {2}.".format(server, moderator, reason))
                except discord.Forbidden:
                    await ctx.send("I can't DM this user. ")
                except discord.HTTPException:
                    await ctx.send("Unknown error - DM failed.")

                await ctx.send("{0} has been kicked for {1}.".format(member, reason))
            else:
                await ctx.send("You don't have permission to run this command!")
                return


        #function banMembers
        #Bans a member and DMs them
        #Returns if the targeted user is too powerful or the bot lacks perms.
        @bot.command()
        @bot_has_permissions(ban_members = True)
        async def ban(ctx, member: discord.Member, *, reason = "Not Specified"):
            if ctx.message.author.guild_permissions.ban_members:
                moderator = ctx.message.author
                server = ctx.guild
                #Will still kick and return a custom error if DM fails.
                if moderator == member:
                    await ctx.send("You cannot ban yourself!")
                    return
                try:
                    await member.ban(reason = reason)
                except discord.Forbidden:
                    await ctx.send("I was unable to ban this user.")
                    return
                try:
                    await member.send("You have been banned from {0} by {1} for {2}.".format(server, moderator, reason))
                except discord.Forbidden:
                    await ctx.send("I can't DM this user.")
                except discord.HTTPException:
                    await ctx.send("Unknown error - DM failed.")

                await ctx.send("{0} has been banned for {1}.".format(member, reason))
            else:
                await ctx.send("You don't have permission to run this command!")


        @bot.command()
        @bot_has_permissions(ban_members = True)
        @guild_only()
        async def unban(ctx, id: int):
            if ctx.message.author.guild_permissions.ban_members:
                userid = await bot.fetch_user(id)
                await ctx.guild.unban(userid)
                await ctx.send("{0} has been unbanned by {0}.".format(userid, ctx.message.author))
            else:
                await ctx.send("You don't have permission to run this command!")

        @bot.command()
        @bot_has_permissions(manage_nicknames = True)
        async def nick(ctx, member: discord.Member, *, nickname = None):
            if ctx.message.author.guild_permissions.manage_nicknames:
                if nickname == None:
                    await member.edit(nick = None)
                    await ctx.send("{0}'s nickname has been reset.".format(member))
                else:
                    try:
                        await member.edit(nick = nickname)
                        await ctx.send("{0}'s name has been changed to {1} by {2}.".format(member, nickname, ctx.message.author))
                    except discord.HTTPException:
                        await ctx.send("Nicknames must be shorter than 32 characters!")
            else:
                await ctx.send("You don't have permission to run this command!")

        @bot.command()
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
                    await ctx.send("Role has configured. Please re-run the most recent comamnd.")

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
                    await ctx.send("An error occured. Please check to make sure you provided a valid length.")
                    return
            else:
                await ctx.send("You don't have permission to run this command!")
                return

        @setnick.error
        async def fail(ctx, error):
          if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send("Missing a required field. Format is: `setnick [user] [time] (nickname) - leave the nickname blank to unlock once more`")
          else:
            await ctx.send("`{0}`".format(error))

        @kick.error
        @ban.error
        @mute.error
        @unmute.error
        @unban.error
        @nick.error
        async def fail(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send("You did not include a user!")
            else:
                await ctx.send("`{0}`".format(error))

def setup(bot):
    bot.add_cog(ModCommands(bot))
