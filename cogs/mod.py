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

        @kick.error
        @ban.error
        @mute.error
        @unmute.error
        @unban.error
        async def fail(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send("You did not include a user!")
            else:
                await ctx.send("`{0}`".format(error))

def setup(bot):
    bot.add_cog(ModCommands(bot))
