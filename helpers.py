import discord

EMBED_COLOR=0xFEC200

def simple_embed(title, text=''):
    embed = discord.Embed(title=title,description=text, color=EMBED_COLOR)
    return embed
