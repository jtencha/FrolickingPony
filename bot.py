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

def isBanned(id):
    with open("botbanned.txt", "r") as f:
        if id in f.read():
            return discord.Embed(title = ":x: Error", description = "You are banned from using this bot!", color = 0xff0000)
        else:
            return False

def blocked(id):
    with open("impersonate.txt", "r") as f:
        if id in f.read():
            return discord.Embed(title = ":x: Error", description = "This user has opted out of impersonations.", color = 0xff0000)
        else:
            return False

#Prints output to terminal if all is well
@bot.event
async def on_ready():
    print("We're clear for takeoff!")
    await bot.change_presence(activity = discord.Game("Going Insane | " + prefix + "help"))

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
        channel = bot.get_channel(909985698088620122)
        await channel.send("-------------RELOADED-------------")
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
