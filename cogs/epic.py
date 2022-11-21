import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
import os
import asyncio
import random
from bot import *

class Epic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        async def guetzali(ctx):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return

            embed = discord.Embed(title = "", description = "", color = 0xff6633)
            embed.set_image(url = random.choice([
            "https://media.discordapp.net/attachments/842447676414361620/843713059033710632/60a1f6f95aa22378467759.gif",
            "https://media.discordapp.net/attachments/404803931227553802/860570669322469377/quetzali.gif",
            "https://media.discordapp.net/attachments/863137688470814741/863936864054149140/makesweet-kxksih.gif",
            "https://media.discordapp.net/attachments/404803931227553802/859942873864994816/697995591921172532-8.gif",
            "https://media.discordapp.net/attachments/842447676414361620/843713059033710632/60a1f6f95aa22378467759.gif",
            ]))
            await ctx.send(embed = embed)


        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        async def amogus(ctx):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return

            embed = discord.Embed(title = random.choice(["Sus", "Sussy", "AMOGUS", "I love amogus", "{0} is sus".format(ctx.message.author)]), description = "\n", color = 0xff6633)
            embed.set_image(url = random.choice(["https://media.discordapp.net/attachments/727291251308757113/864568490626777119/image0-2-1-1-1-1-1-1.gif",
            "https://c.tenor.com/k_H-Sf-5D8IAAAAd/sus-amogus.gif",
            "https://media.discordapp.net/attachments/547864105046769676/886434964479029279/de65d757-bbd8-4e7e-b0c7-7ac35d148b14.gif",
            "https://c.tenor.com/XhYqu5fu4LgAAAAd/boiled-soundcloud-boiled.gif",
            "https://images-ext-2.discordapp.net/external/NzwN2rQSZUejBtxqPh2D9HmNxygXA6kb22GjkFqAQ9o/https/media.discordapp.net/attachments/854081705496412180/898367828674113606/amogus-usa.gif",
            "https://c.tenor.com/FVnOj2hqoGkAAAAC/among-us-funny-dance.gif",
            "https://c.tenor.com/UBSIHrmTLW0AAAAC/among-us-minecraft.gif",
            "https://c.tenor.com/wEwQbVsYwlwAAAAM/hi.gif"
            ]))

            msg = await ctx.send(embed = embed)

        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        async def redpanda(ctx):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return

            embed = discord.Embed(title = "Red Panda, My Beloved", description = "\n", color = 0xff6633)
            embed.set_image(url = random.choice(["https://cdn.discordapp.com/avatars/825212502978723861/c94bd91c4e02b1c9600418e7f8631157.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891099004446842880/redpanda.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891099410040229908/red-panda-3.png",
            "https://media.discordapp.net/attachments/866857228833128449/891099663250362398/OIP.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891100220560121856/OIP.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891100315544326144/OIP.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891100505693093938/OIP.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891100587259740190/OIP.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891100785260265502/red-pandas-cincinnati-zoo-3.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891101059190247444/OIP.png"
            "https://www.thoughtco.com/thmb/s-sGgR7zQSq2tZlZMlD7uuY81Gk=/7360x4912/filters:fill(auto,1)/happy-red-panda-171399380-5b574325c9e77c005b690b41.jpg"


            ]))
            await ctx.send(embed = embed)

        #I hate await async behavior so goddamn much
        #command developed for polyeggia server, per request
        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        async def gibamdib(ctx, status = None):
            server = ctx.guild
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            elif isAllowed("gibamdib", ctx.message.guild.id) == False:
                await ctx.send(embed = discord.Embed(title = ":x: Command Disabled", description = "A server administrator has disabled the gibamdib command.", color = 0xff0000))
                return

            try:
                amdib = discord.utils.get(ctx.message.author.guild.roles, name = "Def Real Amdib")
                if not amdib:
                    amdibrole = await server.create_role(name = "Def Real Amdib", permissions = discord.Permissions(mute_members = True, send_messages = True))
                    for channel in ctx.guild.channels:
                        locked = channel.overwrites_for(amdibrole)
                        locked.mute_members = True
                        await channel.set_permissions(amdibrole, overwrite = locked)
                        await ctx.send("Configured. Re-run the command.")
                        return
                elif status == "remove" and amdib in ctx.message.author.roles:
                    await ctx.message.author.remove_roles(amdib)
                    await ctx.send("You are not amdib anymore rib")
                    return
                elif status == "remove" and amdib not in ctx.message.author.roles:
                    await ctx.send("You can't remove a role you don't have...")
                    return
                elif amdib not in ctx.message.author.roles:
                    await ctx.message.author.add_roles(amdib)
                    await ctx.send('You are now amdib wo. Use "?gibamdib remove" to resign.')
                    await ctx.send("<:pandaqop:942169694717239307>")
                    return
                elif amdib in ctx.message.author.roles:
                    await ctx.send("You are already amdib eggs d")
                    return
                else:
                    embed = discord.Embed(title = ":x: Error", description = "You aren't supposed to get here", color = 0xff0000)
                    await ctx.send(embed = embed)
                    return
            except discord.Forbidden:
                await ctx.send(embed = discord.Embed(title = ":x: Fatal Executuion Error", description = "An error occurred while running this command. The most likely cause is that you have a higher role than the bot.", color = 0xff0000))
                return

        @gibamdib.error
        async def amdibError(ctx, error):
            await ctx.send(embed = discord.Embed(title = ":x: Error", description = "```{0}```".format(error), color = 0xff0000))

        @bot.command(aliases = ["im"])
        @bot_has_permissions(manage_webhooks = True)
        async def impersonate(ctx, member: discord.Member, *, message = None):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return

            elif isBanned(str(member.id), 2) != False:
                #I had this as a function but I have no clue why it kept trying to convert this to a dict
                #ALas, I love my functions but I go the long way for now
                embed = discord.Embed(title = ":x: Error", description = "This user has opted out of impersonations.", color = 0xff0000)
                await ctx.send(embed = embed)
                return

            elif message == None:
                await ctx.send("You need to say something!")
                return
            else:
                await ctx.message.delete()
                webhook = await ctx.channel.create_webhook(name = member.name)
                await webhook.send(str(message), username = member.name, avatar_url = member.avatar_url)
                await webhook.delete()

        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        async def block(ctx):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return

            else:
                count = 0
                with open("impersonate.txt", "r") as f:
                    fl = f.readlines()
                with open("impersonate.txt", "w") as f:
                    for l in fl:
                        if l.strip("\n") != str(ctx.message.author.id):
                            f.write(l)
                        else:
                            count += 1

                if count == 0:
                    with open("impersonate.txt", "a+") as f:
                        f.write(str(ctx.message.author.id) + "\n")
                    await ctx.send(embed = discord.Embed(title = ":white_check_mark: Block Successful", description = "Users will not be able to mimic you.", color = 0x009933))
                    return
                else:
                    embed = discord.Embed(title = ":white_check_mark: Unblock Successful", description = "Users will be able to mimic you.", color = 0x009933)
                    await ctx.send(embed = embed)

        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        async def ezmoney(ctx):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            else:
                embed = discord.Embed(title = "", description = "", color = 0xff6633)
                embed.set_image(url = "https://c.tenor.com/b7jgsT3ctlwAAAAC/when-the-money-fast-money.gif")
                await ctx.send(embed = embed)


        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        async def laugh(ctx):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            else:
                embed = discord.Embed(title = "", description = "", color = 0xff6633)
                embed.set_image(url = "https://c.tenor.com/nbJLAkkQ4QQAAAAC/woody-laugh.gif")
                await ctx.send(embed = embed)

        @bot.command()
        @bot_has_permissions(manage_webhooks = True)
        async def poor(ctx):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return
            else:
                embed = discord.Embed(title = "", description = "", color = 0xff6633)
                embed.set_image(url = 'https://c.tenor.com/oCxcur4d32wAAAAC/squidward-spare-change.gif')
                await ctx.send(embed = embed)

        #--EXCEPTION HANDLING--
        #Dump all of these into one handler
        @impersonate.error
        @block.error
        @amogus.error
        @gibamdib.error
        @laugh.error
        @poor.error
        @ezmoney.error
        @redpanda.error
        @guetzali.error
        async def impError(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send(embed = discord.Embed(title = ":x: Error", description = "You must include a user to impersonate!", color = 0xff0000))
            elif isinstance(error, BotMissingPermissions):
                await ctx.send(f"I don't have permission to run this command! Required: {' '.join(error.missing_perms)}")
            else:
                await ctx.send(embed = discord.Embed(title = ":x: Fatal Error", description = "An internal error prevented the bot from finishing your request. Please try again later.\n\nReference: `{0}`".format(error), color = 0xff0000))
                channel = bot.get_channel(942166599710965831)
                await channel.send("<@687081333876719740> error thrown in {0}".format(ctx.message.guild))

def setup(bot):
    bot.add_cog(Epic(bot))
