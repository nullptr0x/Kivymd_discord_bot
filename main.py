import re
import random

import discord
from typing import NoReturn
from discord.ext import commands
from res.kv_template import kivy, kivymd
from patterns import str_patterns

BOT = commands.Bot(command_prefix="$")


@BOT.listen('on_message')
async def on_message(message):
    count = 0
    for channel in message.author.guild.channels:
        if str(channel.type) == "text":
            for msg in await channel.history(limit=3).flatten():
                if message.content == msg.content:
                    count += 1
            if count > 3:
                await channel.delete_messages([discord.Object(id=message.id)])
    if count > 3:
        await message.author.kick(reason="Spam/scam")


@BOT.listen('on_ready')
async def on_ready():
    print("Beep boop")


@BOT.command(name="linkrules", help="pings the user and links the guidelines of asking questions")
async def linkrules(ctx, member: discord.Member = None, flags: str = "") -> NoReturn:
    if not member:
        await ctx.message.reply("```\nlinkrules {Member}\n            ^^^\nargument member is missing```")
        return

    if "--no-del" not in flags:
        await ctx.message.delete()

    await ctx.send(f"{member.mention}\nYour question does NOT follows the guidelines for asking questions in this "
                   "server. "
                   " Please Read the guidelines and rewrite your question in respect to them. "
                   "https://discord.com/channels/566880874789076992/618108815774056488/816265169880875018")


@BOT.command(name="kv_template", help="Returns the code of a minimal kivy application")
async def kv_template(ctx, flags: str = ""):
    if "--md" in flags.lower():
        await ctx.message.reply(kivymd)
    else:
        await ctx.message.reply(kivy)


@BOT.command(name="invite", help="returns an invite for the requested server")
async def invite(ctx, server: str = "kivy"):
    if server.lower() == "kivy":
        await ctx.message.reply("https://discord.com/invite/eT3cuQp")
    elif server.lower() == "kivymd":
        await ctx.message.reply("https://discord.gg/wu3qBST")
    else:
        await ctx.message.reply("Invite can only be one of \"Kivy\" or \"KivyMD\""
                                " (case insensitive)")


BOT.run('OTMzNzI3MTk1OTg4MzYxMzQ2.YelvNw.RMUxhqVf4KPbOSy4mPboxw1qmLU')
