import os
import json
import ast
import shlex
import shutil
import discord
import crayons
import random
import discord
import utils
from datetime import datetime, timedelta
import pytz
from discord.ext import commands
from discord.utils import oauth_url
import urllib.request
from urllib.request import urlopen
from google_images_download import google_images_download
import asyncio
from asyncio import sleep
import psycopg2
from discord.utils import get
import requests
import aiohttp
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw, ImageOps

bot = commands.Bot(command_prefix='b!', case_insensitive=True)
bot.remove_command('help') 
bot.owner_id = 'BOT OWNER ID HERE'



def owner_or_has_permissions(**perms):
    async def predicate(ctx):
        if await ctx.bot.is_owner(ctx.author):
            return True
        permissions = ctx.channel.permissions_for(ctx.author)
        missing = [perm for perm, value in perms.items(
        ) if getattr(permissions, perm, None) != value]
        if not missing:
            return True
        raise commands.MissingPermissions(missing)

    return commands.check(predicate)


@bot.before_invoke
async def log_command(ctx):
    if ctx.invoked_subcommand:
        return
    ts = crayons.white(utils.get_timestamp(), bold=True)
    msg = crayons.green(ctx.message.content.replace(
        ctx.prefix, "", 1), bold=True)
    chan = crayons.magenta(f"#{ctx.channel}", bold=True)
    guild = crayons.magenta(f"({ctx.guild})")
    user = crayons.yellow(f"{ctx.author}", bold=True)
    print(f"{ts} {msg!s} in {chan} {guild} by {user}")


@bot.command(aliases=["jl","joinlink","link"],pass_context=True)
async def invite(ctx,*,message=""):
    invitelinknew = await ctx.channel.create_invite(destination = ctx.message.channel, xkcd = True, max_uses = 100)
    embed = discord.Embed(title=f"INVITE LINK TO JOIN THIS SERVER",
                          description=f"Here is an instant invite to your server: {invitelinknew}", color=12320855)
    embed.set_image(url="https://i.imgur.com/u07ktga.png")
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def devastate(ctx,*,message=""):
    embed = discord.Embed(title=f"WELCOME TO DEVASTATE ",
                          description=f"👪 This server has {ctx.guild.member_count} members. ", color=12320855)
    embed.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=embed)

@bot.command(aliases=["h"])
async def help(ctx):
    embed = discord.Embed(title=f"BOT HELP COMMANDS",
                          description=f"", color=12320855)
    embed.add_field(name="⚡ BOT Commands",
                    value="`profile`, `dev`", inline=False)
    embed.add_field(name="🎮 Game Commands",
                    value="`dice`, `coinflip`, `truth`, `dare`", inline=False)
    embed.add_field(name="⚙️ Others Commands",
                    value="`invite`,`invitebot`,`quote`, `google`, `time`, `ping`", inline=False)
    embed.add_field(name="🛡️ Administrator Commands",
                    value=f"`announce`, `mop`\n\n Your prefix is **b!** \n\n Use **b!help**\n If you need help or have questions contact server owner\n Add to your server - [Click Here](https://discordapp.com/oauth2/authorize?client_id=703102608776101939&scope=bot&permissions=268823616)\n [Join Official Server](https://discord.gg/TuDEbZq) \n\n 📊 Currently I'am in **{str(len(bot.guilds))} servers.** ", inline=False)
    
    embed.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=embed)

@bot.command(aliases=["q", "quotes"])
async def quote(ctx):
    import random
    qn = random.randint(0, 5726)
    with open("data/quotes.json", "r", encoding="utf-8") as f:
        data_quotes = json.load(f)
        print(len(data_quotes))
        msg = f"```fix\n{data_quotes[qn]['quoteText']}\n-{data_quotes[qn]['quoteAuthor']}\n``` "
        await ctx.send(msg)


@bot.command(aliases=["dares", "d"])
async def dare(ctx):
    qn = random.randint(0, 7)
    with open("data/dares.json", "r", encoding="utf-8") as f:
        data_dares = json.load(f)
        msg = f"{ctx.message.author.mention}\n```fix\n{data_dares[qn]['dare']}\n``` "
        await ctx.send(msg)


@bot.command(aliases=["devs", "developer"])
async def dev(ctx):
    embed = discord.Embed(title=f"Felix Fernando",
                          description=f"VoltGizeRz", color=15105570)
    embed.add_field(name="Biography",
                    value="Hello Greetings from me :smile: ", inline=False)
    embed.add_field(name="Instagram", value="@felix_fernandoo", inline=False)
    embed.add_field(name="GitHub", value="github.com/voltgizerz", inline=False)
    user = bot.get_user(bot.owner_id)
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_author(name="Developer Information",
                     icon_url=bot.user.avatar_url)
    embed.set_footer(text="Command invoked by {}".format(
        ctx.message.author.name))
    await ctx.send(embed=embed)

@bot.command(aliases=["infoprofile", "ip"])
async def profile(ctx, *, message=""):
    embed = discord.Embed(
        title=f"{ctx.message.author}", description=f"", color=15105570)
    tanggal = ctx.author.joined_at.strftime("%d %b %Y")
    registrasi = ctx.author.created_at.strftime("%d %b %Y")
    mentions = [
        role.mention for role in ctx.message.author.roles if role.mentionable]
    roles = " ".join(mentions)

    embed.add_field(name="User ID", value=f"{ctx.author.id}", inline=False)
    embed.add_field(name="Nickname", value=f"{ctx.author.nick}", inline=False)
    embed.add_field(name="Roles", value=f"{roles}", inline=False)
    embed.add_field(name="Joined Date", value=f"{tanggal}", inline=False)
    embed.add_field(name="Registration Date",
                    value=f"{registrasi}", inline=False)
    embed.add_field(name="Status", value=f"{ctx.author.status}", inline=False)
    user = bot.get_user(ctx.author.id)
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_author(name="User Information", icon_url=bot.user.avatar_url)
    embed.set_footer(text="Command invoked by {}".format(
        ctx.message.author.name))
    await ctx.send(embed=embed)


@bot.group(aliases=["search"])
async def google(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.invoke(bot.get_command("google images"))


@google.command(name="gambar")
async def google_img(ctx, *, message=""):
    if ctx.message.content not in ['b!search','b!google']:
        try:
            index = random.randint(0, 2)
            msg = f"⌛ Please Wait, I am working on it..."
            await ctx.send(msg)
            if 'b!search' in ctx.message.content:
                keywords = ctx.message.content.replace("b!search ","").lower()
            elif 'b!google' in ctx.message.content:
                keywords = ctx.message.content.replace("b!google ","").lower()
            response = google_images_download.googleimagesdownload()
            arguments = {"keywords":keywords,"limit":3,"print_urls":True}
            paths = response.download(arguments)
            with open(paths[0][keywords][index], 'rb') as f: #OPEN FILE LOCATION
                msg = f"{ctx.message.author.mention} Finished searching images for **{keywords}** 🤔"
                await ctx.send(file=discord.File(f),content=msg)
        except:
            msg = f"{ctx.message.author.mention} Images not found for **{keywords}** 🤔"
            await ctx.send(msg)
        shutil.rmtree('downloads') 
    else:
        msg = f"{ctx.message.author.mention} Missing Keywords Example : **b!search 'keywords'** 🤔"
        await ctx.send(msg)

@bot.group(aliases=["indonesia", "indocovid", "covidindo", "indo", "korona", "covid19"])
async def covid(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.invoke(bot.get_command("covid indo"))


@covid.command(name="indo")
async def covid_indo(ctx, *, message=""):
    if(str(ctx.message.content) in ["b!covid", "b!indonesia", "b!indocovid", "b!covidindo", "b!indo", "b!korona", "b!covid19"]):
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        url = "https://api.kawalcorona.com/indonesia/"
        headers = {'User-Agent': user_agent, }
        request = urllib.request.Request(
            url, None, headers)  # The assembled request
        response = urllib.request.urlopen(request)
        data = json.load(response)  # The data u need\

        tz_Jakarta = pytz.timezone('Asia/Jakarta')
        datetime_Jakarta = datetime.now(tz_Jakarta)
        tanggal = datetime_Jakarta.strftime("%d %b %Y %H:%M:%S")

        msg = f"{ctx.message.author.mention} - **{data[0]['name']} 🇮🇩 **```fix\n😔 POSITIF   : {data[0]['positif']}\n😄 SEMBUH    : {data[0]['sembuh']}\n😭 MENINGGAL : {data[0]['meninggal']}\n🏥 DIRAWAT   : {data[0]['dirawat']}```*Sumber data : Kementerian Kesehatan & JHU. Update terakhir : {tanggal} WIB* "
        await ctx.send(msg)
    else:
        kota = ctx.message.content.replace("b!covid ", "").lower()
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        url = "https://api.kawalcorona.com/indonesia/provinsi/?"
        headers = {'User-Agent': user_agent, }
        request = urllib.request.Request(
            url, None, headers)  # The assembled request
        response = urllib.request.urlopen(request)
        data = json.load(response)

        x = 0
        get = 0
        for x in range(34):
            if(kota == data[x]['attributes']['Provinsi'].lower()):
                get = x
                break
            else:
                x = x

    if(kota != data[x]['attributes']['Provinsi'].lower()):
        tz_Jakarta = pytz.timezone('Asia/Jakarta')
        datetime_Jakarta = datetime.now(tz_Jakarta)
        tanggal = datetime_Jakarta.strftime("%d %b %Y %H:%M:%S")
        msg = f"{ctx.message.author.mention} - Oopps... 😭 ```fix\n❌ PROVINSI '{kota}' YANG ANDA MASUKAN TIDAK TERDAFTAR!\n✔️ PASTIKAN ANDA MEMASUKAN NAMA PROVINSI DENGAN BENAR\n⚠️ CONTOH : b!covid Sumatera Selatan```*Sumber data : Kementerian Kesehatan & JHU. Update terakhir : {tanggal} WIB* "
        await ctx.send(msg)
    else:
        tz_Jakarta = pytz.timezone('Asia/Jakarta')
        datetime_Jakarta = datetime.now(tz_Jakarta)
        tanggal = datetime_Jakarta.strftime("%d %b %Y %H:%M:%S")
        msg = f"{ctx.message.author.mention} - **{data[get]['attributes']['Provinsi']} 🇮🇩 **```fix\n😔 POSITIF   : {data[get]['attributes']['Kasus_Posi']}\n😄 SEMBUH    : {data[get]['attributes']['Kasus_Semb']}\n😭 MENINGGAL : {data[get]['attributes']['Kasus_Meni']}```*Sumber data : Kementerian Kesehatan & JHU. Update terakhir : {tanggal} WIB* "
        await ctx.send(msg)


@covid.command(name="sumsel")
async def covid_indo(ctx):
    tz_Jakarta = pytz.timezone('Asia/Jakarta')
    datetime_Jakarta = datetime.now(tz_Jakarta)
    tanggal = datetime_Jakarta.strftime("%d %b %Y %H:%M:%S")
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    url = "https://api.kawalcorona.com/indonesia/provinsi/?"
    headers = {'User-Agent': user_agent, }
    request = urllib.request.Request(
        url, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)
    data = json.load(response)  # The data u need\
    msg = f"{ctx.message.author.mention} - **{data[6]['attributes']['Provinsi']} 🇮🇩 **```fix\n😔 POSITIF   : {data[6]['attributes']['Kasus_Posi']}\n😄 SEMBUH    : {data[6]['attributes']['Kasus_Semb']}\n😭 MENINGGAL : {data[6]['attributes']['Kasus_Meni']}```*Sumber data : Kementerian Kesehatan & JHU. Update terakhir : {tanggal} WIB* "
    await ctx.send(msg)


@covid.command(name="jkt")
async def covid_indo(ctx):
    tz_Jakarta = pytz.timezone('Asia/Jakarta')
    datetime_Jakarta = datetime.now(tz_Jakarta)
    tanggal = datetime_Jakarta.strftime("%d %b %Y %H:%M:%S")
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    url = "https://api.kawalcorona.com/indonesia/provinsi/?"
    headers = {'User-Agent': user_agent, }
    request = urllib.request.Request(
        url, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)
    data = json.load(response)  # The data u need\
    msg = f"{ctx.message.author.mention} - **{data[0]['attributes']['Provinsi']} 🇮🇩 **```fix\n😔 POSITIF   : {data[0]['attributes']['Kasus_Posi']}\n😄 SEMBUH    : {data[0]['attributes']['Kasus_Semb']}\n😭 MENINGGAL : {data[0]['attributes']['Kasus_Meni']}```*Sumber data : Kementerian Kesehatan & JHU. Update terakhir : {tanggal} WIB* "
    await ctx.send(msg)


def monotonic():
    import time
    return time.monotonic()

@bot.command(aliases=["pong", "uptime"], pass_context=True)
async def ping(ctx):
    before = monotonic()
    ping = (monotonic() - before) * 1000
    embed = discord.Embed(
        title="Devastate Status :love_you_gesture_tone1: ", color=3066993)
    embed.set_footer(text=f"Command invoked by {ctx.message.author.name}")
    embed.add_field(name="Client Latency",
                    value=f"`⏱️ {int(float(ping)/10)}ms`", inline=False)
    embed.add_field(name='Bot Latency   ',
                    value=f"`⌛ {round(bot.latency * 1000/10)}ms`")
    await ctx.send(embed=embed)


@bot.command(pass_context=True, aliases=["announcement"])
@commands.has_permissions(administrator=True)
async def announce(ctx,  *, message=""):
    try:
        channel = bot.get_channel("INPUT YOUR ANNOUNCEMENT TEXT CHANNEL ID HERE")
        await channel.send(message)
        await ctx.send(f'{ctx.message.author.mention} Announcement Have Been Sent! :white_check_mark: ')
    except:
        await ctx.send(f'{ctx.message.author.mention} Failed Sending Announcement! :x: ')


@announce.error
async def mop_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(":warning: You cant do that! :face_with_hand_over_mouth: ")


@bot.command(pass_context=True, aliases=["mopping", "clean", "clear"])
@commands.has_permissions(administrator=True)
async def mop(ctx, limit: int="", message=""):
    if limit!='':
        if(limit > 50):
            await ctx.send(f':warning: MAX Deleting 50 Messages {ctx.author.mention}')
        else:
            try:
                await ctx.channel.purge(limit=limit)
                await ctx.message.delete()
            except:
                await ctx.send(f':recycle:  Done Cleared **{limit}** Message By {ctx.author.mention}')
    else:
        await ctx.send(f'{ctx.author.mention} Failed cleared message missing arguments Example : **b!mop 10**')


@mop.error
async def mop_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(":warning: You cant do that! :face_with_hand_over_mouth: ")


@bot.command(aliases=["truths", "t"])
async def truth(ctx):
    qn = random.randint(0, 7)
    with open("data/truths.json", "r", encoding="utf-8") as f:
        data_truths = json.load(f)
        msg = f"{ctx.message.author.mention}\n```fix\n{data_truths[qn]['truth']}\n``` "
        await ctx.send(msg)


@bot.command(aliases=["giphy"],pass_context=True)
async def gif(ctx, *, search=""):
    try:
        author = ctx.message.author
        user_name = author.name
        session = aiohttp.ClientSession()
        print(search)
        if search == '':
            embed = discord.Embed(title=f"{user_name} Random GIF",
                                    description=f"", color=3447003)
            response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=PgVCpPdQHEIaeUcBrpNGXKcnuQS6AVS0')
            data = json.loads(await response.text())
            embed.set_image(url=data['data']['images']['original']['url'])
        else:
            embed = discord.Embed(title=f"{user_name} GIF : **{search}**  ",
                                    description=f"", color=3447003)
            search.replace(' ', '%20')
            response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=PgVCpPdQHEIaeUcBrpNGXKcnuQS6AVS0&limit=10')
            await session.close()
            data = json.loads(await response.text())
            gif_choice = random.randint(0, 9)
            embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])
        await session.close()
        await ctx.send(embed=embed)
    except:
        msg = f"{ctx.message.author.mention} GIF not found for **{search}**" 
        await ctx.send(msg)


@bot.command(aliases=["roll", "rolldice"])
async def dice(ctx):
    dice = random.randint(0, 5)
    link = f"data/dice/{dice+1}.png"
    with open(link, 'rb') as f:
        msg = f"{ctx.message.author.mention} you Got **{dice+1}**"
        await ctx.send(msg)
        await ctx.send(file=discord.File(f))


@bot.command(aliases=["s"], hidden=True)
@commands.is_owner()
async def say(ctx, *, message):
    await ctx.send(message)


@bot.command(aliases=["linkbot"])
async def invitebot(ctx):
    p = discord.Permissions.text()
    p.mention_everyone = False
    p.send_tts_messages = False
    p.manage_roles = True
    await ctx.send(oauth_url(bot.user.id, p))


async def status_task():
    while True:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="#StayAtHome"))
        await asyncio.sleep(300)
        await bot.change_presence(activity=discord.Streaming(name="Social Distancing", url="https://www.twitch.tv/voltgizerz"))
        await asyncio.sleep(300)
        await bot.change_presence(activity=discord.Game(name=f"DM to contact Developer", type=0))
        await asyncio.sleep(300)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Devastate | b!help"))
        await asyncio.sleep(300)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="#BlackLiveMattters"))
        await asyncio.sleep(300)



def image_process(member,status,number):
    im = Image.open('./avatar/avatar.jpg')
    im = im.resize((300, 300))
    bigsize = (im.size[0] * 5, im.size[1] * 5)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill='white', outline='white')
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save('./avatar/output.png')

    if status == 'join':
        background = Image.open('./avatar/bg.png')
    else:
        background = Image.open('./avatar/bg-gb.png')

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype(r'./avatar/sans.ttf', 100)

    if status == 'join':
        draw.text((645, 80), "WELCOME", fill='white', font=font,)
    else:
        draw.text((645, 80), "GOODBYE", fill='white', font=font,)

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype(r'./avatar/sans.ttf', 65)
    draw.text((645, 180), member, fill='white', font=font)

    if status == 'join':
        draw.text((645, 250), f"Guild Member - {number+1}", fill='white', font=font)
    else:
        draw.text((645, 250), f"See you Again :(", fill='white', font=font)
    background.paste(im, (60, 80), im)
    background.save('./avatar/overlap.png') #OUTPUT FILE TO UPLOAD
    return True

@bot.event
async def on_member_join(member):
    #if member.guild.id == (YOUR DISCORD ID HERE): (USE THIS ONLY, IF YOUR BOT IN MORE THAN 1 DISCORD GUILD)
    print("Recognized that " + member.name + " joined")
    Picture_request = requests.get(member.avatar_url)
    if Picture_request.status_code == 200:
        with open("./avatar/avatar.jpg", 'wb') as f:
            f.write(Picture_request.content)
    guild = bot.get_guild("INSERT YOUR GUILD ID HERE") #YOUR GUILD ID
    if guild in bot.guilds:
        members = guild.member_count
        
    image_process(member,'join',members)
    channel = bot.get_channel("INSRERT YOUR WELCOME TEXT CHANNEL ID HERE") # WELCOME  TEXT CHANNEL ID
    with open("./avatar/overlap.png", 'rb') as f: #OPEN FILE LOCATION
        msg = (f"**SELAMAT DATANG {member.mention} DI DEVASTATE :zap:**\n\n- Silahkan membaca dan memahami <#562899314511446034> & <#562897998456291329> terlebih dahulu.\n- Jika sudah membaca dan memahami silahkan bergabung di voice channel Waiting Rooms.\n- Anda harus melakukan interview terlebih dahulu sebelum bergabung.\n\n<@&289742953440608256> atau <@&289743236203937793>  hanya akan melakukan interview player yang berada di voice channel Ruang Tunggu.")
        await channel.send(file=discord.File(f),content=msg)

@bot.event
async def on_member_remove(member):
    #if member.guild.id == (YOUR DISCORD ID HERE): (USE THIS ONLY, IF YOUR BOT IN MORE THAN 1 DISCORD GUILD)
    print("Recognized that " + member.name + " left")
    Picture_request = requests.get(member.avatar_url)
    if Picture_request.status_code == 200:
        with open("./avatar/avatar.jpg", 'wb') as f:
            f.write(Picture_request.content)
    image_process(member,'left',20)
    channel = bot.get_channel("INSRERT YOUR GOODBYE TEXT CHANNEL ID HERE") # GOODBYE TEXT CHANNEL ID
    with open("./avatar/overlap.png", 'rb') as f: #OPEN FILE LOCATION
        msg = (f"**SELAMAT TINGGAL {member.mention} DARI DEVASTATE :zap:**\nKami segenap <@&289742953440608256> dan <@&289743236203937793> dan seluruh staff lainnya berterima kasih\nkepada anda sudah meluangkan waktu pada server kami, kami tetap menuggu kehadiran anda untuk kembali. ")
        await channel.send(file=discord.File(f),content=msg)


@bot.event
async def on_ready():
    bot.loop.create_task(status_task())
    ts = crayons.white(utils.get_timestamp(), bold=True)
    print(f"{ts} Logged in as {crayons.red(bot.user, bold=True)} (ID {crayons.yellow(bot.user.id, bold=True)})")
    owner = bot.get_user(bot.owner_id)
    try:
        print("Ready!")
        bot.loop.create_task(status_task())
    except discord.HTTPException:
        pass

@bot.event
async def on_command_error(ctx, error):
    ts = crayons.white(utils.get_timestamp(), bold=True)
    print(f"{ts} {crayons.red(error.__class__.__name__, bold=True)} {error}")
    if isinstance(error, commands.NotOwner):
        await ctx.send("**Restricted command.**", delete_after=10)
    elif isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace(
            'guild', 'server').title() for perm in error.missing_perms]
        await ctx.send(f"You are missing {missing} permission(s) to run this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(error)


def get_token(*, test=False):
    token = os.getenv(
        "")
    if token:
        return token
    path = ".token"
    if test:
        path += "-test"
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


if __name__ == '__main__':
    import sys
    test = "--test" in sys.argv
    if test:
        bot.command_prefix = "-"
    bot.run(get_token(test=test))
