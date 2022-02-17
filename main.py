import os

import discord
from typing import NoReturn
from discord.ext import commands
from res.kv_template import kivy, kivymd

BOT = commands.Bot(command_prefix="!", help_command=None)


@BOT.listen('on_message')
async def on_message(message):
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
@BOT.command(name="ban")
async def ban(ctx, member: discord.Member, reason="no reason provided"):
    await member.ban(reason=reason)


@commands.has_any_role("Kivymd Team")
@BOT.command(name="kick")
async def kick(ctx, member: discord.Member, reason="no reason provided"):
    await member.kick(reason=reason)


@BOT.command(name="docs")
async def docs(ctx, target, flags=""):
    doc_links = [
        "https://kivymd.readthedocs.io/en/latest/themes",
        "https://kivymd.readthedocs.io/en/latest/components/anchorlayout",
        "https://kivymd.readthedocs.io/en/latest/components/backdrop",
        "https://kivymd.readthedocs.io/en/latest/components/banner",
        "https://kivymd.readthedocs.io/en/latest/components/bottomnavigation",
        "https://kivymd.readthedocs.io/en/latest/components/bottomsheet",
        "https://kivymd.readthedocs.io/en/latest/components/boxlayout",
        "https://kivymd.readthedocs.io/en/latest/components/button",
        "https://kivymd.readthedocs.io/en/latest/components/card",
        "https://kivymd.readthedocs.io/en/latest/components/carousel",
        "https://kivymd.readthedocs.io/en/latest/components/chip",
        "https://kivymd.readthedocs.io/en/latest/components/circularlayout",
        "https://kivymd.readthedocs.io/en/latest/components/colorpicker",
        "https://kivymd.readthedocs.io/en/latest/components/datatables",
        "https://kivymd.readthedocs.io/en/latest/components/datepicker",
        "https://kivymd.readthedocs.io/en/latest/components/dialog",
        "https://kivymd.readthedocs.io/en/latest/components/dropdownitem",
        "https://kivymd.readthedocs.io/en/latest/components/expansionpanel",
        "https://kivymd.readthedocs.io/en/latest/components/filemanager",
        "https://kivymd.readthedocs.io/en/latest/components/fitimage",
        "https://kivymd.readthedocs.io/en/latest/components/floatlayout",
        "https://kivymd.readthedocs.io/en/latest/components/gridlayout",
        "https://kivymd.readthedocs.io/en/latest/components/imagelist",
        "https://kivymd.readthedocs.io/en/latest/components/label",
        "https://kivymd.readthedocs.io/en/latest/components/list",
        "https://kivymd.readthedocs.io/en/latest/components/mdswiper",
        "https://kivymd.readthedocs.io/en/latest/components/menu",
        "https://kivymd.readthedocs.io/en/latest/components/navigationdrawer",
        "https://kivymd.readthedocs.io/en/latest/components/navigationrail",
        "https://kivymd.readthedocs.io/en/latest/components/progressbar",
        "https://kivymd.readthedocs.io/en/latest/components/refreshlayout"
        "https://kivymd.readthedocs.io/en/latest/components/relativelayout"
        "https://kivymd.readthedocs.io/en/latest/components/screen",
        "https://kivymd.readthedocs.io/en/latest/components/selection",
        "https://kivymd.readthedocs.io/en/latest/components/selectioncontrols"
        "https://kivymd.readthedocs.io/en/latest/components/slider",
        "https://kivymd.readthedocs.io/en/latest/components/snackbar",
        "https://kivymd.readthedocs.io/en/latest/components/spinner",
        "https://kivymd.readthedocs.io/en/latest/components/stacklayout",
        "https://kivymd.readthedocs.io/en/latest/components/tabs",
        "https://kivymd.readthedocs.io/en/latest/components/taptargetview",
        "https://kivymd.readthedocs.io/en/latest/components/textfield",
        "https://kivymd.readthedocs.io/en/latest/components/timepicker",
        "https://kivymd.readthedocs.io/en/latest/components/toolbar",
        "https://kivymd.readthedocs.io/en/latest/components/tooltip",
        "https://kivymd.readthedocs.io/en/latest/components/transition",
        "https://kivymd.readthedocs.io/en/latest/components/widget",
        "https://kivymd.readthedocs.io/en/latest/behaviors/background-color",
        "https://kivymd.readthedocs.io/en/latest/behaviors/elevation",
        "https://kivymd.readthedocs.io/en/latest/behaviors/focus",
        "https://kivymd.readthedocs.io/en/latest/behaviors/hover",
        "https://kivymd.readthedocs.io/en/latest/behaviors/magic",
        "https://kivymd.readthedocs.io/en/latest/behaviors/ripple",
        "https://kivymd.readthedocs.io/en/latest/behaviors/togglebutton",
        "https://kivymd.readthedocs.io/en/latest/behaviors/touch",
        "https://kivymd.readthedocs.io/en/latest/effects/fadingedgeeffect",
        "https://kivymd.readthedocs.io/en/latest/effects/roulettescrolleffect",
        "https://kivymd.readthedocs.io/en/latest/effects/stiffscrolleffect",
        "https://kivymd.readthedocs.io/en/latest/templates/rotatewidget",
        "https://kivymd.readthedocs.io/en/latest/templates/scalewidget",
        "https://kivymd.readthedocs.io/en/latest/templates/stencilwidget",
    ]

    pages = [link.split('/')[-1] for link in doc_links]

    for page in pages:
        if page == target:
            await ctx.channel.send(doc_links[pages.index(page)])
        else:
            await ctx.channel.send(f"Sorry, but I can't find the docs of the target {target}")


BOT.run(os.environ["TOKEN"])
