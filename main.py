import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import locale_str as _
import os
import asyncio
from typing import Literal,Optional
import json





MY_GUILD = discord.Object(id=my_guild_id) 


class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='$',
            intents=discord.Intents.all())


    async def load_cogs(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await client.load_extension(f'cogs.{filename[:-3]}')

    async def setup_hook(self):
        await self.load_cogs()
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        await self.tree.sync()     

intents = discord.Intents.default()
client = MyClient()
@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.command()
async def load(ctx,file,extension):
  await client.load_extension(f'{file}.{extension}')
  await ctx.send(f'加载{extension}成功')

@client.command()
async def unload(ctx,file,extension):
  await client.unload_extension(f'{file}.{extension}')
  await ctx.send(f'卸載{extension}成功')

@client.command()
async def reload(ctx,file,extension):
  await client.reload_extension(f'{file}.{extension}')
  await ctx.send(f'重新加载{extension}成功')


@client.command()
@commands.guild_only()
# @commands.is_owner()
async def sync(
  ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


client.run('TOKEN')