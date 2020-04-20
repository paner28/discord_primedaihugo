from discord.ext import commands
import discord
import os
import sympy

TOKEN = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()

class data:
    jflag = False
    aflag = False
    axflag = False
    yflag = False
    kmax = 10**15
    kmin = 0
    an = []
    num = [-3] * 100

@client.event
async def on_ready():
    bot_channel = client.get_channel(701367378386223114)
    await bot_channel.send("server start!")
    print("server start!")

@client.event
async def on_message(message):
    global channel,pl
    channel = client.get_channel(685797761290993681)
    pl = []
    if message.channel.name == "素数判定":
        if message.author.bot:
            return
        if data.jflag or data.axflag or data.yflag:
            # xが含まれてた場合はここを読み込む
            kn = message.content
            print(kn)
            if int(kn) != 0:
                data.kmax = 10**(int(kn))
                data.kmin = 10**(int(kn)-1)
            elif int(kn) == 0:
                data.kmax = 10**15
                data.kmin = 0
            if data.yflag:
                data.an = [1,3,7,9]
            if data.axflag:
                data.aflag = True
                data.axflag = False
                await channel.send("スペース区切りでaになる数を数字で指定してください")
                return
        elif data.aflag:
            data.an = message.content.split()
            data.an = [int(i) for i in data.an]
            data.an.sort()
            await channel.send("a = " + str(data.an))
        else:
            #　1回目のルートではここを読み込む
            global t
            k = []
            data.num = [-3] * 100
            msg = message.content
            k = list(msg)
            t = len(k)
            print(k)

        if data.jflag:
            await fx(t)
            await make_list(pl)
            data.jflag = False
            data.kmax = 10**15
            data.kmin = 0
            return

        if data.aflag or data.yflag:
            await fxa(t)
            data.aflag = False
            data.yflag = False
            data.an = []
            return

        await change(k)
        print(nk)

        if "y" in msg:
            data.yflag = True
            await channel.send("4つ子素数判定します\n桁数を入力してください")
            return
        if "x" in msg and "a" in msg:
            data.axflag = True
            await channel.send("桁数を入力してください")
            return
        if 'a' in msg:
            data.aflag = True
            await channel.send("スペース区切りでaになる数を数字で指定してください")
            return
        elif "x" in msg:
            data.jflag = True
            await channel.send("桁数を入力してください")
            return
        else:
            await judge(nk,t)
    else:
        return

async def judge(nk,t):
    p = 0
    for i in range(t):
        if nk[i] < 10:
            p *= 10
        else:
            p *= 100
        p += nk[i]
    if sympy.isprime(int(p)):
        await channel.send(str(p) + "は素数です")
    else:
        await channel.send(str(p) + "=" + str(sympy.factorint(int(p))))
    return

async def change(k):
    global nk
    nk = []
    k = ["10" if i == "t" or i == "T" else i for i in k]
    k = ["11" if i == "j" or i == "J" else i for i in k]
    k = ["12" if i == "q" or i == "Q" else i for i in k]
    k = ["13" if i == "k" or i == "K" else i for i in k]
    k = ["14" if i == "x" or i == "X" else i for i in k]
    k = ["-2" if i == "a" or i == "A" else i for i in k]
    k = ["-2" if i == "y" or i == "Y" else i for i in k]
    try:
        k = [int(i) for i in k]
    except:
        await channel.send("半角自然数を入力してください")
    nk = k
    return nk

async def fx(n):
    for i in range(n):
        if nk[i] == 14:
            nk[i] = -1
            if i == 0:
                for j in range(1,14):
                    data.num[i] = j
                    await fx(n)
            else:
                for j in range(0,14):
                    data.num[i] = j
                    await fx(n)
            nk[i] = 14
            return
        elif nk[i] == -1:
            continue
        else:
            data.num[i] = nk[i]
    q = 0
    for i in range(n):
        if data.num[i] < 10:
            q *= 10
        else:
            q *= 100
        q += data.num[i]
    if q > data.kmin and q < data.kmax and sympy.isprime(q) == True:
        pl.append(q)
    
async def make_list(pl):
    pc = len(pl)
    mflag = [0] * 100000
    maisuu = [[0] * 13 for i in range(100000)]
    print(pl)
    for i in range(pc):
        for j in range(i+1,pc):
            if pl[i]>pl[j]:
                pl[i],pl[j] = pl[j],pl[i]
        for j in range(13):
            if maisuu[i][j] > 4:
                mflag[i] = 1
    for i in range(pc-2,1,-1):
        if mflag[i] == 0:
            for j in range(i+1,pc):
                if maisuu[i] == maisuu[j]:
                    mflag[i] = 1

    for i in range(len(pl)):
        await channel.send(str(pl[i]) + "は素数です")
    await channel.send("素数は" + str(pc) + "個です")    
    
async def fxa(n):
    print(data.num)
    for i in range(n):
        if nk[i] == 14:
            nk[i] = -1
            for j in range(1,14):
                data.num[i] = j
                await fxa(n)
            nk[i] = 14
            return
        elif nk[i] == -1:
            continue
        elif nk[i] == -2:
            data.num[i] = 'a'
        else:
            data.num[i] = nk[i]
    data.num = [i for i in data.num if not i == -3]
    p = map(str, data.num)
    p = ''.join(p)
    for i in data.an:
        kp = p
        kp = kp.replace('a',str(i))
        kp = int(kp)
        if kp > data.kmax or kp < data.kmin:
            return
        if sympy.isprime(kp) == False:
            return
    await adc(n)
    await channel.send(str(v) + "は素数です")
    return

async def adc(n):
    global v
    v=0
    pa = ['0']
    for i in range(n):
        if data.num[i] == 10:
            pa += "T"
        elif data.num[i] == 11:
            pa += "J"
        elif data.num[i] == 12:
            pa += "Q"
        elif data.num[i] == 13:
            pa += "K"
        else:
            pa += str(data.num[i])
    pa = [i for i in pa if not i == "0"]
    print(pa)
    v = ''.join(pa)
    return v

client.run(TOKEN)
