# coding: UTF-8
# token情報やチャンネルidなどの定数を別のファイルにおく
import const
# インストールした discord.py を読み込む
import discord

# 自分のBotのアクセストークンに置き換えてください
TOKEN = const.token

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
  channel = client.get_channel(const.channel_id['bot_control'])
  # 起動したらターミナルにログイン通知が表示される
  print('投稿削除サーバー')
  await channel.send('投稿削除サーバー起動')
  return

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
  # メッセージ送信者がBotだった場合は無視する
  if message.author.bot:
    return
  if message.channel.name == 'bot作成チーム':
    return
  if message.channel.name == 'bot_control':
    return
  if message.channel.name == 'コメントルーム':
    return
  if message.channel.name == 'ルール':
    return
  if message.channel.name == '対戦a観客部屋':
    return
  if message.channel.name == '対戦b観客部屋':
    return
  if message.channel.name == 'バグやご要望':
    return
  await message.channel.purge()
  print('投稿削除しました。')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
