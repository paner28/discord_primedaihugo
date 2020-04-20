import function
import data
import const

async def bot_control(msg):
  print(f'channel.bot_control: msg={msg}, ary={msg.content.split()}')
  ary = msg.content.split()
  if ary[0] == 'role_set':
    await msg.channel.send('役職を設定します。')
    if len(ary) != 4:
      await msg.channel.send(f'{msg.author.mention} role_setの引数の数が違います。')
      return
    ary.pop(0)
    a_or_b = ary[0]
    ary.pop(0)
    if a_or_b != 'a' and a_or_b != 'b':
      await msg.channel.send(f'{msg.author.mention} role_setの対戦の文字が違います。')
      return
    user_id = ary[0].translate(str.maketrans({'<':'', '>': '', '@':'', '!':''}))
    member = msg.guild.get_member(int(user_id))
    await function.role_change(member, f'player-{a_or_b}-1')
    user_id = ary[1].translate(str.maketrans({'<':'', '>': '', '@':'', '!':''}))
    member = msg.guild.get_member(int(user_id))
    await function.role_change(member, f'player-{a_or_b}-2')
    await msg.channel.send(f'{msg.author.mention} 役職の設定が終わりました。')
  if ary[0] == 'game_start':
    await msg.channel.send('ゲームを開始する準備をしています。')
    if len(ary) != 2:
      await msg.channel.send(f'{msg.author.mention} game_startの引数の数が違います。')
      return
    a_or_b = ary[1]
    if a_or_b != 'a' and a_or_b != 'b':
      await msg.channel.send(f'{msg.author.mention} game_startの対戦の文字が違います。')
      return
    class_data = data.a
    if a_or_b == 'b':
      class_data = data.b
    channel = msg.guild.get_channel(const.channel_id[f'player-{a_or_b}-1'])
    await channel.purge()
    channel = msg.guild.get_channel(const.channel_id[f'player-{a_or_b}-2'])
    await channel.purge()
    for i in range(11):
      class_data.draw('1')
      class_data.draw('2')
    class_data.turn = '1'
    await function.message_push(msg.guild, f'player-{a_or_b}-1', f"素数大富豪スタート！\nお互いに11枚引きました。\n\n{class_data.turn_message('1')}")
    await function.message_push(msg.guild, f'player-{a_or_b}-2', f"素数大富豪スタート！\nお互いに11枚引きました。\n\n{class_data.turn_message('2')}")
    await function.message_push(msg.guild, f'jikkyo-{a_or_b}', f"素数大富豪スタート！\nお互いに11枚引きました。\n\n{class_data.turn_message('jikkyo')}")
    await msg.channel.send(f'{msg.author.mention} ゲームスタートしました。')
    return
  if ary[0] == 'game_reset':
    await msg.channel.send('ゲームをリセットします。')
    if len(ary) != 2:
      await msg.channel.send(f'{msg.author.mention} game_startの引数の数が違います。')
      return
    a_or_b = ary[1]
    if a_or_b != 'a' and a_or_b != 'b':
      await msg.channel.send(f'{msg.author.mention} game_startの対戦の文字が違います。')
      return
    class_data = data.a
    if a_or_b == 'b':
      class_data = data.b
    player_id = class_data.player['1'].id
    if player_id != 0:
      player = msg.guild.get_member(player_id)
      await function.role_change(player, "kankyaku")
    player_id = class_data.player['2'].id
    if player_id != 0:
      player = msg.guild.get_member(player_id)
      await function.role_change(player, "kankyaku")
    if a_or_b == 'a':
      data.a = data.game(data.player(0), data.player(0))
    elif a_or_b == 'b':
      data.b = data.game(data.player(0), data.player(0))
    await msg.channel.send(f'{msg.author.mention} ゲームリセットしました。')
    return
  if ary[0] == 'role_reset':
    await function.message_push(msg.guild, 'bot_control', "全てのメンバーを観客に変更します。")
    for member in msg.guild.members:
      if not member.bot:
        await function.role_change(member, "kankyaku")
    await msg.channel.send('役職の初期化がおわりました。')
    return
  print(f"{ary[0]}が見当たりません。")

async def player(msg, a_or_b, player_num_):
  print(f'channel.player: msg={msg}, a_or_b={a_or_b}, player_num_={player_num_}')
  class_data = data.a
  if a_or_b == 'b':
    class_data = data.b
  if class_data.turn != player_num_:
    return #あなたの番じゃないよ
  return_obj = class_data.player_input(player_num_, msg.content.upper())
  print(f"channel.player return_obj={return_obj}")
  if return_obj['type'] == 'turn_continue': # まだ自分のターンが続くとき
    await msg.channel.send(return_obj['text'])
    return
  if return_obj['type'] == 'turn_end': # 自分のターンが終わるとき,全体で公開されるとき
    text = return_obj['text']
    await function.message_push(msg.guild, 'player-' + a_or_b + '-1', f"{text}\n{class_data.turn_message('1')}")
    await function.message_push(msg.guild, 'player-' + a_or_b + '-2', f"{text}\n{class_data.turn_message('2')}")
    await function.message_push(msg.guild, 'jikkyo-' + a_or_b, f"{text}\n{class_data.turn_message('jikkyo')}")
    return
  if return_obj['type'] == 'winner':
    await function.message_push(msg.guild, f'player-{a_or_b}-{player_num_}', f"＿人人人人人人＿\n＞　YOU WIN!　＜\n￣Y^Y^Y^Y^Y^Y^￣\n{class_data.current_situation(0,0)}")
    await function.message_push(msg.guild, f'player-{a_or_b}-{data.teki_num(player_num_)}', f"YOU LOSE\n{class_data.current_situation(0,0)}")
    await function.message_push(msg.guild, 'jikkyo-' + a_or_b, f"＿人人人人人人人＿\n＞　ゲーム終了　＜\n￣Y^Y^Y^Y^Y^Y^Y^￣\nプレイヤー{player_num_}が勝利しました。\n{class_data.current_situation(0,0)}")
    player1 = msg.guild.get_member(int(class_data.player['1'].id))
    player2 = msg.guild.get_member(int(class_data.player['2'].id))
    print(f'channel.player winner player1={player1}')
    print(f'channel.player winner player2={player2}')
    await function.role_change(player1, 'kankyaku')
    await function.role_change(player2, 'kankyaku')
    await function.message_push(msg.guild, 'bot_control', '役職設定終了しました。')
    if a_or_b == 'a':
      data.a = data.game(data.player(0), data.player(0))
    if a_or_b == 'b':
      data.b = data.game(data.player(0), data.player(0))
    return
  print(f"channel.player return_dict error : dict={return_obj}")

# reutrn_obj = {'type', 'text'}
