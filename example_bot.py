import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    print("Discord bot ID is "+str(bot.user.id))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('카지노 일'))

@bot.command(aliases=["Hello","hello!","Hello!","hi","Hi","hi!","Hi!"])
async def hello(ctx):
    
    await ctx.channel.send("Hello!")

@bot.command()
async def embed(ctx):
    embed=discord.Embed(title="Embed", description="Embed 내용.", color=0x00aaaa)
    embed.set_author(name="작성자의 이름")
    embed.add_field(name="이것은 field1입니다.", value="이것은 field1 값입니다.", inline=False)
    embed.add_field(name="이것은 field2입니다.", value="이것은 field2 값입니다.", inline=False)
    embed.add_field(name="이것은 field3입니다.", value="이것은 field3 값입니다.", inline=False)
    embed.add_field(name="이것은 field4입니다.", value="이것은 field4 값입니다.", inline=False)
    embed.set_footer(text="이것은 footer의 값입니다.")
    await ctx.channel.send(embed=embed)

bot.run('my token')
