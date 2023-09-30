import discord
import os
import random
import logging
import users
from drinking_sentences import sentence_data
from helpers import EMBED_COLOR, simple_embed
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger('discord')
logger.name = 'application'


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    logger.info("Bot is Online")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="getting DRUNK!!!"))
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.exception(e)

@bot.tree.command(name="spin")
async def spin(ctx):
    """
    returns a random choice from wheel

    Usage:
    !spin
    """
    sentences, probabilities = zip(*sentence_data)
    choice = random.choice(random.choices(sentences, probabilities))
    await ctx.response.send_message(embed=simple_embed('Your Task:', choice))


@bot.tree.command(name="ping")
async def ping(ctx):
    """
    Pings the bot and send a response with the time needed in ms

    Usage:
    !ping
    """
    await ctx.response.send_message(embed=simple_embed(f"Pong! {round(bot.latency * 1000)}ms"))

@bot.tree.command(name="addme")
async def addme(ctx):
    await ctx.response.send_message(embed=simple_embed('Info', users.add_user(ctx.guild.id, ctx.user.mention)))

@bot.tree.command(name="adduser")
async def adduser(ctx, user_name: discord.Member):
    await ctx.response.send_message(embed=simple_embed('Info', users.add_user(ctx.guild.id, user_name.mention)))

@bot.tree.command(name="removeme")
async def removeme(ctx):
    await ctx.response.send_message(embed=simple_embed('Info', users.remove_user(ctx.guild.id, ctx.user.mention)))

@bot.tree.command(name="removeuser")
async def removeme(ctx, user_name: discord.Member):
    await ctx.response.send_message(embed=simple_embed('Info', users.remove_user(ctx.guild.id, user_name.mention)))

@bot.tree.command(name="list")
async def list(ctx):
    await ctx.response.send_message(embed=simple_embed('Users', users.get_users(ctx.guild.id)))

@bot.tree.command(name="shot")
async def shot(ctx):
    if users.check_user(ctx.guild.id, ctx.user.mention) == True:
        await ctx.response.send_message(embed=simple_embed('Take a Shot!', random.choice(users.users[ctx.guild.id])))
        return
    await ctx.response.send_message(embed=simple_embed('Take a Shot for not beeing in the list!', ctx.user.mention))

@bot.tree.command(name="info")
async def info(ctx):
    await ctx.response.send_message("https://github.com/Katze719/CaptainDrunk")

bot.run(str(os.getenv('Token')))
