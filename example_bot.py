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

@bot.command(aliases=["myprofile","mydata","me"])
async def  myProfile(ctx,howmuch="short"):
    playerchange(ctx,0,0)
    senderid=ctx.author.id
    player = chipdir+"/player"+str(senderid)+".txt"
    if(howmuch=="all"):
        with open(player,"r") as playerchip:
            chipline=playerchip.readlines()
            chips=int(chipline[0])
            wonchips=int(chipline[1])
            lostchips=int(chipline[2])
            totwin=int(chipline[3])
            totdraw=int(chipline[4])
            totlose=int(chipline[5])
            rpswin=int(chipline[6])
            rpsdraw=int(chipline[7])
            rpslose=int(chipline[8])
            jackwin=int(chipline[9])
            jackdraw=int(chipline[10])
            jacklose=int(chipline[11])
            slotwin=int(chipline[12])
            slotdraw=int(chipline[13])
            slotlose=int(chipline[14])
            bacwin=int(chipline[15])
            bacdraw=int(chipline[16])
            baclose=int(chipline[17])
        embed = discord.Embed(title="**"+str(ctx.author)+"**", description="", color=0x009900)
        embed.add_field(name="현재 칩 수", value="**{}**".format(chips), inline=False)
        embed.add_field(name="얻거나 잃은 칩 수", value="{}개의 칩을 따고 {}개의 칩을 잃음".format(wonchips,lostchips), inline=False)
        embed.add_field(name="전체 전적", value="{}승 {}패 {}무".format(totwin,totlose,totdraw), inline=False)
        if(totwin+totlose+totdraw==0):
            embed.add_field(name="전체 승률", value="아직 플레이한 게임이 없습니다.", inline=False)
        else:
            embed.add_field(name="전체 승률", value="{0:5.2f}%".format(100*totwin/(totwin+totlose+totdraw)), inline=False)
        embed.add_field(name="가위바위보 전적", value="{}승 {}패 {}무".format(rpswin,rpslose,rpsdraw), inline=False)
        if(rpswin+rpslose+rpsdraw==0):
            embed.add_field(name="가위바위보 승률", value="아직 플레이한 게임이 없습니다.", inline=False)
        else:
            embed.add_field(name="가위바위보 승률", value="{0:5.2f}%".format(100*rpswin/(rpswin+rpslose+rpsdraw)), inline=False)
        embed.add_field(name="블랙잭 전적", value="{}승 {}패 {}무".format(jackwin,jacklose,jackdraw), inline=False)
        if(jackwin+jacklose+jackdraw==0):
            embed.add_field(name="블랙잭 승률", value="아직 플레이한 게임이 없습니다.", inline=False)
        else:
            embed.add_field(name="블랙잭 승률", value="{0:5.2f}%".format(100*jackwin/(jackwin+jacklose+jackdraw)), inline=False)
        embed.add_field(name="슬롯머신 전적", value="{}승 {}패 {}무".format(slotwin,slotlose,slotdraw), inline=False)
        if(slotwin+slotlose+slotdraw==0):
            embed.add_field(name="슬롯머신 승률", value="아직 플레이한 게임이 없습니다.", inline=False)
        else:
            embed.add_field(name="슬롯머신 승률", value="{0:5.2f}%".format(100*slotwin/(slotwin+slotlose+slotdraw)), inline=False)
        embed.add_field(name="바카라 전적", value="{}승 {}패 {}무".format(bacwin,baclose,bacdraw), inline=False)
        if(bacwin+baclose+bacdraw==0):
            embed.add_field(name="바카라 승률", value="아직 플레이한 게임이 없습니다.", inline=False)
        else:
            embed.add_field(name="바카라 승률", value="{0:5.2f}%".format(100*bacwin/(bacwin+baclose+bacdraw)), inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)
    else:
        with open(player,"r") as playerchip:
            chipline=playerchip.readlines()
            chips=int(chipline[0])
            wonchips=int(chipline[1])
            lostchips=int(chipline[2])
            totwin=int(chipline[3])
            totdraw=int(chipline[4])
            totlose=int(chipline[5])
        embed = discord.Embed(title="**"+str(ctx.author)+"**", description="", color=0x009900)
        embed.add_field(name="현재 칩 수", value="**{}**".format(chips), inline=False)
        embed.add_field(name="얻거나 잃은 칩 수", value="{}개의 칩을 따고 {}개의 칩을 잃음".format(wonchips,lostchips), inline=False)
        embed.add_field(name="전적", value="{}승 {}패 {}무".format(totwin,totlose,totdraw), inline=False)
        if(totwin+totlose+totdraw==0):
            embed.add_field(name="승률", value="아직 플레이한 게임이 없습니다.", inline=False)
        else:
            embed.add_field(name="승률", value="{}% \n자세한 정보는 !me all".format(100*totwin/(totwin+totlose+totdraw)), inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

@bot.command(aliases=["help","도움말"])
async def Help(ctx,myung="all"):
    if(myung=="all" or myung=="help" or myung=="도움말" or myung=="Help"):
        embed=discord.Embed(title="명령어 목록", description="모든 명령어는 !명령어 형태로, (괄호)안 내용은 필수가 아닙니다.", color=0x00aaaa)
        embed.set_author(name="카지노 봇")
        embed.add_field(name="!help\n!도움말", value="명령어 목록을 알려줍니다. !help (명령어)로 특정 명령어나 게임의 자세한 정보를 알 수 있습니다.", inline=False)
        embed.add_field(name="!myProfile\n!myprofile\n!mydata\n!me", value="플레이어 본인의 정보를 보여줍니다.", inline=False)
        embed.add_field(name="!myChip\n!mychip\n!chip", value="플레이어 본인의 칩 수만을 보여줍니다.", inline=False)
        embed.add_field(name="!addChip (칩 수)\n!addchip (칩 수)\n!add (칩 수)", value="(칩 수)만큼 칩을 추가합니다. 기본값은 100입니다.", inline=False)
        embed.add_field(name="!RockPaperSissors (칩 수)\n!rps (칩 수) \n!가위바위보 (칩 수)", value="테스트용 게임. 칩을 걸고 가위바위보를 합니다.  칩은 1~10개 사이이며,기본값은 1입니다.", inline=False)
        embed.add_field(name="!BlackJack (칩 수)\n!블랙잭 (칩 수)\n!blackjack (칩 수)\n!21 (칩 수)", value="칩을 걸고 블랙잭 게임을 진행합니다. 칩은 10~1000개 사이이며, 기본값은 10입니다.", inline=False)
        embed.add_field(name="!SlotMachine (칩 수)\n!slot (칩 수)\n!슬롯머신 (칩 수)", value="칩을 걸고 슬롯머신을 가동합니다. 칩은 10~500개 사이이며, 기본값은 10입니다.", inline=False)
        embed.add_field(name="!Baccarat \n!바카라 \n!baccarat \n!bac \n!macau ", value="바카라 게임을 진행합니다", inline=False)
        await ctx.channel.send(embed=embed)
        return
    elif(myung=="myProfile" or myung=="myprofile" or myung=="mydata" or myung=="me"):
        embed=discord.Embed(title="myProfile (길이)", description="플레이어의 칩, 승패, 승률 정보를 보여줍니다. \n!myprofile !mydata !me 로도 사용할 수 있습니다.\n 명령어 뒤 (길이)에 all을 붙여 자세한 정보를 볼 수 있습니다.", color=0x00aaaa)
        embed.set_author(name="카지노 봇")
        await ctx.channel.send(embed=embed)
        return
    elif(myung=="myChip" or myung=="mychip" or myung=="chip"):
        embed=discord.Embed(title="myChip", description="플레이어의 칩 수를 보여줍니다.\n!mychip !chip 으로도 사용할 수 있습니다.\n 칩을 한 번도 쓰지 않은 경우 100개의 chip이 생성됩니다.", color=0x00aaaa)
        embed.set_author(name="카지노 봇")
        await ctx.channel.send(embed=embed)
        return
    elif(myung=="addChip" or myung=="addchip" or myung=="add"):
        embed=discord.Embed(title="addChip (칩 수)", description="플레이어의 칩 수를 추가합니다.\n!addchip !add 로도 사용할 수 있습니다.\n 칩의 수를 지정하지 않으면 100개가 추가되며, 음수를 넣어도 정상 동작합니다.\n이것으로 변경한 칩은 게임으로 잃거나 얻은 칩에 포함되지 않습니다.", color=0x00aaaa)
        embed.set_author(name="카지노 봇")
        await ctx.channel.send(embed=embed)
        return
    elif(myung=="RockPaperSissors" or myung=="가위바위보" or myung=="rps"):
        embed=discord.Embed(title="RockPaperSissors (칩 수)", description="칩을 걸고 딜러와 가위바위보를 진행합니다.\n!가위바위보 !rps 로도 사용할 수 있습니다.\n 칩의 수를 지정하지 않으면 1개를 걸고 진행하며 이경우 승리시 1개를 얻고 패배시 1개를 잃습니다.\n 칩은 1~100개를 걸 수 있습니다.", color=0x00aaaa)
        embed.set_author(name="카지노 봇")
        await ctx.channel.send(embed=embed)
        return
    elif(myung=="BlackJack" or myung=="blackjack" or myung=="블랙잭" or myung=="21"):
        embed=discord.Embed(title="BlackJack (칩 수)", description="일정량의 칩을 베팅해 그만 둘 때 까지 딜러와 블랙잭 게임을 진행합니다.\n!blackjack !블랙잭 !21 로도 사용할 수 있습니다.\n블랙잭은 카드를 뽑아 21에 가깝게 만드는 게임으로, hit으로 카드를 뽑고 stay로 중단할 수 있습니다. \n 10, J, Q, K를 모두 10으로, A를 11 혹은 1로 계산한 카드 숫자의 합이 점수이며, 점수가 21을 초과하면 상대가 승리합니다.\n\n 칩의 수를 지정하지 않으면 10개를 걸고 진행하며 이경우 일반적인 승리시 20개, 블랙잭으로 승리시 30개를 얻고 패배시 10개를 잃습니다.\n칩은 10~1000개를 걸 수 있습니다.", color=0x00aaaa)
        embed.set_author(name="카지노 봇")
        await ctx.channel.send(embed=embed)
        return
    elif(myung=="SlotMachine" or myung=="slot" or myung=="슬롯머신"):
        embed=discord.Embed(title="SlotMachine (칩 수)", description="칩을 넣고 슬롯머신을 가동합니다.\n!슬롯머신 !slot 으로도 사용할 수 있습니다.\n슬롯머신은 3x3의 아이콘 배열 중 2행의 세 심볼을 분석합니다. 조건에 부합하면 칩을 받고, 그렇지 않으면 잃습니다.\n\n규칙은 다음과 같습니다\n :seven: - :seven: - :seven: 건 칩의 200배, :slot_machine: - :slot_machine: - :slot_machine: 건 칩의 100배\n :watermelon: - :watermelon: - :watermelon: 건 칩의 100배, :watermelon: - :watermelon: - :slot_machine: 건 칩의 100배\n :bell: - :bell: - :bell: 건 칩의 18배, :bell: - :bell: - :slot_machine: 건 칩의 18배\n :grapes: - :grapes: - :grapes: 건 칩의 14배, :grapes: - :grapes: - :slot_machine: 건 칩의 14배\n :tangerine: - :tangerine: - :grapes: 건 칩의 10배, :grapes: - :grapes: - :slot_machine: 건 칩의 10배\n:cherries: - :cherries: - :question: 건 칩의 5배, :cherries: - :question: - :question: 건 칩의 2배\n 항목에 포함되지 않으면 칩을 잃는다.", color=0x00aaaa)
        embed.set_author(name="카지노 봇")
        await ctx.channel.send(embed=embed)
        return
    elif(myung=="바카라" or myung=="Baccarat" or myung=="baccarat" or myung=="bac" or myung=="macau"):
        embed=discord.Embed(title="Baccarat", description="플레이어, 뱅커(딜러) 중 어느 쪽이 이길 지, 혹은 무승부일 지 예측해 베팅하고 결과에 따라 칩을 받는 게임입니다.\n A는 1로, 10, J, Q, K를 모두 0로 계산하며, 카드의 점수 합에서 일의 자리를 비교해 더 높은 쪽이 승리합니다.\n바카라는 양측이 카드를 2장씩 뽑아 비교하며, 규칙에 따라 한장이 더 추가됩니다. \n예측에 성공하면 베팅한 칩의 두배를, tie에 베팅했으면 8배를 받으며, banker가 6으로 승리하면 1.5배를 받습니다.", color=0x00aaaa)
        embed.set_author(name="카지노 봇")
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
            playerchip.write("100\n"+"0\n"*17)

@bot.command(aliases=["mychip","chip"])
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

@bot.command(aliases=["addchip","add"])
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
        if(wants<1 or wants>100):
            embed = discord.Embed(title="가위바위보 RockPaperSissors",description="\n칩은 1개~100개 사이로 베팅해주세요.", color=0x00aaaa)
            await ctx.channel.send(embed=embed)
            return
        if(wants<1 or int(chips)-wants<0):
            answer = ctx.author.name+"씨의 칩은 "+chips.rstrip('\n')+"개 입니다."
            embed = discord.Embed(title="칩이 부족합니다.",description=answer+"\n칩은 음수가 될 수 없습니다.", color=0x00aaaa)
            await ctx.channel.send(embed=embed)
            return
    rps = ["가위","바위","보"]
    embed = discord.Embed(title="가위바위보",description=ctx.author.name+"님\n가위, 바위, 보 중 하나를 5초 안에 내주세요!\nㄱㅇ, ㅂㅇ, ㅂ 혹은 s, r, p의 축약형도 가능합니다.", color=0x00aaaa)
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
        if(user_rps=="ㄱㅇ" or user_rps=="s"):
            user_rps = "가위"
        elif(user_rps=="ㅂㅇ" or user_rps=="r"):
            user_rps = "바위"
        elif(user_rps=="ㅂ" or user_rps=="p"):
            user_rps = "보"
        answer = ""
        if bot_rps == user_rps:
            answer = "딜러인 저는 " + bot_rps + "를 냈고, "+ctx.author.name+"씨는 " + user_rps + "를 내셨습니다.\n" + "비겼습니다.\n"
            wants=0
            result=1
        elif (bot_rps == "가위" and user_rps == "바위") or (bot_rps == "보" and user_rps == "가위") or (bot_rps == "바위" and user_rps == "보"):
            answer = "딜러인 저는 " + bot_rps + "를 냈고, "+ctx.author.name+"씨는 " + user_rps + "를 내셨습니다.\n" + "승리하셨습니다. 칩 "+str(wants)+"개를 획득하셨습니다.\n"
            result=0
        elif (bot_rps == "바위" and user_rps == "가위") or (bot_rps == "가위" and user_rps == "보") or (bot_rps == "보" and user_rps == "바위"):
            answer = "딜러인 저는 " + bot_rps + "를 냈고, "+ctx.author.name+"씨는 " + user_rps + "를 내셨습니다.\n" + "패배하셨습니다. 칩 "+str(wants)+"개를 잃으셨습니다.\n"
            wants=-wants
            result=2
        else:
            embed = discord.Embed(title="가위바위보",description="가위, 바위, 보 중에서만 내셔야 합니다.\nㄱㅇ, ㅂㅇ, ㅂ 혹은 s, r, p의 축약형도 가능합니다", color=0x00aaaa)
            await ctx.channel.send(embed=embed)
            return
        embed = discord.Embed(title="가위바위보",description=answer, color=0x00aaaa)
        playerchange(ctx,wants,0)
        if wants>0:
            playerchange(ctx,wants,1)
        else:
            playerchange(ctx,-wants,2)
        playerchange(ctx,1,result+3)
        playerchange(ctx,1,result+6)
        await ctx.channel.send(embed=embed)
        with open(player+".txt","r") as playerchip:
            chipline=playerchip.readlines()
            chips=chipline[0]
            await ctx.channel.send("{} 씨가 소지하고 있는 칩은 총 **{}**개 입니다!".format(ctx.author.name, chips.rstrip('\n')))
        return

@bot.command(aliases=["블랙잭","blackjack","21"])
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
                embed = discord.Embed(title="블랙잭 Blackjack",description="\n칩은 10개~1000개 사이로 베팅해주세요.", color=0x00aaaa)
                await ctx.channel.send(embed=embed)
                return
            if(wants<1 or int(chips)-wants<0):
                answer = ctx.author.name+"씨의 칩은 "+chips.rstrip('\n')+"개 입니다."
                embed = discord.Embed(title="칩이 부족합니다.",description=answer+"\n칩은 음수가 될 수 없습니다.", color=0x00aaaa)
                await ctx.channel.send(embed=embed)
                return
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
            earn=-wants
            result=2
        elif score_player == 9999 and score_dealer < score_player:
            answer = answer + "블랙잭! 승리하셨습니다!"
            earn = wants+wants//2
            result=0
        elif score_dealer == 0:
            answer = answer + "딜러 버스트로 승리하셨습니다!"
            earn= wants
            result=0
        elif score_dealer == score_player:
            answer = answer + "비겼습니다"
            earn=0
            result=1
        elif score_dealer < score_player:
            answer = answer + "승리하셨습니다!"
            earn=wants
            result=0
        else:
            answer = answer + "패배하셨습니다."
            earn=-wants
            result=2
        playerchange(ctx,earn,0)
        if earn>0:
            playerchange(ctx,earn,1)
        else:
            playerchange(ctx,-earn,2)
        playerchange(ctx,1,result+3)
        playerchange(ctx,1,result+9)
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

@bot.command(aliases=["슬롯머신","slot"])
async def SlotMachine(ctx,wants=10):
    def checksame(newtext):
        return newtext.author == ctx.author and newtext.channel == channel
    senderid=ctx.author.id
    sendername = chipdir+"/player"+str(senderid)
    channel = ctx.channel
    with open(sendername+".txt","r+") as playerchip:
        chipline=playerchip.readlines()
        chips=chipline[0]
        if(wants<10 or wants>500):
            embed = discord.Embed(title="슬롯머신 SlotMachine",description="\n칩은 10개~500개 사이로 베팅해주세요.", color=0x00aaaa)
            await ctx.channel.send(embed=embed)
            return
        if(wants<1 or int(chips)-wants<0):
            answer = ctx.author.name+"씨의 칩은 "+chips.rstrip('\n')+"개 입니다."
            embed = discord.Embed(title="칩이 부족합니다.",description=answer+"\n칩은 음수가 될 수 없습니다.", color=0x00aaaa)
            await ctx.channel.send(embed=embed)
            return
    while(True):
        slot1=[":grapes:",":slot_machine:",":tangerine:",":grapes:",":slot_machine:",":watermelon:",":grapes:",":bell:",":grapes:",":seven:",":grapes:",":cherries:",":grapes:",":tangerine:",":watermelon:",":tangerine:",":grapes:",":slot_machine:",":tangerine:",":tangerine:",":cherries:"]
        slot2=[":slot_machine:",":bell:",":cherries:",":watermelon:",":tangerine:",":grapes:",":bell:",":tangerine:",":bell:",":seven:",":watermelon:",":cherries:",":grapes:",":cherries:",":grapes:",":tangerine:",":slot_machine:",":bell:",":tangerine:",":cherries:",":bell:",":cherries:",":tangerine:",":cherries:"]
        slot3=[":grapes:",":slot_machine:",":bell:",":watermelon:",":bell:",":bell:",":tangerine:",":lemon:",":grapes:",":bell:",":tangerine:",":bell:",":lemon:",":bell:",":tangerine:",":lemon:",":bell:",":seven:",":bell:",":grapes:",":watermelon:",":tangerine:",":lemon:"]
        num1 = random.randint(0,20) 
        num2 = random.randint(0,23) 
        num3 = random.randint(0,22)
        bedang = -1
        resu = [slot1[num1%21],slot1[(num1+1)%21],slot1[(num1+2)%21],slot2[num2%24],slot2[(num2+1)%24],slot2[(num2+2)%24],slot3[num3%23],slot3[(num3+1)%23],slot3[(num3+2)%23]]
        if(resu[1]==resu[4] and resu[4]==resu[7]):
            if(resu[1]==":seven:"):
                bedang = 200-1
            elif(resu[1]==":slot_machine:"):
                bedang = 100-1
            elif(resu[1]==":watermelon:"):
                bedang = 100-1
            elif(resu[1]==":bell:"):
                bedang = 18-1
            elif(resu[1]==":grapes:"):
                bedang = 14-1
            elif(resu[1]==":tangerine:"):
                bedang = 10-1
        elif(resu[1]==resu[4] and resu[7]=="slot_machine"):
            if(resu[1]==":watermelon:"):
                bedang = 100-1
            elif(resu[1]==":bell:"):
                bedang = 18-1
            elif(resu[1]==":grapes:"):
                bedang = 14-1
            elif(resu[1]==":tangerine:"):
                bedang = 10-1
        elif(resu[1]==":cherries:"):
            if(resu[4]==":cherries:"):
                bedang = 5-1
            else:
                bedang = 2-1
        result = "7777777777 \n"+resu[0]+" - "+resu[3]+" - "+resu[6]+"\n"+resu[1]+" - "+resu[4]+" - "+resu[7]+" <-\n"+resu[2]+" - "+resu[5]+" - "+resu[8]+"\n7777777777 \n"
        if(bedang==201):
            winlose = "\n[ - - JACKPOT! - - ]"
            ton=0
            playerchange(ctx,wants*bedang,1)
        elif(bedang>0):
            winlose = "\n[ - - YOU WON! - - ]"
            ton=0
            playerchange(ctx,wants*bedang,1)
        else:
            winlose = "\n[ - - YOU LOSE - - ]"
            ton=2
            playerchange(ctx,-wants*bedang,2)
        playerchange(ctx,wants*bedang,0)
        playerchange(ctx,1,ton+3)
        playerchange(ctx,1,ton+12)
        with open(sendername+".txt","r") as playerchip:
            chipline=playerchip.readlines()
            chips=chipline[0]
        embed = discord.Embed(title="SlotMachine 슬롯머신", description=result+winlose, color=0x00aaaa)
        await ctx.channel.send(embed=embed)
        await ctx.channel.send("{} 씨가 소지하고 있는 칩은 총 **{}**개 입니다!".format(ctx.author.name, chips.rstrip('\n')))
        await ctx.channel.send("다시 하시고 싶으시면 Y(혹은 y)를, 아니면 N(혹은 n)을 입력해주세요.\n 제한시간: 10초")
        try:
            msg2 = await bot.wait_for('message', timeout=10.0, check=checksame)
            while(msg2.content!="Y" and msg2.content!="N" and msg2.content!="y" and msg2.content!="n"):
                await ctx.channel.send("다시 하시고 싶으시면 Y(혹은 y)를, 아니면 N(혹은 n)을 입력해주세요.\n 제한시간: 10초")
                msg2 = await bot.wait_for('message', timeout=40.0, check=checksame)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="슬롯머신",description="10초가 다 지나 게임을 종료합니다.", color=0x00aaaa)
            await ctx.channel.send(embed=embed)
            return
        if msg2.content=="N" or msg2.content=="n":
            break
        with open(sendername+".txt","r+") as playerchip:
            chipline=playerchip.readlines()
            chips=chipline[0]
            if(wants<10 or wants>500):
                embed = discord.Embed(title="슬롯머신 SlotMachine",description="\n칩은 10개~500개 사이로 베팅해주세요.", color=0x00aaaa)
                await ctx.channel.send(embed=embed)
                return
            if(wants<1 or int(chips)-wants<0):
                answer = ctx.channel.send(ctx.author.name+"씨의 칩은 "+chips.rstrip('\n')+"개 입니다.")
                embed = discord.Embed(title="칩이 부족합니다.",description=answer+"\n칩은 음수가 될 수 없습니다.", color=0x00aaaa)
                await ctx.channel.send(embed=embed)
                return
    return

@bot.command(aliases=["바카라","baccarat","macau","bac"])
async def Baccarat(ctx,wants=10):
    def checksame(newtext):
        return newtext.author == ctx.author and newtext.channel == channel
    senderid=ctx.author.id
    sendername = chipdir+"/player"+str(senderid)
    channel = ctx.channel
    deck = fresh_deck()
    while True:
        embed = discord.Embed(title="바카라",description="40초 안에 banker, player, tie 중 베팅할 곳을 선택 해주세요. ", color=0x00aaaa)
        msg1 =await ctx.channel.send(embed=embed)
        try:
            msg2 = await bot.wait_for('message', timeout=40.0, check=checksame)
            while(msg2.content!="banker" and msg2.content!="player" and msg2.content!="tie"):
                await ctx.channel.send(" banker, player, tie 중 베팅할 곳을 선택 해주세요.")
                msg2 = await bot.wait_for('message', timeout=40.0, check=checksame)
            mypick = msg2.content
        except asyncio.TimeoutError:
            await msg1.delete()
            embed = discord.Embed(title="Baccarat",description="40초가 다 지나 항복으로 간주합니다.", color=0x00aaaa)
            await ctx.channel.send(embed=embed)
            return  
        with open(sendername+".txt","r+") as playerchip:
            chipline=playerchip.readlines()
            chips=chipline[0]
            if int(chips)<=0 :
                answer = ctx.author.name+"씨의 칩은 "+chips.rstrip('\n')+"개 입니다."
                embed = discord.Embed(title="칩이 부족합니다.",description=answer, color=0x00aaaa)
                await ctx.channel.send(embed=embed)
                return
            embed = discord.Embed(title="바카라",description="40초 안에 베팅할 칩의 양을 정해주세요.\n 현재 "+ctx.author.name+"씨의 칩은 "+chips.rstrip('\n')+"개 입니다.", color=0x00aaaa)
            msg1 =await ctx.channel.send(embed=embed)
            try:
                while True:
                    await ctx.channel.send("베팅할 칩의 양을 제대로 정해주세요. 양수가 아니거나, 칩이 부족하면 실행할 수 없습니다.")
                    msg2 = await bot.wait_for('message', timeout=40.0, check=checksame)
                    try:
                        wants = int(msg2.content)
                        if(wants>=1 and wants<=1000 and int(chips)-wants>=0):
                            break
                    except:
                        pass
            except asyncio.TimeoutError:
                await msg1.delete()
                embed = discord.Embed(title="블랙잭",description="40초가 다 지나 게임을 종료합니다.", color=0x00aaaa)
                await ctx.channel.send(embed=embed)
                return
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
        score_dealer = count_baccarat(dealer)
        score_player = count_baccarat(player)
        if score_player>=8 or score_dealer>=8:
            pass
        elif score_player>=6:
            if score_dealer<=5:
                card, deck = hit(deck)
                dealer.append(card)
        else:
            card, deck = hit(deck)
            player.append(card)
            if player[2][1]==2 or player[2][1]==3:
                if score_dealer <=4:
                    card, deck = hit(deck)
                    dealer.append(card)
            elif player[2][1]==4 or player[2][1]==5:
                if score_dealer <=5:
                    card, deck = hit(deck)
                    dealer.append(card)
            elif player[2][1]==6 or player[2][1]==7:
                if score_dealer <=6:
                    card, deck = hit(deck)
                    dealer.append(card)
            elif player[2][1]==8:
                if score_dealer <=2:
                    card, deck = hit(deck)
                    dealer.append(card)
            else: #A 9 10 J Q K
                if score_dealer <=3:
                    card, deck = hit(deck)
                    dealer.append(card)
        dealstr2 = show_cards(dealer, "딜러인 저의 덱은 ")
        playstr2 = show_cards(player,f"{ctx.message.author.mention}님의 덱은")
        answer = dealstr2+'\n\n'+playstr2+f"\n\n{ctx.message.author.mention}님은 승자 예측을 다음과 같이 하셨습니다:\n"+mypick+'\n\n'
        await msg1.delete()
        if score_dealer == score_player:
            answer = answer + "비겼습니다. "
            win="tie"
            bedang=8
        elif score_dealer < score_player:
            answer = answer + "플레이어의 승입니다. "
            win="player"
            bedang=1
        else:
            answer = answer + "딜러의 승입니다. "
            win="banker"
            bedang=1
        if mypick==win:
            if(win=="dealer" and score_dealer==6):
                playerchange(ctx,wants//2,0)
                playerchange(ctx,wants//2,1)
                
            else:
                playerchange(ctx,bedang*wants,0)
                playerchange(ctx,bedang*wants,1)
            result=0
            answer = answer + "예측에 성공하셨습니다!"
        else:
            answer = answer + "예측에 실패하셨습니다."
            playerchange(ctx,-wants,0)
            playerchange(ctx,wants,2)
            result=2
        playerchange(ctx,1,result+3)
        playerchange(ctx,1,result+15)
        with open(sendername+".txt","r") as playerchip:
            chipline=playerchip.readlines()
            chips=chipline[0]
        embed = discord.Embed(title="바카라",description=answer+'\n'+ctx.author.name+"씨의 칩은 "+chips.rstrip('\n')+"개 입니다. \n\n 다시 하시고 싶으시면 Y(혹은 y)를, 아니면 N(혹은 n)을 입력해주세요.", color=0x00aaaa)
        embed.set_footer(text="40초 안에 입력하시지 않으면 자동으로 종료 처리됩니다.")
        msg1 = await ctx.channel.send(embed=embed)
        try:
            msg2 = await bot.wait_for('message', timeout=40.0, check=checksame)
            while(msg2.content!="Y" and msg2.content!="N" and msg2.content!="y" and msg2.content!="n"):
                await ctx.channel.send("다시 하시고 싶으시면 Y(혹은 y)를, 아니면 N(혹은 n)을 입력해주세요.")
                msg2 = await bot.wait_for('message', timeout=40.0, check=checksame)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="바카라",description="40초가 다 지나 게임을 종료합니다.", color=0x00aaaa)
            await ctx.channel.send(embed=embed)
            return
        if msg2.content=="N" or msg2.content=="n":
            break
    return

bot.run('my token')
