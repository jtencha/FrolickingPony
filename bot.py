import os
import discord
from discord.ext import commands
import stayinAlive
import time

starttime = time.time()

token = os.environ['bottoken']

#Prefix can be changed here
prefix = "?"

intents = discord.Intents.default()
intents = discord.Intents(messages = True, guilds = True, members = True)

bot = commands.Bot(command_prefix = prefix, intents = intents)
bot.remove_command("help")

owner_id = "687081333876719740"
ember = "825212502978723861"

#check on entry
def isBanned(id, type = 1):
    if type == 1:
        with open("botbanned.txt", "r") as f:
            if id in f.read():
                return discord.Embed(title = ":x: Error", description = "You are banned from using this bot!", color = 0xff0000)
            else:
                return False
    elif type == 2:
        with open("impersonate.txt", "r") as f:
            if id in f.read():
                return discord.Embed(title = ":x: Error", description = "This user has opted out of impersonations", color = 0xff0000)
            else:
                return False

#we have to do this the hard way, it seems
def isAllowed(perm, id):
    with open("settings.txt", "r") as f:
        fl = f.readlines()
        f.close()

    for line in fl:
        serverid = line[:line.index(":")]
        usetting = line[line.index(":") + 1:line.index(";")]
        status = line[line.index(";") + 1:]
        if (int(serverid) == id):
            if perm == usetting:
                if status == "t\n":
                    return True
                else:
                    return False

#basic trigger stuff
@bot.event
async def on_ready():
    print("We're clear for takeoff!")
    await bot.change_presence(activity = discord.Game("Going Insane | " + prefix + "help"))
    #await bot.change_presence(activity = discord.Game("Undergoing Maintenance"))

@bot.event
async def on_guild_join(Guild):
    with open("settings.txt", "a+") as f:
        f.write(str(Guild.id) + ":" + "economy;f\n")
        f.write(str(Guild.id) + ":" + "moderation;f\n")
        f.write(str(Guild.id) + ":" + "gibamdib;f\n")
        f.write(str(Guild.id) + ":" + "developer;f\n")

@bot.command()
async def changestatus(ctx, *, status):
    if (str(ctx.message.author.id) == str(owner_id)) or (str(ctx.message.author.id) == str(ember)):
        await bot.change_presence(activity = discord.Game(status))
        await ctx.send("Updated status")
    else:
        await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Only the bot owner can use this command!", color = 0xff0000))


#terminate bot
@bot.command()
async def sleep(ctx):
    if (str(ctx.message.author.id) == str(owner_id)) or (str(ctx.message.author.id) == str(ember)):
        await ctx.send("Goodnight...")
        print("User terminated the bot.")
        quit()
    else:
        await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Only the bot owner can use this command!", color = 0xff0000))

#reload files
@bot.command()
async def reload(ctx):
    if (str(ctx.message.author.id) == str(owner_id)) or (str(ctx.message.author.id) == str(ember)):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                bot.unload_extension("cogs.{0}".format(filename[:-3]))
                bot.load_extension("cogs.{0}".format(filename[:-3]))

        embed = discord.Embed(title = ":white_check_mark: Cogs successfully reloaded.", description = "\n", color = 0x009933)
        await ctx.send(embed = embed)
    else:
        await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Only the bot owners can use this command!", color = 0xff0000))

#manually reload in case something doesn't work
@bot.command()
async def unpack(ctx):
    if (str(ctx.message.author.id) == str(owner_id)) or (str(ctx.message.author.id) == str(ember)):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                bot.load_extension("cogs.{0}".format(filename[:-3]))
        await ctx.send(embed = discord.Embed(title = ":white_check_mark: Wake and Shake", description = "All checks passed.", color = 0x009933))
    else:
        await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Only the bot owners can use this command!", color = 0xff0000))

@bot.command()
async def pack(ctx):

    if (str(ctx.message.author.id) == str(owner_id)) or (str(ctx.message.author.id) == str(ember)):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                bot.unload_extension("cogs.{0}".format(filename[:-3]))
        await ctx.send(embed = discord.Embed(title = ":white_check_mark: Go to Jail. Do not pass go.", description = "All checks passed.", color = 0x009933))
    else:
        await ctx.send(embed = discord.Embed(title = ":x: Error", description = "Only the bot owners can use this command!", color = 0xff0000))

@bot.command()
async def printcontents(ctx, file):
    if (str(ctx.message.author.id) == str(owner_id)):
        embed = discord.Embed(title = "Contents of {0}".format(file), description = "\n", color = 0xff6633)
        try:
            with open(file, "r") as f:
                lines = f.readlines()
                i = 1;
                for line in lines:
                    embed.add_field(name = "‎", value = "{0}: {1}".format(i, line), inline = False)
                    i+=1
            await ctx.send(embed = embed)
        except FileNotFoundError:
            await ctx.send(embed = discord.Embed(title = ":x: Error", description = "The provided file does not exist!", color = 0xff0000))


@bot.command()
async def uptime(ctx):
    if isBanned(str(ctx.message.author.id), 1) != False:
        await ctx.send(embed = isBanned(str(ctx.message.author.id)))
        return

    now = time.time()
    s = now - starttime
    m = int(s) // 60
    s = s % 60
    h = m // 60
    m = m % 60
    totaltime = "{0} hours {1} minutes {2} seconds".format(int(h), int(m), int(s))

    await ctx.send(embed = discord.Embed(title = "Bot Uptime", description = "FrolickingPony has been online for " + str(totaltime), color = 0x009933))

@reload.error
@sleep.error
@unpack.error
@pack.error
@uptime.error
async def onError(ctx, error):
    await ctx.send(embed = discord.Embed(title = ":x: Error", description = "{0}".format(error), color = 0xff0000))

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension("cogs.{0}".format(filename[:-3]))

stayinAlive.live()

print("Unloaded")
bot.run(token)
