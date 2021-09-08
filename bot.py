import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
from secret import token
import os
import asyncio
import random

#Prefix can be changed here
prefix = "?"

intents = discord.Intents.default()
intents = discord.Intents(messages = True, guilds = True)


bot = commands.Bot(command_prefix = prefix, intents = intents)
bot.remove_command("help")

#Prints output to terminal if all is well
@bot.event
async def on_ready():
    print("We're clear for takeoff!")
    await bot.change_presence(activity = discord.Game("Going Insane | ;help"))

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

@bot.command()
async def reset(ctx):
    owner_id = "687081333876719740"
    if str(ctx.message.author.id) == str(owner_id):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                bot.unload_extension("cogs.{0}".format(filename[:-3]))
                bot.load_extension("cogs.{0}".format(filename[:-3]))
        await ctx.send("Successfully reset the bot.")
    else:
        await ctx.send("Only the bot owner can use this command!")

@bot.command()
async def unpack(ctx):
    owner_id = "687081333876719740"
    if str(ctx.message.author.id) == str(owner_id):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                bot.load_extension("cogs.{0}".format(filename[:-3]))
        await ctx.send("All extensions have been loaded.")
    else:
        await ctx.send("Only the bot owner can use this command!")

@bot.command()
async def pack(ctx):
    owner_id = "687081333876719740"
    if str(ctx.message.author.id) == str(owner_id):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                bot.unload_extension("cogs.{0}".format(filename[:-3]))
        await ctx.send("All extensions have been packed up.")
    else:
        await ctx.send("Only the bot owner can use this command!")

@reset.error
@sleep.error
@unpack.error
@pack.error
async def on_command_error(ctx, error):
    await ctx.send("`{0}`".format(error))

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension("cogs.{0}".format(filename[:-3]))

print("Second stage clear")
bot.run(token)
