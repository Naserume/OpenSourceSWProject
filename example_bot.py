import discord
import asyncio
import os
from cardgame import *
from discord.ext import commands
import random

bot = commands.Bot(command_prefix='!',help_command=None)
chipdir = "./saved"

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    print("Discord bot ID is "+str(bot.user.id))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('!help 카지노 일'))

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

@bot.command(aliases=["help"])
async def Help(ctx):
    embed=discord.Embed(title="명령어 목록", description="모든 명령어는 !(명령어) 형태", color=0x00aaaa)
    embed.set_author(name="카지노 봇")
    embed.add_field(name="!help", value="명령어 목록을 알려줍니다", inline=False)
    embed.add_field(name="!addChip (숫자)", value="(숫자)만큼 칩을 추가합니다. 값이 없으면 100개", inline=False)
    embed.add_field(name="!가위바위보 (숫자)", value="테스트용 게임. 칩을 걸고 가위바위보를 합니다. 기본값은 1개", inline=False)
    embed.add_field(name="!myChip", value="플레이어의 칩 수를 보여줍니다.", inline=False)
    embed.set_footer(text="footer는 아직 어떻게 쓸지 모른다.")
    await ctx.channel.send(embed=embed)

def playerchange(ctx,want,locate):
    if not os.path.isdir(chipdir):
        os.mkdir(chipdir)
    senderid=ctx.author.id
    player = chipdir+"/player"+str(senderid)+".txt"
    try:
        with open(player,"r") as playerchip:
            chipline=playerchip.readlines()
            chip=int(chipline[locate])
            #print(chip)
        with open(player,"w") as playerchip:
            chip = chip+want
            print(chip)
            chipline[locate]=str(chip)+'\n'
            playerchip.writelines(chipline)
    except FileNotFoundError:
        with open(player,"w") as playerchip:
            playerchip.write("100\n0\n0\n0\n")

@bot.command(aliases=["mychip"])
async def myChip(ctx):
    playerchange(ctx,0,0)
    senderid=ctx.author.id
    player = chipdir+"/player"+str(senderid)+".txt"
    with open(player,"r") as playerchip:
        chipline=playerchip.readlines()
        chips=chipline[0]
        await ctx.send(f"{ctx.message.author.mention}님의 칩은"+chips.rstrip('\n')+"개 입니다.")
        #try:
        #    await bot.get_user(ctx.author.id).send("당신의 카드는 어쩌고저쩌고")
        #except discord.errors.Forbidden:
        #    await ctx.channel.send(ctx.author.name+"씨의 칩은 "+chips.rstrip('\n')+"개")
        #    await ctx.send(f"{ctx.message.author.mention}님 서버 이름 클릭 - 개인정보 보호 설정 - 서버 멤버가 보내는 개인 메시지 허용해주세요.")
        #    요게 개인에게 직접 메시지 보내는 법이다.

@bot.command(aliases=["addchip"])
async def addChip(ctx,wants=100):
    playerchange(ctx,wants,0)
    senderid=ctx.author.id
    player = chipdir+"/player"+str(senderid)
    with open(player+".txt","r") as playerchip:
        chipline=playerchip.readlines()
        chips=chipline[0]
        await ctx.send(f"{ctx.message.author.mention}님의 칩은"+chips.rstrip('\n')+"개 입니다.")

@bot.command(aliases=["가위바위보","rps"])
async def RockPaperSissors(ctx,wants=1):
    senderid=ctx.author.id
    player = chipdir+"/player"+str(senderid)
    with open(player+".txt","r") as playerchip:
        chipline=playerchip.readlines()
        chips=chipline[0]
        if(wants<1 or int(chips)-wants<0):
            answer = ctx.channel.send(ctx.author.name+"씨의 칩은 "+chips.rstrip('\n')+"개 입니다.")
            embed = discord.Embed(title="칩이 부족합니다.",description=answer+"\n칩은 음수가 될 수 없습니다.", color=0x00aaaa)
            await ctx.channel.send(embed=embed)
            return
    rps = ["가위","바위","보"]
    embed = discord.Embed(title="가위바위보",description=ctx.author.name+"님\n가위, 바위, 보 중 하나를 5초 안에 내주세요!", color=0x00aaaa)
    senderid=ctx.author.id
    channel = ctx.channel
    msg1 =await ctx.channel.send(embed=embed)
    def checksame(newtext):
        return newtext.author == ctx.author and newtext.channel == channel
    try:
        msg2 = await bot.wait_for('message', timeout=5.0, check=checksame)
    except asyncio.TimeoutError:
        await msg1.delete()
        embed = discord.Embed(title="가위바위보",description="5초가 다 지났어요!", color=0x00aaaa)
        await ctx.channel.send(embed=embed)
        return
    else:
        await msg1.delete()
        bot_rps = str(random.choice(rps))
        user_rps  = str(msg2.content)
        answer = ""
        if bot_rps == user_rps:
            answer = "딜러인 저는 " + bot_rps + "를 냈고, "+ctx.author.name+"씨는 " + user_rps + "를 내셨습니다.\n" + "비겼습니다.\n"
            wants=0
            result=2
        elif (bot_rps == "가위" and user_rps == "바위") or (bot_rps == "보" and user_rps == "가위") or (bot_rps == "바위" and user_rps == "보"):
            answer = "딜러인 저는 " + bot_rps + "를 냈고, "+ctx.author.name+"씨는 " + user_rps + "를 내셨습니다.\n" + "승리하셨습니다. 칩 "+str(wants)+"개를 획득하셨습니다.\n"
            result=1
        elif (bot_rps == "바위" and user_rps == "가위") or (bot_rps == "가위" and user_rps == "보") or (bot_rps == "보" and user_rps == "바위"):
            answer = "딜러인 저는 " + bot_rps + "를 냈고, "+ctx.author.name+"씨는 " + user_rps + "를 내셨습니다.\n" + "패배하셨습니다. 칩 "+str(wants)+"개를 잃으셨습니다.\n"
            wants=-wants
            result=3
        else:
            embed = discord.Embed(title="가위바위보",description="가위, 바위, 보 중에서만 내셔야 합니다.", color=0x00aaaa)
            await ctx.channel.send(embed=embed)
            return
        embed = discord.Embed(title="가위바위보",description=answer, color=0x00aaaa)
        playerchange(ctx,wants,0)
        await ctx.channel.send(embed=embed)
        playerchange(ctx,1,result)
        with open(player+".txt","r") as playerchip:
            chipline=playerchip.readlines()
            chips=chipline[0]
            await ctx.channel.send(ctx.author.name+"씨의 칩은 "+chips.rstrip('\n')+"개")
        return

@bot.command(aliases=["블랙잭","blackjack"])
async def BlackJack(ctx,wants=10):
    def checksame(newtext):
        return newtext.author == ctx.author and newtext.channel == channel
    senderid=ctx.author.id
    sendername = chipdir+"/player"+str(senderid)
    deck = fresh_deck()
    while True:
        with open(sendername+".txt","r+") as playerchip:
            chipline=playerchip.readlines()
            chips=chipline[0]
            if(wants<10 or wants>1000):
                embed = discord.Embed(title="블랙잭 Blackjack",description=answer+"\n칩은 10개~1000개 사이로 베팅해주세요.", color=0x00aaaa)
                await ctx.channel.send(embed=embed)
                return
            if(wants<1 or int(chips)-wants<0):
                answer = ctx.channel.send(ctx.author.name+"씨의 칩은 "+chips.rstrip('\n')+"개 입니다.")
                embed = discord.Embed(title="칩이 부족합니다.",description=answer+"\n칩은 음수가 될 수 없습니다.", color=0x00aaaa)
                await ctx.channel.send(embed=embed)
                return
            playerchange(ctx,-wants,0)
            chips=int(chips)-wants
            await ctx.channel.send(ctx.author.name+"씨의 남은 칩은 "+str(chips)+"개 입니다.")
        dealer = []
        player = []
        card, deck = hit(deck)
        player.append(card)
        card, deck = hit(deck)
        dealer.append(card)
        card, deck = hit(deck)
        player.append(card)
        card, deck = hit(deck)
        dealer.append(card)
        senderid=ctx.author.id
        channel = ctx.channel
        score_dealer = count_score(dealer)
        score_player = count_score(player)
        if score_player == 21:
            score_player=9999
        else:
            while score_player < 21 and score_player > 0:
                dealstr1 = "딜러인 저의 핸드는 \n ------- -- \n"+str(dealer[1][0])+' '+str(dealer[1][1])+"\n\n"
                playstr1 = show_cards(player,f"{ctx.message.author.mention}님의 핸드는")
                embed = discord.Embed(title="블랙잭",description=dealstr1+playstr1+"\n\n 40초 안에 hit/stay 중 하나를 선택 해주세요.", color=0x00aaaa)
                msg1 =await ctx.channel.send(embed=embed)
                try:
                    msg2 = await bot.wait_for('message', timeout=40.0, check=checksame)
                    while(msg2.content!="hit" and msg2.content!="stay"):
                        await ctx.channel.send("hit이나 stay 중 하나를 입력해주세요.")
                        msg2 = await bot.wait_for('message', timeout=40.0, check=checksame)
                    if msg2.content=="hit":
                        card, deck = hit(deck)
                        player.append(card)
                        score_player = count_score(player)
                    else:
                        break
                except asyncio.TimeoutError:
                    await msg1.delete()
                    embed = discord.Embed(title="블랙잭",description="40초가 다 지나 항복으로 간주합니다.", color=0x00aaaa)
                    await ctx.channel.send(embed=embed)
                    return
        if score_dealer == 21:
            score_dealer = 9999
        while score_dealer <= 16 and score_dealer > 0:
            card, deck = hit(deck)
            dealer.append(card)
            score_dealer = count_score(dealer)
        dealstr2 = show_cards(dealer, "딜러인 저의 핸드는 ")
        playstr2 = show_cards(player,f"{ctx.message.author.mention}님의 핸드는")
        answer = dealstr2+'\n\n'+playstr2+'\n\n'
        await msg1.delete()
        if score_player == 0:
            answer = answer + "버스트로 패배하셨습니다."
            earn=0
            result=3
        elif score_player == 9999 and score_dealer < score_player:
            answer = answer + "블랙잭! 승리하셨습니다!"
            earn = wants*2+wants//2
            result=1
        elif score_dealer == 0:
            answer = answer + "딜러 버스트로 승리하셨습니다!"
            earn=wants*2
            result=1
        elif score_dealer == score_player:
            answer = answer + "비겼습니다"
            earn=wants
            result=2
        elif score_dealer < score_player:
            answer = answer + "승리하셨습니다!"
            earn=wants*2
            result=1
        else:
            answer = answer + "패배하셨습니다."
            earn=0
            result=3
        playerchange(ctx,earn,0)
        playerchange(ctx,1,result)
        with open(sendername+".txt","r") as playerchip:
            chipline=playerchip.readlines()
            chips=chipline[0]
        embed = discord.Embed(title="블랙잭",description=answer+'\n'+ctx.author.name+"씨의 칩은 "+chips.rstrip('\n')+"개 입니다. \n\n 다시 하시고 싶으시면 Y(혹은 y)를, 아니면 N(혹은 n)을 입력해주세요.", color=0x00aaaa)
        embed.set_footer(text="40초 안에 입력하시지 않으면 자동으로 종료 처리됩니다.")
        msg1 = await ctx.channel.send(embed=embed)
        try:
            msg2 = await bot.wait_for('message', timeout=40.0, check=checksame)
            while(msg2.content!="Y" and msg2.content!="N" and msg2.content!="y" and msg2.content!="n"):
                await ctx.channel.send("다시 하시고 싶으시면 Y(혹은 y)를, 아니면 N(혹은 n)을 입력해주세요.")
                msg2 = await bot.wait_for('message', timeout=40.0, check=checksame)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="블랙잭",description="40초가 다 지나 게임을 종료합니다.", color=0x00aaaa)
            await ctx.channel.send(embed=embed)
            return
        if msg2.content=="N" or msg2.content=="n":
            break
    return

bot.run('my token')
