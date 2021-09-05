import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
from secret import token
import os
import asyncio
import random

#Prefix can be changed here
prefix = ";"

intents = discord.Intents.default()
intents = discord.Intents(messages = True, guilds = True)


client = commands.Bot(command_prefix = prefix, intents = intents)
client.remove_command("help")

#Prints output to terminal if all is well
@client.event
async def on_ready():
    print("We're clear for takeoff!")
    await client.change_presence(activity = discord.Game("Going Insane | ;help"))

#Rough draft, I'll make this better soon
#@client.event
#async def on_command_error(ctx, error, message):
    #if isinstance(error, discord.ext.commands.CommandNotFound):
        #await ctx.send("Command at {0} is not recognized.".format(message))

@client.command()
async def guetzali(ctx):
    await ctx.send(random.choice(["Guetzali Guetzali",
    "https://media.discordapp.net/attachments/842447676414361620/843713059033710632/60a1f6f95aa22378467759.gif",
    "https://media.discordapp.net/attachments/404803931227553802/860570669322469377/quetzali.gif",
    "https://media.discordapp.net/attachments/863137688470814741/863936864054149140/makesweet-kxksih.gif",
    "https://media.discordapp.net/attachments/404803931227553802/859942873864994816/697995591921172532-8.gif"
    ]))
#Ping
@client.command()
async def ping(ctx):
    embed = discord.Embed(title = ":ping_pong: Pong!", description = f"{round(client.latency * 1000)}ms", color = 0x009933)
    await ctx.send(embed = embed)

#Invite command
@client.command()
async def invite(ctx):
    embed = discord.Embed(title = "Invite RoboticPony", url = "https://discord.com/oauth2/authorize?client_id=834799912507277312&permissions=243165293686&scope=bot", description = "Invite the bot with the link above!", color = 0x009933)
    await ctx.send(embed = embed)

#Help list
#Use numbers to navigate the menus
#Defaults to ;commands 1 if no number is provided.
@client.command()
async def help(ctx, type = "1"):
    if type == "1":
        embed = discord.Embed(title = "Avalible Commands:", description = "Commands marked with an * require permissions.\n\n", color = 0x009933)
        embed.add_field(name = ";about [user]", value = "Get info about a user", inline = False)
        embed.add_field(name = ";guetzali", value = "Guetzali moment", inline = False)
        embed.add_field(name = ";help", value = "General overview of commands", inline = False)
        embed.add_field(name = ";invite", value = "Invite RoboticPony", inline = False)
        embed.add_field(name = ";ping", value = "Bot response time.", inline = False)
        embed.add_field(name = ";poll [option] [option] [option] [option]", value = "Create a poll", inline = False)
        embed.add_field(name = ";mute [user] [time] [reason]*", value = "Mute a user for a set time", inline = False)
        embed.add_field(name = ";unmute [user] [reason]*", value = "Unmute a user", inline = False)
        embed.add_field(name = ";kick [user] [reason]*", value = "Kicks a member.", inline = False)
        embed.add_field(name = ";ban [user] [reason]*", value = "Bans a member.", inline = False)
        embed.add_field(name = "Secret Command*", value = "Puts the bot to sleep.", inline = False)
        embed.add_field(name = "\n\nList 1 of 1", value = "\n\nAdministrator permissions are recommended for moderation.")
        await ctx.send(embed = embed)
    else:
        await ctx.send("Invalid command.")

@client.command()
@bot_has_permissions(manage_messages = True)
async def poll(ctx, option_one, option_two, option_three = None, option_four = None):
    embed = discord.Embed(title = "Poll Created by {0}".format(ctx.message.author), description = "\n", color = 0x009933)
    embed.add_field(name = "1️⃣ Option One:", value = "{0}".format(option_one), inline = False)
    embed.add_field(name = "2️⃣ Option Two:", value = "{0}".format(option_two), inline = False)
    if option_three != None:
        embed.add_field(name = "3️⃣ Option Three:", value = "{0}".format(option_three), inline = False)
        if option_four != None:
            embed.add_field(name = "4️⃣ Option Four:", value = "{0}".format(option_four), inline = False)

    #Inefficient, but it gets the job done. I'll make it prettier and less repetitive later.
    #Deletes the ;poll command typed by the user.
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
        await ctx.send("You must include at least two choices!")
    elif isinstance(error, BotMissingPermissions):
        await ctx.send("Fatal error, command terminated.")
        await ctx.send(error)
    else:
        await ctx.send(error)

@client.command()
async def about(ctx, member: discord.Member):
    embed = discord.Embed(title = "{0}".format(member), description = "User information:", color = 0x009933)
    embed.add_field(name = "Name:", value = member.name, inline = True)
    embed.add_field(name = "User ID:", value = member.id, inline = True)
    embed.add_field(name = "Highest Role:", value = member.top_role)
    embed.add_field(name = "Created Account:", value = member.created_at)
    embed.add_field(name = "Joined Server:", value = member.joined_at)
    embed.set_thumbnail(url = member.avatar_url)
    await ctx.send(embed = embed)

@about.error
async def incorrect(ctx, error):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        embed = discord.Embed(title = "About RoboticPony", description = "Version: 1.4.6.1\nDeveloped by: FamiliarNameMissing and discord.py", color = 0x009933)
        await ctx.send(embed = embed)
    else:
        await ctx.send(error)

#Function mute
#Mutes a member forever and DMs them.
@client.command()
@bot_has_permissions(manage_messages = True)
async def mute(ctx, member: discord.Member, time = None, *, reason = "Not Specified"):
    if ctx.message.author.guild_permissions.mute_members:
        moderator = ctx.message.author
        server = ctx.guild

        muterole = discord.utils.get(member.guild.roles, name = "Muted")
        if not muterole:
            muterole = await server.create_role(name = "Muted", permissions = discord.Permissions(send_messages = False, read_messages = True))
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


#function unMute
#Will only unmute if user has "muterole"
#It will still return an error if the mute role isn't present.
@client.command()
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
@client.command()
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
@client.command()
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

'''
@client.command()
@bot_has_permissions(administrator = True)
@guild_only()
async def unban(ctx, id):
    if ctx.message.author.guild_permissions.ban_members:
        userid = await client.fetch_user(id)
        await ctx.guild.unban(userid)
        await ctx.send(userid + " has been unbanned by {0}.".format(ctx.message.author))
    else:
        await ctx.send("You don't have permission to run this command!")


@unban.error
async def fail(ctx, error):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send("You did not include a user!")
    else:
        await ctx.send(error)
'''

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send("You did not include a user!")
    elif isinstance(error, BotMissingPermissions):
        await ctx.send(error)
    else:
        await ctx.send(error)

#Secret command wo
@client.command()
async def sleep(ctx):
    owner_id = "687081333876719740"
    if str(ctx.message.author.id) == str(owner_id):
        await ctx.send("Goodnight...")
        print("User terminated the bot.")
        quit()
    else:
        await ctx.send("Only the bot owner can use this command!")

client.run(token)
