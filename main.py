import discord
import json
import os
import random
import logging
# from . import img_gen
from drinking_sentences import sentence_data
from helpers import EMBED_COLOR, simple_embed
from discord.ext import commands

logger = logging.getLogger('discord')

def log(ctx, msg):
    logger.info(f"{ctx.author.name} from {ctx.guild.name} {msg}")


def add_user(ctx, user_name):
    if not os.path.exists(f"{ctx.guild.name}_users.json"):
        with open(f"{ctx.guild.name}_users.json", 'w+') as f_:
            d = {"names":[]}
            json.dump(d, f_, indent=4)

    with open(f"{ctx.guild.name}_users.json", 'r+') as f:
        json_data = json.load(f)
        json_data['names'].append(user_name)
        f.seek(0)
        json.dump(json_data, f, indent=4)
    logger.info(f"{user_name} from server {ctx.guild.name} added")

def clear_users(ctx):
    with open(f"{ctx.guild.name}_users.json", 'r+') as f:
        json_data = json.load(f)
        json_data['names'] = []
    os.remove(f"{ctx.guild.name}_users.json")
    with open(f"{ctx.guild.name}_users.json", 'w+') as f:
        json.dump(json_data, f, indent=4)
    log(ctx, "cleared all users!")

def get_users(ctx, mention_users=False):

    log(ctx, "requested a user list")
    online_usernames = []
    bot_list = ['Vinny', 'Maki', 'Captain Drunk']

    for member in ctx.guild.members:
        if member.status == discord.Status.online:
            online_usernames.append(member.name)
    
    for bot_name in bot_list:
        if bot_name in online_usernames:
            online_usernames.remove(bot_name)

    print(online_usernames)


    with open(f"{ctx.guild.name}_users.json", 'r') as f:
        json_data = json.load(f)
        response = ''
        for name in json_data['names']:
            for user, mention in name.items():
                if mention_users:
                    response += str('- ' + mention + '\n')
                else:
                    response += str('- ' + user + '\n')
        return response
    
def delete_user(ctx, user_name):
    with open(f"{ctx.guild.name}_users.json", 'r') as f:
        json_data = json.load(f)
        for i, dic in enumerate(json_data["names"]):
            for name, mention in dic.items():
                if name == user_name:
                    del json_data["names"][i]
                    break
    os.remove(f"{ctx.guild.name}_users.json")
    with open(f"{ctx.guild.name}_users.json", 'w+') as f:
        json.dump(json_data, f, indent=4)
    log(ctx, "removed from the list")

bot = commands.Bot(command_prefix="%", intents=discord.Intents.all())

@bot.event
async def on_ready():
    logger.info("Bot is Online")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="getting DRUNK!!!"))

@bot.command(aliases=['time'])
async def ping(ctx):
    """
    Pings the bot and send a response with the time needed in ms

    Usage:
    !ping
    """
    await ctx.reply(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command(aliases=['add_me', 'addMe', 'AddMe', 'Addme', 'join'])
async def addme(ctx):
    """
    Adds the user to the list, and makes him ready to Drink a few shots :)

    Usage:
    !addme
    """
    await ctx.reply(embed=simple_embed("Added!", ctx.author.mention))
    add_user(ctx, {ctx.author.name : ctx.author.mention})

@bot.command()
async def clear_list(ctx):
    """
    DO NOT USE THIS, use `!remove_me` instead

    Usage:
    !clear_list

    clears the list of users for the server
    """
    await ctx.reply(embed=simple_embed("cleared the list!", ''))
    clear_users(ctx)

@bot.command(aliases=['list', 'list_users', 'list-users'])
async def users(ctx, raw=''):
    """
    returns a list of users ready to drink (with the real discord names)

    Usage:
    !users
    !users raw
    """
    if raw == 'raw':
        with open(f"{ctx.guild.name}_users.json", 'r') as f:
            await ctx.reply(json.load(f)['names'])
            return

    await ctx.reply(embed=simple_embed('People ready to DRINK', get_users(ctx)))

@bot.command(aliases=['mention', 'drunk'])
async def message(ctx):
    """
    mentions every user in the list ready to drink

    Usage:
    !message
    """
    await ctx.reply(embed=simple_embed('get yo ass in here, my favourite drunken boys and girls !!!', get_users(ctx, True)))

@bot.command(aliases=['DRINK', 'Drink'])
async def drink(ctx):
    """
    mentions every user in the list and prompts them to take a shot

    Usage:
    !drink
    """
    await ctx.reply(embed=simple_embed('TIME TO TAKE A SHOT!!!', get_users(ctx, True)))

@bot.command(aliases=['SHOT', 'Shot'])
async def shot(ctx):
    """
    picks a random user in the list and prompts him to take a shot

    Usage:
    !shot
    """
    with open(f"{ctx.guild.name}_users.json", 'r') as f:
        json_data = json.load(f)
        choice = random.choice(json_data['names'])
        for user, mention in choice.items():
            response = 'YOU HAVE BEEN CHOSEN TO TAKE A SHOT!!!'
    await ctx.reply(embed=simple_embed(response, mention))

@bot.command(aliases=['remove-me', 'delete-me'])
async def remove_me(ctx):
    """
    removes you from the list (pussy)

    Usage:
    !remove_me
    """
    await ctx.reply(embed=simple_embed("removed you from the list!"))
    delete_user(ctx, ctx.author.name)

@bot.command(aliases=['slots', 'wheel'])
async def spin(ctx):
    """
    returns a random choice from wheel

    Usage:
    !spin
    """
    sentences, probabilities = zip(*sentence_data)
    # img_gen.get_img(len(sentences))
    # file = discord.File("spin.png")
    choice = random.choice(random.choices(sentences, probabilities))
    await ctx.reply(embed=simple_embed('Your Task:', choice))
    log(ctx, f"spin={choice}")

@bot.command()
async def info(ctx):
    await ctx.reply("https://github.com/Katze719/CaptainDrunk")

bot.run(str(os.getenv('DevToken')))
