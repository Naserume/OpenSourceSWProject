import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
chipdir = "./saved"

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

@bot.command()
async def addChip(ctx,wants=100):
    if not os.path.isdir(chipdir):
        os.mkdir(chipdir)
    senderid=ctx.author.id
    player=chipdir+"/player"+str(senderid)
    try:
        with open(player+".txt","r") as playerchip:
            chip=int(playerchip.read())
            print(chip)
        with open(player+".txt","w") as playerchip:
            chip = chip+wants
            print(chip)
            playerchip.write(str(chip))
    except FileNotFoundError:
        with open(player+".txt","w") as playerchip:
            playerchip.write("100")
    with open(player+".txt","r") as playerchip:
        await ctx.channel.send(ctx.author.name+"씨의 칩은 "+playerchip.read()+"개")

bot.run('my token')
