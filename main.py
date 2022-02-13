import os

import discord
from typing import NoReturn
from discord.ext import commands
from res.kv_template import kivy, kivymd

BOT = commands.Bot(command_prefix="!", help_command=None)


@BOT.listen('on_message')
async def on_message(message):
    count = 0
    # tokenized_msg = message.content.split()

    # for channel in message.author.guild.channels:
    #     if str(channel.type) == "text":
    #         for msg in await channel.history(limit=3).flatten():
    #             if message.content == msg.content:
    #                 count += 1
    #         if count > 3:
    #             await channel.delete_messages([discord.Object(id=message.id)])
    # if count > 3:
    #     await message.author.kick(reason="Spam/scam")

    if message.channel.category.name == "✅ AVAILABLE HELP CHANNELS":
        if message.author != BOT.user:
            await message.channel.edit(category=BOT.get_channel(941631930779172874))
            await message.pin()


@BOT.listen("on_command_error")
async def on_command_error(ctx, err):
    await ctx.channel.send(f"```\n{err}\n```")


@BOT.listen('on_ready')
async def on_ready():
    print("Beep boop")
    activity = discord.Game(name="!help", type=3)
    await BOT.change_presence(activity=activity)


@BOT.command(name="linkrules", help="pings the user and links the guidelines of asking questions"
                                    "Usages:"
                                    "!linkrules <ping the member>")
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


@commands.has_any_role("KivyMD Team", "Extension developers")
@BOT.command(name="purge")
async def purge(ctx, limit=3):
    await ctx.channel.purge(limit=limit)


@BOT.command(name="help")
async def help(ctx):  # RIP python's builtin help function
    help_msg = discord.Embed(title="Commands", color=0x808000)
    help_msg.add_field(name="!linkrules <Member>",
                       value="Links the rules for asking questions in this server by mentioning the user\n"
                       "Flags:\n--no-del : prevents the bot from removing the command message.")

    help_msg.add_field(name="!invite <server=\"Kivy\">",
                       value="Sends the invite link of either kivy or kivymd server based on the second argument, "
                       "defaults to Kivy")

    help_msg.add_field(name="!kv_template", value="Returns the code of a minimal kivy app in case you too lazy to "
                       "write it all, pass the '--md' flag to replace Kivy with Kivymd")

    help_msg.add_field(name="!close", value="Closes the current question of the help channel and moves it to the "
                                            "available category")

    help_msg.add_field(name="!kick <Member> <reason=\"no reason provided\">", value="Kicks a member with a reason, "
                       "reason defaults to 'no reason provided'")

    help_msg.set_thumbnail(url="https://kivymd.readthedocs.io/en/latest/_static/logo-kivymd.png")

    help_msg.set_footer(text="Note that the angular brackets '<>' are just for demonstration, do not use them while "
                             "running commands. Have a great day!")

    await ctx.channel.send(embed=help_msg)


@BOT.command(name="close")
async def close(ctx):
    available_help_channel_embed = discord.Embed(title="✅ This help channel is available!", color=0x00FF00)
    available_help_channel_embed.add_field(name="Ask your question here to claim the channel",
                                           value="Please be polite and respectful, try to share a minimal code, "
                                           "explain what you expected to happen and what actually happened. Please "
                                           "refer to our guidelines to ask for help for more information, "
                                           "https://discord.com/channels/566880874789076992/618108815774056488/816265169880875018")

    await ctx.channel.edit(category=BOT.get_channel(941631710045564948))
    await ctx.channel.send(embed=available_help_channel_embed)

    pinned_msgs = await ctx.channel.pins()
    for msg in pinned_msgs:
        await msg.unpin()


@commands.has_any_role("Kivymd Team")
async def ban(ctx, member: discord.Member, reason="no reason provided"):
    await member.ban(reason=reason)


@commands.has_any_role("Kivymd Team")
async def kick(ctx, member: discord.Member, reason="no reason provided"):
    await member.kick(reason=reason)


BOT.run(os.environ["TOKEN"])
