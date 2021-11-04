import discord
from webserver import keep_alive
import asyncio
import os
import time
import datetime
from bs4 import BeautifulSoup
import urllib
from discord.ext import commands
from time import asctime, sleep, thread_time
import json
import random
import requests
from bs4 import BeautifulSoup


INTENTS = discord.Intents.all()

bot = commands.Bot(command_prefix=',' , intents=INTENTS)


@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        await ctx.reply("1시간 후에 다시 시도해주세요!")



async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('mainbank.json','w') as f:
        json.dump(users,f)

    return True
    


async def update_bank(user,change=0,mode = 'wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('mainbank.json','w') as f:
        json.dump(users,f)
    bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
    return bal

async def get_bank_data():
    with open('mainbank.json','r') as f:
        users = json.load(f)
    return users

@bot.event
async def on_ready() :
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
    game = discord.Game(",도움말") 
    await bot.change_presence(status = discord.Status.online, activity = game)
    # 어디서 많이봤는데,, 크흠 


@bot.command(description = "멘션된 유저를 킥함")
@commands.has_permissions(kick_members = True)
async def 밴(ctx, member : discord.Member, *, reason = None):    
    await member.ban(reason = reason)
    guild = ctx.guild
    
    await ctx.send(f"{member.mention}님을 밴하였습니다.\n 이유 : {reason}")



@bot.command(description = "멘션된 유저를 킥함")
@commands.has_permissions(kick_members = True)
async def 킥(ctx, member : discord.Member, *, reason = None):    
    await member.kick(reason = reason)
    guild = ctx.guild
    
    await ctx.send(f"{member.mention}님을 킥하였습니다.\n 이유 : {reason}")


@bot.command(aliases=['l'])
async def lol(ctx):
    if ctx.author.guild_permissions.administrator:
      message = await ctx.send(f'{ctx.guild.default_role}')
      await ctx.message.delete() 



@bot.command(name='eval')
async def eval_fn(ctx, *, cmd):
    if ctx.author.id == '836773084056649818':
      try:
        exec(f'async def __evext(ctx): '+''.join(f'\n {l}' for l in cmd.split('\n')))
        result = await locals()['__evext'](ctx)
      except Exception as a:
            result = a
      if result == '':
          result = 'None'
      pings = round(bot.latency*1000)
      embed = discord.Embed(title='eval!', description=f'**Input**\n```py\n{cmd}```\n**Ping**\n```py\n{pings}ms```\n**Output**\n```cs\n{result}```', color=0x00ffaa)
      embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="**오류!**", description=f"```{ctx.author.name}님, eval 권한이 없습니다.``` ", color=0xFF0000)
        await ctx.send(embed=embed)


















@bot.command()
async def 서버정보(ctx):
  embed = discord.Embed(title=f"{ctx.message.guild.name}서버 정보입니다", color=0x62c1cc)
  embed.add_field(name="📜이름", value=f"{ctx.message.guild.name}",inline=True)
  embed.add_field(name="🧭잠수 시간", value=f"{ctx.message.guild.afk_timeout}",inline=True)
  embed.add_field(name="👱‍♂️서버 주인", value=f"{ctx.message.guild.owner}",inline=True)
  embed.add_field(name="😃서버 멤버수", value=f"{ctx.message.guild.member_count}",inline=True)
  
  embed.add_field(name="⌛서버 생성일", value = ctx.message.guild.created_at.strftime("20%y년 %m월 %d일"),inline=True)
  
  
  
 
  
  embed.add_field(name="💬서버 채팅채널 ", value=f"{len(ctx.message.guild.text_channels)}개",inline=True)
  embed.add_field(name="🔊서버음성채널 ", value=f"{len(ctx.message.guild.voice_channels)}개",inline=True)
 
  embed.add_field(name="🖐시스탬 환영메세지", value=f"{ctx.message.guild.system_channel.name}",inline=True)
  embed.add_field(name="🟢서버 인증단계", value=ctx.message.guild.verification_level,inline=True)
  embed.add_field(name="💌서버 부스터 레벨", value=ctx.message.guild.premium_subscription_count,inline=True)
  embed.set_image(url=ctx.message.guild.icon_url)
 
  await ctx.send(embed=embed)




@bot.command()
async def 채널정보(ctx):
  embed = discord.Embed(title=f"{ctx.channel.name}의 정보입니다", color=0x62c1cc)
  embed.add_field(name="📜이름", value=f"{ctx.channel.mention}",inline=False)
  embed.add_field(name="📜채널위치", value=f"{ctx.channel.position}",inline=False)
  embed.add_field(name="📜채널카테고리", value=f"{ctx.channel.category}",inline=False)
  embed.add_field(name="📜채널 주제", value=f"{ctx.channel.topic}",inline=False)
  embed.add_field(name="📜채널 생성 시각", value=f"{ctx.channel.created_at}",inline=False)
 
  await ctx.send(embed=embed)


    
    


@bot.command(name="주사위")
async def repeat(ctx, *,unmber):
    dice = random.randrange(1,unmber)
    await ctx.send(dice)
     
      

@bot.command(name="따라해")
async def repeat(ctx, *, txt):
  await ctx.message.delete() 
  await ctx.send(txt)   
      

@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def 뮤트(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild

    mutedRole = discord.utils.get(guild.roles, name="mute")

    if not mutedRole:
        mutedRole = await guild.create_role(name="뮤트")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=False, read_messages=True)
    embed = discord.Embed(title="뮤트", description=f"{member.mention} 님이 뮤트되셨습니다. ", colour=discord.Colour.light_gray())
    embed.add_field(name="이유:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.send(f"{member}님은 {guild.name}님으로부터 뮤튼당하셨습니다. 이유: {reason}")
    await member.add_roles(mutedRole, reason=reason)


@bot.command(description="뮤트 해재")
@commands.has_permissions(manage_messages=True)
async def 언뮤트(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="뮤트")

   await member.remove_roles(mutedRole)
   await member.send(f"{member}님은 {ctx.guild.name}서버로부터 언뮤트되셨습니다.")
   embed = discord.Embed(title="언뮤트", description=f"언뮤트-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)
    
@bot.command()
async def 슬로우(ctx, number: str):
    if ctx.author.guild_permissions.administrator:

        if int(number) > 21600 or int(number) <= -1:
            raise commands.BadArgument
        else:
            await ctx.channel.edit(slowmode_delay=int(number))
            embed = discord.Embed(title=f"⌛채널  슬로우  모드를  {number}초로  설정했습니다!", color=0x62c1cc)
            await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title="명령어를 사용할 수 있는 권한이 없어요!", color=0x62c1cc)
        await ctx.reply(embed=embed)
        


@bot.command(name="정보", aliases=["유저정보"])
async def information(ctx, member: discord.Member = None):
    if member is None: member = ctx.author
    embed = discord.Embed(title=f"{member.name}님의 유저정보입니다", color=0x62c1cc)
    embed.add_field(name="📋 이름", value=f"{member.name}", inline=True)
    
    embed.add_field(name="📜별명", value=member.display_name)
    
    status_dict: dict = {discord.Status.online: '🟢온라인',
      discord.Status.offline: '🔴오프라인',
      discord.Status.idle: "🔵자리비움",
      discord.Status.do_not_disturb: "🟠방해금지"}
    user_status = status_dict[member.status]
    embed.add_field(name="📠상태", value=f"{user_status}", inline=True)
    embed.add_field(
        name="📅 가입",
        value=str(member.created_at.year) + "년" +
        str(member.created_at.month) + "월" + str(member.created_at.day) + "일",
        inline=True,
    )
    
    embed.add_field(name="☀️ 가장 높은 역할", value=member.top_role.mention, inline=True)
    embed.add_field(name="😋유저", value="❌" if member.bot else "⭕")
    embed.set_footer(text=f"{ctx.author.name} | 님이 명령어를 사용했습니다.",
                     icon_url=member.avatar_url)
    await ctx.send(embed=embed)


  
  
    

@bot.command(aliases=['ㄷㅂㄱ'])
@commands.cooldown(1, 3600, commands.BucketType.user)
async def 돈받기(ctx):
  user = ctx.author
  users = await get_bank_data()
  if str(user.id) in users:
        
    
    user = ctx.author

    users = await get_bank_data()
    earnings = random.randrange(5000 , 10000)

    await ctx.send(f'{ctx.author.mention} 님이 {earnings} 원을 받으셨습니다')

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)
  else:
    await ctx.send("먼저 `,가입`으로 가입을 해주시기 바랍니다.")
    return

@bot.command()
async def 가입(ctx):
    user = ctx.author
    users = await get_bank_data()
    money = 10000

    if str(user.id) in users:
        await ctx.send("이미 가입이 완료된 상태입니다.")
        return
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0   
        await ctx.send("정상적으로 가입이 완료되었습니다 \n 가입 기념으로 10,000원을 지급했습니다.")  
        users[str(user.id)]["wallet"] += money   

    with open('mainbank.json','w') as f:
        json.dump(users,f)













@bot.command(aliases=['ㄷㅂ'])
async def 도박(ctx,amount = None):
    user = ctx.author
    users = await get_bank_data()
    if str(user.id) in users:
        if amount == None:
            await ctx.reply("배팅할금액을 입력해주세요!")
            return
    
        if amount in ["올인", "ㅇㅇ"]:
            await ctx.send("아직 개발중입니다.")
            return
        else:
            try:
                amount = int(amount)
            except ValueError:
                await ctx.send("걸돈을 제대로 입력해주세요")
                return

        bal = await update_bank(ctx.author)
      
    
    
       

        if amount > bal[0]:
            await ctx.reply('돈이 부족합니다!')
            return
    
        if amount < 500:
            await ctx.reply("적어도 500원이상 베팅해야합니다")
            return
        else:
   
        
         randomNum= random.randrange(1, 3)
        if randomNum == 1:
         
        
        
          await update_bank(ctx.author,-1*amount)
          await ctx.send(f'{ctx.author.mention}님이 졌어요. 돈을 잃게됩니다. ㅠㅠ \n `-{amount}`')
        
        if randomNum == 2:

           
            await update_bank(ctx.author,2*amount)
            await ctx.send(f'{ctx.author.mention}님이 이겼어요! \n `{amount}`')
    else:
        await ctx.send("먼저 `,가입`으로 가입을 해주시기 바랍니다.")
        return
   
    
@bot.command(aliases=['돈'])
async def 잔액(ctx):
    user = ctx.author
    users = await get_bank_data()
   
    if str(user.id) in users:
      await open_account(ctx.author)
      user = ctx.author

      users = await get_bank_data()

      wallet = users[str(user.id)]["wallet"]
    

      embed = discord.Embed(title=f'{ctx.author.name} 님의 방울코인',color = discord.Color.red())
      embed.add_field(name="방울코인", value=wallet)
    else:
      await ctx.send("먼저 `,가입`으로 가입을 해주시기 바랍니다.")
      return
    
    await ctx.send(embed= embed)






    
@bot.command(name="서버수")
async def guild_count(ctx):
      await ctx.send(f"{len(bot.guilds)}개의 서버 참여중")


@bot.command(name="청소")
async def 청소(ctx, amount = 0):

        amounttmp = amount;
        if ctx.message.author.guild_permissions.administrator:
            if amounttmp < 1001:
                await ctx.channel.purge(limit=amount+1);
                cleaning = await ctx.send(str(amounttmp) +  '개의 메세지가 청소 완료되었습니다');
                await asyncio.sleep(5)
                await cleaning.delete()
            else:
                cleaning = await ctx.send('`0`에서 `100`이하의 숫자를 입력해주세요');
                await asyncio.sleep(5)
                await cleaning.delete() 
        else:
            cleaning = await ctx.send(f"{ctx.author.name}님은 권한이 없습니다");
            await asyncio.sleep(5)
            await cleaning.delete()

  



keep_alive()


bot.run(token)
