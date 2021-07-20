import discord
from discord.ext import commands, tasks
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
    await bot.change_presence(activity=discord.Game("Going Insane"))

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
    embed = discord.Embed(title = "Invite RoboticPony", url = "https://discord.com/oauth2/authorize?client_id=834799912507277312&permissions=0&scope=bot", description = "Invite the bot with the link above!", color = 0x009933)
    await ctx.send(embed = embed)

#Help list
@bot.command()
async def commands(ctx):
    embed = discord.Embed(title = "Avalible Commands for Version 1.0 of RoboticPony:", color = 0x009933)
    embed.add_field(name = ";wave", value = "Waves hello to the bot.")
    embed.add_field(name = ";guetzali", value = "Guetzali moment", inline = False)
    embed.add_field(name = ";commands", value = "You know what this does", inline = False)
    embed.add_field(name = ";ping", value = "Bot response time.", inline = False)
    embed.add_field(name = ";kick [user] [reason]", value = "Kick a member.", inline = False)
    embed.add_field(name = ";ban [user] [reason]", value = "Bans a member.", inline = False)
    embed.add_field(name = ";sleep", value = "Puts the bot to sleep.", inline = False)
    await ctx.send(embed = embed)

@bot.command()
async def about(ctx):
    embed = discord.Embed(title = "About RoboticPony", description = "Version: 1.0\nDeveloped by: FamiliarNameMissing", color = 0x009933)
    await ctx.send(embed = embed)


#Function kickMembers
#Kicks a member and DMs them.
@bot.command()
async def kick(ctx, member: discord.User, *, reason = None):
    if ctx.message.author.guild_permissions.ban_members:
        moderator = ctx.message.author
        if member == ctx.message.author:
            await ctx.send("You cannot kick yourself!")
        #See if the moderator provided a reason.
        elif reason == None:
            await member.send("You have been kicked by {0}.".format(moderator))
            await member.kick(reason = reason)
            await ctx.send("{0} has been kicked.".format(member))
        else:
            await member.send("You have been kicked by {0} for {1}.".format(moderator, reason))
            await member.kick(reason = reason)
            await ctx.send("{0} has been kicked for {1}.".format(member, reason))
    else:
        await ctx.send("You don't have permission to run this command!")

#function banMembers
#Bans a member and DMs them
@bot.command()
async def ban(ctx, member: discord.User, *, reason = None):
    if ctx.message.author.guild_permissions.ban_members:
        moderator = ctx.message.author
        if member == ctx.message.author:
            await ctx.send("You cannot ban yourself!")
        #See if the moderator provided a reason.
        elif reason == None:
            await member.send("You have been banned by {0}.".format(moderator))
            await member.ban(reason = reason)
            await ctx.send("{0} has been banned.".format(member))
        else:
            await member.send("You have been banned by {0} for {1}.".format(moderator, reason))
            await member.ban(reason = reason)
            await ctx.send("{0} has been banned for {1}.".format(member, reason))
    else:
        await ctx.send("You don't have permission to run this command!")

#Turns the bot off
@bot.command()
async def sleep(ctx):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.send("Goodnight...")
        print("User terminated the bot.")
        quit()
    else:
        await ctx.send("You don't have permission to run this command!")


bot.run("Hehe nothing to see here")
