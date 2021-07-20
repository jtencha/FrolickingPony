import discord
from discord.ext import commands, tasks
import os
import asyncio

prefix = ";"


intents = discord.Intents.default()
intents = discord.Intents(messages = True, guilds=True)


client = commands.Bot(command_prefix = prefix, intents = intents)

@client.event
async def on_ready():
    print("We're clear for takeoff!")
    await client.change_presence(activity=discord.Game("Going Insane"))

@client.command()
async def ping(ctx):
    embed = discord.Embed(title = ":ping_pong: Pong!", description = f"{round(client.latency * 1000)}ms", color = 0x009933)
    await ctx.send(embed = embed)

@client.command()
async def invite(ctx):
    embed = discord.Embed(title = "Invite RoboticPony", url = "https://discord.com/oauth2/authorize?client_id=834799912507277312&permissions=0&scope=bot", description = "Invite the bot with the link above!", color = 0x009933)
    await ctx.send(embed = embed)

@client.command()
async def sleep(ctx):
    message = await ctx.send("Goodnight...")
    print("User terminated the bot.")
    quit()


client.run("Hehe nothing to see here")
