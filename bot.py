import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions
from discord import Member
import os
import asyncio
import random

#Prefix can be changed here
prefix = ";"

intents = discord.Intents.default()
intents = discord.Intents(messages = True, guilds = True)


bot = commands.Bot(command_prefix = prefix, intents = intents)

#Prints output to terminal if all is well
@bot.event
async def on_ready():
    print("We're clear for takeoff!")
    await bot.change_presence(activity=discord.Game("Going Insane | ;commands 1"))

#Chooses a random greeting
@bot.command()
async def wave(ctx):
    await ctx.send(random.choice(["Hello", "Helgo 👋", ":wavezali:", "Hey!", "Helg", ":floofwave:"]))

@bot.command()
async def guetzali(ctx):
    await ctx.send(random.choice(["Guetzali Guetzali",
    "https://media.discordapp.net/attachments/842447676414361620/843713059033710632/60a1f6f95aa22378467759.gif",
    "https://media.discordapp.net/attachments/404803931227553802/860570669322469377/quetzali.gif",
    "https://media.discordapp.net/attachments/863137688470814741/863936864054149140/makesweet-kxksih.gif",
    "https://media.discordapp.net/attachments/404803931227553802/859942873864994816/697995591921172532-8.gif"
    ]))
#Ping
@bot.command()
async def ping(ctx):
    embed = discord.Embed(title = ":ping_pong: Pong!", description = f"{round(bot.latency * 1000)}ms", color = 0x009933)
    await ctx.send(embed = embed)

#Invite command
@bot.command()
async def invite(ctx):
    embed = discord.Embed(title = "Invite RoboticPony", url = "https://discord.com/oauth2/authorize?client_id=834799912507277312&permissions=8&scope=bot", description = "Invite the bot with the link above!", color = 0x009933)
    await ctx.send(embed = embed)

#Help list
@bot.command()
async def commands(ctx, type):
    if type == "1":
        embed = discord.Embed(title = "Avalible Commands:", description = "Commands marked with an * require permissions \n\nUse ;commands [number] to navigate the command list.", color = 0x009933)
        embed.add_field(name = ";wave", value = "Waves hello to the bot.")
        embed.add_field(name = ";guetzali", value = "Guetzali moment", inline = False)
        embed.add_field(name = ";commands [number]", value = "You know what this does", inline = False)
        embed.add_field(name = ";invite", value = "Invite RoboticPony", inline = False)
        embed.add_field(name = ";ping", value = "Bot response time.", inline = False)
        embed.add_field(name = ";poll [option] [option] [option] [option]", value = "Create a poll", inline = False)
        embed.add_field(name = "\nList 1 of 2", value = "\n\nNote: this bot requires administrator to function properly.", inline = False)
        await ctx.send(embed = embed)
    elif type == "2":
        embed = discord.Embed(title = "Avalible Commands:", description = "Commands marked with an * require permissions \n\nUse ;commands [number] to navigate the command list.", color = 0x009933)
        embed.add_field(name = ";about", value = "About RoboticPony", inline = False)
        embed.add_field(name = ";mute [user] [reason]*", value = "Mute a user permanently", inline = False)
        embed.add_field(name = ";unmute [user] [reason]*", value = "Unmute a user", inline = False)
        embed.add_field(name = ";kick [user] [reason]*", value = "Kicks a member.", inline = False)
        embed.add_field(name = ";ban [user] [reason]*", value = "Bans a member.", inline = False)
        embed.add_field(name = "Secret Command*", value = "Puts the bot to sleep.", inline = False)
        embed.add_field(name = "\nList 2 of 2", value = "\n\nNote: this bot requires administrator to function properly.")
        await ctx.send(embed = embed)
    else:
        await ctx.send("Use ;commands 1 or ;commands 2 to view the help menus.")

@commands.error
async def no_good(ctx, error):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send("You must include a number after ;commands")
    else:
        await ctx.send(error)

@bot.command()
async def poll(ctx, option_one, option_two, option_three = None, option_four = None):
    embed = discord.Embed(title = "Poll Created by {0}".format(ctx.message.author), description = "\n", color = 0x009933)
    embed.add_field(name = "1️⃣ Option One:", value = "{0}".format(option_one), inline = False)
    embed.add_field(name = "2️⃣ Option Two:", value = "{0}".format(option_two), inline = False)
    if option_three != None:
        embed.add_field(name = "3️⃣ Option Three:", value = "{0}".format(option_three), inline = False)
        if option_four != None:
            embed.add_field(name = "4️⃣ Option Four:", value = "{0}".format(option_four), inline = False)

#Inefficient, but it gets the job done. I'll make it prettier and less repetitive later.
    poll = await ctx.send(embed = embed)
    await poll.add_reaction("1️⃣")
    await poll.add_reaction("2️⃣")
    if option_three != None:
        await poll.add_reaction("3️⃣")
        if option_four != None:
            await poll.add_reaction("4️⃣")

@poll.error
async def denied(ctx, error):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send("You must include at least two choices!")
    elif isinstance(error, BotMissingPermissions):
        await ctx.send("Fatal error, please try again.")
    else:
        await ctx.send(error)

@bot.command()
async def about(ctx):
    embed = discord.Embed(title = "About RoboticPony", description = "Version: 1.4.2\nDeveloped by: FamiliarNameMissing", color = 0x009933)
    await ctx.send(embed = embed)

#Function mute
#Mutes a member forever and DMs them.
@bot.command()
@bot_has_permissions(administrator = True)
async def mute(ctx, member: discord.User, *, reason = "Not Specified"):
    if ctx.message.author.guild_permissions.mute_members:
        moderator = ctx.message.author
        server = ctx.guild
        #Checks for a reason
        #If none, assigns "Not specified"
        if reason == None:
            reason = "Not Specified"
        try:
            muterole = discord.utils.get(member.guild.roles, name = "Muted")
            await member.add_roles(muterole)
            await ctx.send("{0} has been muted for {1}.".format(member, reason))
        except AttributeError:
            await ctx.send('Please configure a role named "Muted" for the bot to use.')
        except discord.Forbidden:
            await ctx.send("I was unable to mute this user.")
            return
        try:
            await member.send("You have been muted by {0} in {1} for {2}.".format(moderator, member, reason))
        except discord.Forbidden:
            await ctx.send("I can't DM this user.")
    else:
        await ctx.send("You don't have permission to run this command!")
        return

@mute.error
async def nope(ctx, error):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send("You did not include a user!")
    elif isinstance(error, BotMissingPermissions):
        await ctx.send("This bot requires administrator.")
    else:
        await ctx.send(error)

@bot.command()
@bot_has_permissions(administrator = True)
async def unmute(ctx, member: discord.User, *, reason = "Not Specified"):
    if ctx.message.author.guild_permissions.mute_members:
        moderator = ctx.message.author
        server = ctx.guild
        try:
            muterole = discord.utils.get(member.guild.roles, name = "Muted")
            await member.remove_roles(muterole)
            await ctx.send("{0} has been unmuted for {1}.".format(member, reason))
        except AttributeError:
            await ctx.send('Please configure a role named "Muted" for the bot to use.')
        except discord.Forbidden:
            await ctx.send("I was unable to unmute this user.")
            return
        try:
            await member.send("You have been unmuted by {0} in {1} for {2}.".format(moderator, member, reason))
        except discord.Forbidden:
            await ctx.send("I can't DM this user.")
    else:
        await ctx.send("You don't have permission to run this command!")
        return

@unmute.error
async def nope(ctx, error):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send("You did not include a user!")
    elif isinstance(error, BotMissingPermissions):
        await ctx.send("This bot requires administrator.")
    else:
        await ctx.send(error)
#Function kickMembers
#Kicks a member and DMs them.
#Returns if the targeted user is too powerful or the bot lacks perms.
@bot.command()
@bot_has_permissions(administrator = True)
async def kick(ctx, member: discord.User, *, reason = "Not Specified"):
    if ctx.message.author.guild_permissions.kick_members:
        moderator = ctx.message.author
        server = ctx.guild
        #See if the moderator provided a reason.
        #Assigns "Not specified" if none
        #Will still kick and return a custom error if DM fails.
        if reason == None:
            reason = "Not Specified"
        try:
            await member.kick(reason = reason)
        except discord.Forbidden:
            await ctx.send("I was unable to kick this user.")
            return
        try:
            await member.send("You have been kicked from {0} by {1} for {2}.".format(server, moderator, reason))
        except discord.Forbidden:
            await ctx.send("I can't DM this user. ")

        await ctx.send("{0} has been kicked for {1}.".format(member, reason))
    else:
        await ctx.send("You don't have permission to run this command!")
        return

#Check for garbage
@kick.error
async def rejected(ctx, error):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send("You did not include a user!")
    elif isinstance(error, BotMissingPermissions):
        await ctx.send("This bot requires administrator.")
    else:
        await ctx.send(error)


#function banMembers
#Bans a member and DMs them
#Returns if the targeted user is too powerful or the bot lacks perms.
@bot.command()
@bot_has_permissions(administrator = True)
async def ban(ctx, member: discord.User, *, reason = "Not Specified"):
    if ctx.message.author.guild_permissions.ban_members:
        moderator = ctx.message.author
        server = ctx.guild
        #See if the moderator provided a reason.
        #Assigns "not specified" if none.
        #Will still kick and return a custom error if DM fails.
        if reason == None:
            reason = "Not Specified"
        try:
            await member.ban(reason = reason)
        except discord.Forbidden:
            await ctx.send("I was unable to ban this user.")
            return
        try:
            await member.send("You have been banned from {0} by {1} for {2}.".format(server, moderator, reason))
        except discord.Forbidden:
            await ctx.send("I can't DM this user.")

        await ctx.send("{0} has been banned for {1}.".format(member, reason))
    else:
        await ctx.send("You don't have permission to run this command!")

#Check for garbage
@ban.error
async def rejected(ctx, error):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send("You did not include a user!")
    elif isinstance(error, BotMissingPermissions):
        await ctx.send("This bot requires administrator.")
    else:
        await ctx.send(error)


#Secret command wo
@bot.command()
async def sleep(ctx):
    owner_id = "687081333876719740"
    if str(ctx.message.author.id) == str(owner_id):
        await ctx.send("Goodnight...")
        print("User terminated the bot.")
        quit()
    else:
        await ctx.send("Only the bot owner can use this command!")


bot.run("Hehe nothing to see here")
