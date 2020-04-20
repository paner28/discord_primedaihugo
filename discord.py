# coding: UTF-8
# token情報やチャンネルidなどの定数を別のファイルにおく
import const
# 関数関係
import function
import channel
import data
import os
# インストールした discord.py を読み込む
import discord

# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.environ['DISCORD_BOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
  channel = client.get_channel(const.channel_id['bot_control'])
  # 起動したらターミナルにログイン通知が表示される
  await channel.send('server-start!')
  data.a = data.game(data.player(0), data.player(0))
  data.b = data.game(data.player(0), data.player(0))
  print('...ready')
  await channel.send('...ready')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
  # メッセージ送信者がBotだった場合は無視する
  if message.author.bot:
    return
  if message.channel.name == 'bot_作成チーム':
    return
  if message.channel.name == 'bot_control':
    await channel.bot_control(message)
    return
  if 'プレイヤー' in message.channel.name:
    channel_name = message.channel.name
    print(channel_name[5])
    print(channel_name[7])
    await channel.player(message, channel_name[5], channel_name[7])
    return 
  # if message.channel.name == 'プレイヤーa-1':
  #   await channel.playera1(message)
  #   return
  # if message.channel.name == 'プレイヤーa-2':
  #   await channel.playera2(message)
  #   return
  # if message.channel.name == 'プレイヤーb-1':
  #   await channel.playerb1(message)
  #   return
  # if message.channel.name == 'プレイヤーb-2':
  #   await channel.playerb2(message)
  #   return

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
