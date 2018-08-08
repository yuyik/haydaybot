import discord
import random
from discord.ext import commands

bot_description = """
This is StatsBot, a bot originally made for r/HayDay's Discord server, now public on GitHUb
"""
bot = commands.Bot(command_prefix='?', description="description")
startup_extensions = ["Stats", "Games"]


@bot.event
async def on_ready():
    channel = bot.get_channel(channel_id)
    await channel.send("Bot is running and ready for commands.")


@commands.has_any_role()
@bot.command()
async def load(extension_name : str):
    """Loads an extension."""
    channel = bot.get_channel(channel_id)
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await channel.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await channel.send("{} loaded.".format(extension_name))


@commands.has_any_role()
@bot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    channel = bot.get_channel(channel_id)
    bot.unload_extension(extension_name)
    await channel.send("{} unloaded.".format(extension_name))
''' Information '''


@bot.command(pass_context=True, no_pm=True)
async def serverinfo(ctx):
    """Shows server's information, copied from Red (made by twentysix)"""
    server = ctx.message.server
    channel = ctx.message.channel
    online = len([m.status for m in server.members
                  if m.status == discord.Status.online or m.status == discord.Status.idle])
    total_users = len(server.members)
    text_channels = len([x for x in server.channels if x.type == discord.ChannelType.text])
    voice_channels = len([x for x in server.channels if x.type == discord.ChannelType.voice])
    passed = (ctx.message.timestamp - server.created_at).days
    created_at = ("Since {}. That's over {} days ago!"
                  "".format(server.created_at.strftime("%d %b %Y %H:%M"), passed))

    colour = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
    colour = int(colour, 16)

    data = discord.Embed(
        description=created_at,
        colour=discord.Colour(value=colour))
    data.add_field(name="Region", value=str(server.region))
    data.add_field(name="Users", value="{}/{}".format(online, total_users))
    data.add_field(name="Text Channels", value=str(text_channels))
    data.add_field(name="Voice Channels", value=str(voice_channels))
    data.add_field(name="Roles", value=str(len(server.roles)))
    data.add_field(name="Owner", value=str(server.owner))
    data.set_footer(text="Server ID: " + server.id)

    if server.icon_url:
        data.set_author(name=server.name, url=server.icon_url)
        data.set_thumbnail(url=server.icon_url)
    else:
        data.set_author(name=server.name)

    try:
        await channel.send(embed=data)
    except discord.HTTPException:
        await channel.send("I need the `Embed links` permission "
                           "to send this")


@commands.has_any_role()
@bot.command()
async def reset():
    """
    Resets profile picture and username back to original
    """
    picture = open("profile_pic", "rb")
    await bot.user.edit_profile(avatar=picture.read(), username="username")


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


bot.run("token")
