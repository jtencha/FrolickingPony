import os
import discord
from discord.ext import commands
import stayinAlive

token = os.environ['bottoken']

#Prefix can be changed here
prefix = "?"

intents = discord.Intents.default()
intents = discord.Intents(messages = True, guilds = True, members = True)


bot = commands.Bot(command_prefix = prefix, intents = intents)
bot.remove_command("help")

#Prints output to terminal if all is well
@bot.event
async def on_ready():
    print("We're clear for takeoff!")
    await bot.change_presence(activity = discord.Game("Going Insane | ?help"))

#Secret command wo
@bot.command()
async def sleep(ctx):
    owner_id = "687081333876719740"
    if str(ctx.message.author.id) == str(owner_id):
        await ctx.send("Goodnight...")
        print("User terminated the bot.")
        quit()
    else:
        await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Only the bot owner can use this command!", color = 0xff0000))

@bot.command()
async def reload(ctx):
    owner_id = "687081333876719740"
    if str(ctx.message.author.id) == str(owner_id):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                bot.unload_extension("cogs.{0}".format(filename[:-3]))
                bot.load_extension("cogs.{0}".format(filename[:-3]))

        embed = discord.Embed(title = ":white_check_mark: Cogs successfully reloaded.", description = "\n", color = 0x009933)
        await ctx.send(embed = embed)
    else:
        await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Only the bot owner can use this command!", color = 0xff0000))

@bot.command()
async def unpack(ctx):
    owner_id = "687081333876719740"
    if str(ctx.message.author.id) == str(owner_id):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                bot.load_extension("cogs.{0}".format(filename[:-3]))
        await ctx.send(embed = discord.Embed(title = ":white_check_mark: Unpacked", description = "Successfully loaded cogs", color = 0x009933))
    else:
        await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Only the bot owner can use this command!", color = 0xff0000))

@bot.command()
async def pack(ctx):
    owner_id = "687081333876719740"
    if str(ctx.message.author.id) == str(owner_id):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                bot.unload_extension("cogs.{0}".format(filename[:-3]))
        await ctx.send(embed = discord.Embed(title = ":white_check_mark: Packed", description = "Successfully packed cogs", color = 0x009933))
    else:
        await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Only the bot owner can use this command!", color = 0xff0000))

@reload.error
@sleep.error
@unpack.error
@pack.error
async def onError(ctx, error):
    await ctx.send(embed = discord.Embed(title = ":x: Error", description = "{0}".format(error), color = 0xff0000))

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension("cogs.{0}".format(filename[:-3]))

stayinAlive.live()

print("Unloaded")
bot.run(token)