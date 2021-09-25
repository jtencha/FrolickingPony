import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
import os
import asyncio
import random

class Functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command()
        async def avatar(ctx, member: discord.Member):
            embed = discord.Embed(title = "{0}'s avatar".format(member), description = "\n", color = 0xff6633)
            embed.set_image(url = member.avatar_url)
            await ctx.send(embed = embed)

        #Bot response time
        @bot.command()
        async def ping(ctx):
            embed = discord.Embed(title = ":ping_pong: Pong!", description = "{0}ms".format(round(bot.latency * 1000)), color = 0xff6633)
            await ctx.send(embed = embed)

        @bot.command()
        async def invite(ctx):
            embed = discord.Embed(title = "Invite RoboticPony", url = "https://discord.com/api/oauth2/authorize?client_id=834799912507277312&permissions=244239027318&scope=bot", description = "Invite the bot with the link above!", color = 0xff6633)
            await ctx.send(embed = embed)

        @bot.command()
        @bot_has_permissions(manage_messages = True)
        async def poll(ctx, option_one, option_two, option_three = None, option_four = None):
            embed = discord.Embed(title = "Poll Created by {0}".format(ctx.message.author), description = "\n", color = 0xff6633)
            embed.add_field(name = "1️⃣ Option One:", value = "{0}".format(option_one), inline = False)
            embed.add_field(name = "2️⃣ Option Two:", value = "{0}".format(option_two), inline = False)
            if option_three != None:
                embed.add_field(name = "3️⃣ Option Three:", value = "{0}".format(option_three), inline = False)
                if option_four != None:
                    embed.add_field(name = "4️⃣ Option Four:", value = "{0}".format(option_four), inline = False)

            #Deletes the command typed by the user.
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
                await ctx.send(embed = discord.Embed(title = ":x: Error", description = "You must include at least two poll options!", color = 0xff0000))
            else:
                embed = discord.Embed(title = ":x: Error", description = "```{0}```".format(error), color = 0xff0000)
                await ctx.send(embed = embed)

        #info on user
        @bot.command()
        async def about(ctx, member: discord.Member):
            embed = discord.Embed(title = "{0}".format(member), description = "User information:", color = 0xff6633)
            embed.add_field(name = "Name:", value = member.name, inline = True)
            embed.add_field(name = "User ID:", value = member.id, inline = True)
            embed.add_field(name = "Highest Role:", value = member.top_role)
            embed.add_field(name = "Created Account:", value = member.created_at)
            embed.add_field(name = "Joined Server:", value = member.joined_at)
            embed.set_thumbnail(url = member.avatar_url)
            await ctx.send(embed = embed)

        @about.error
        @avatar.error
        async def incorrect(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send("You did not include a user!")
            else:
                embed = discord.Embed(title = ":x: Error", description = "```{0}```".format(error), color = 0xff0000)
                await ctx.send(embed = embed)
                print(error)

        @bot.command()
        async def eightball(ctx, question):
            choices = ["No", "I guess", "Absolutely not.", "Ha, you wish", "Yes! Yes! and Yes!", "Unclear. Check back later.", "Without a doubt.", "If you say so", "Sussy", "Kinda sus not gonna lie"]
            await ctx.send(random.choice(choices))

        @eightball.error
        async def bad(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send("You need to ask me something...")
            else:
                embed = discord.Embed(title = ":x: Error", description = "```{0}```".format(error), color = 0xff0000)
                await ctx.send(embed = embed)

        @bot.command()
        async def embed(ctx, title, *, message = "\n"):
            embed = discord.Embed(title = title, description = message, color = 0xff6633)
            embed.set_author(name = "{0}".format(ctx.message.author), icon_url = ctx.message.author.avatar_url)
            await ctx.message.delete()
            await ctx.send(embed = embed)

        @bot.command()
        async def sourcecode(ctx):
            embed = discord.Embed(title = "Source code for RoboticPony:", description = "https://github.com/FamiliarNameMissing/RoboticPony", color = 0xff6633)
            await ctx.send(embed = embed)

        @bot.command()
        async def suggest(ctx, *, message):
            try:
                embed = discord.Embed(title = "Contact Developer", description = "Abuse will result in a ban from this command.", color = 0xff0000)
                embed.add_field(name = 'Are you sure that you want to send this message to the developer? Respond with "CONFIRM" (case sensitive).', value = "Your message: {0}".format(message))
                msg = await ctx.send(embed = embed)
                def check(msg):
                    if msg.content != "CONFIRM":
                        raise TypeError
                    else:
                        return msg.content == "CONFIRM"

                await bot.wait_for("message", check = check)
                embed = discord.Embed(title = "Suggestion by {0} from {1}:".format(ctx.message.author, ctx.guild), description = "{0}".format(message), color = 0xff6633)
                channel = bot.get_channel(890432795342696488)
                await channel.send(embed = embed)
                embed = discord.Embed(title = "Suggestion Sent", description = ":white_check_mark: Your suggestion has been sent to the developer.", color = 0x009933)
                await ctx.send(embed = embed)

            except TypeError:
                embed = discord.Embed(title = "Suggestion Terminated", description = ":x: Your suggestion has successfully been terminated.", color = 0xff0000)
                await ctx.send(embed = embed)


        @embed.error
        async def fail(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send("You need to give me at least a title to embed!")
            else:
                await ctx.send("`{0}`".format(error))

        @suggest.error
        async def failed(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send("You did not give me a suggestion!")
            else:
                embed = discord.Embed(title = ":x: Error", description = "```{0}```".format(error), color = 0xff0000)
                await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Functions(bot))
