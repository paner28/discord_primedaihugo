import random
import const
import sympy

class player:
  def __init__(self, id):
    self.id = id
    self.hand = []

class gouseisu:
  def __init__(self):
    self.flag = False
    self.field = {'list':[], 'obj':{}}
    self.gouseisu_flag = False #合成数の時にはフラグを立てる

class game:
  def __init__(self, a, b):
    self.turn = '1'
    self.kakumei = False
    self.draw_flag = False
    self.gouseisu = gouseisu()
    self.field = []
    self.graveyard = []
    self.joker_memory = {'text': '', 'replace':[]}
    self.deck = [
      {'num':1,'char':'1'},{'num':1,'char':'1'},{'num':1,'char':'1'},{'num':1,'char':'1'},
      {'num':2,'char':'2'},{'num':2,'char':'2'},{'num':2,'char':'2'},{'num':2,'char':'2'},
      {'num':3,'char':'3'},{'num':3,'char':'3'},{'num':3,'char':'3'},{'num':3,'char':'3'},
      {'num':4,'char':'4'},{'num':4,'char':'4'},{'num':4,'char':'4'},{'num':4,'char':'4'},
      {'num':5,'char':'5'},{'num':5,'char':'5'},{'num':5,'char':'5'},{'num':5,'char':'5'},
      {'num':6,'char':'6'},{'num':6,'char':'6'},{'num':6,'char':'6'},{'num':6,'char':'6'},
      {'num':7,'char':'7'},{'num':7,'char':'7'},{'num':7,'char':'7'},{'num':7,'char':'7'},
      {'num':8,'char':'8'},{'num':8,'char':'8'},{'num':8,'char':'8'},{'num':8,'char':'8'},
      {'num':9,'char':'9'},{'num':9,'char':'9'},{'num':9,'char':'9'},{'num':9,'char':'9'},
      {'num':10,'char':'T'},{'num':10,'char':'T'},{'num':10,'char':'T'},{'num':10,'char':'T'},
      {'num':11,'char':'J'},{'num':11,'char':'J'},{'num':11,'char':'J'},{'num':11,'char':'J'},
      {'num':12,'char':'Q'},{'num':12,'char':'Q'},{'num':12,'char':'Q'},{'num':12,'char':'Q'},
      {'num':13,'char':'K'},{'num':13,'char':'K'},{'num':13,'char':'K'},{'num':13,'char':'K'},
      {'num':77,'char':'X'},{'num':77,'char':'X'}
    ]
    random.shuffle(self.deck)
    # self.deck = random.shuffle(self.deck)
    self.player = {'1':a, '2':b}

  def current_situation(self, one_secret, two_secret):
    print(f'current_situation: one_secret={one_secret}, two_secret={two_secret}')
    self.hand_sort()
    player_1 = ', '.join(list(map(lambda x: x['char'], self.player['1'].hand)))
    player_2 = ', '.join(list(map(lambda x: x['char'], self.player['2'].hand)))
    field = ', '.join(list(map(lambda x: x['char'], self.field)))
    field_num = ''.join(list(map(lambda x: str(x['num']), self.field)))
    if one_secret:
      player_1 = ', '.join(list(map(lambda x: '?', self.player['1'].hand)))
    if two_secret:
      player_2 = ', '.join(list(map(lambda x: '?', self.player['2'].hand)))
    return f"```\n山札残り枚数:{len(self.deck)}\n\nプレイヤー1:{player_1}\n場の状況:{field} ({field_num})\nプレイヤー2:{player_2}\n```"

  def draw(self, player_num_):
    print(f'data.draw: player_num_={player_num_} deck_num={len(self.deck)}')
    if self.deck == []:
      print(f'data.draw: デッキリフレッシュ')
      if self.graveyard == []:
        print(f'data.draw: デッキリフレッシュできなかった。')
        return
      self.deck.extend(self.graveyard)
      self.graveyard = []
    self.player[player_num_].hand.append(self.deck[0])
    self.deck.pop(0)
    self.player[player_num_].hand = sorted(self.player[player_num_].hand, key=lambda x : int(x['num']))

  def hand_sort(self):
    print(f'data.hand_sort')
    self.player['1'].hand = sorted(self.player['1'].hand, key=lambda x : int(x['num']))
    self.player['2'].hand = sorted(self.player['2'].hand, key=lambda x : int(x['num']))

  def turn_message(self, player_num_):
    print(f'data.turn_message: player_num_={player_num_}')
    if player_num_ == 'jikkyo':
      return f'{self.current_situation(0, 0)}\n\nプレイヤー{self.turn}の番です。'
    if player_num_ == self.turn:
      return f"{self.current_situation(not player_num_ == '1', not player_num_ == '2')}\nあなたのターンです。\n素数はそのままアルファベットで記入\nx はジョーカー\nd はドロー(1ターンに一度のみ)\ng は合成数だし\npはパス"
    else:
      return f"{self.current_situation(not player_num_ == '1', not player_num_ == '2')}\n相手のターンです。しばらくお待ちください。"

  def player_input(self, player_num_, text_):  # text_は大文字
    print(f'data.player_input: player_num_={player_num_}, text_={text_}')
    if text_ == 'D':
      if self.draw_flag:
        return {'type':'turn_continue','text':"すでに一枚引きました！"}
      self.draw(player_num_)
      self.draw_flag = True
      return {'type':'turn_end', 'text':'ドローしました。'}
    if text_ == 'P':
      self.graveyard.extend(self.field)
      self.field = []
      self.draw_flag = False
      self.turn = teki_num(player_num_)
      return {'type':'turn_end', 'text':'パスしました。相手にターンが渡ります。'}
    if text_ == 'G':
      self.gouseisu.flag = True
      return {'type':'turn_continue', 'text':"合成数出しが選択されました。場に出したい合成数を文字で入力してください。"}
    if text_ == 'X':
      print('ジョーカー最強！')
    elif 'X' in text_: #ジョーカーを含んでいた時
      self.joker_memory['text'] = text_
      self.joker_memory['replace'] = []
      return {'type':'turn_continue','text':"ジョーカーが選択されたので、最初のジョーカーの代わりとなる0~13の間の数字を入力してください。"}
    if self.joker_memory['text'] != '': # ジョーカーのあとの処理
      if not text_.isdecimal():
        return {'type':'turn_continue', 'text':'数字ではありません。数字を入れてください。'}
      if int(text_) > 13 or int(text_) < 0:
        return {'type':'turn_continue', 'text':'数字が0~13の間のではありません。0~13の間で記入してください。'}
      self.joker_memory['replace'].append(text_)
      if len(self.joker_memory['replace']) != self.joker_memory['text'].count('X'): # ジョーカー二枚つかってたとき
        return {'type':'turn_continue','text':'もう一枚のジョーカーの代わりとなる0~13の間の数字を入力してください'}
      text_ = self.joker_memory['text']
      self.joker_memory['text'] = ''
    player_input_list = []
    for char in text_:
      if char == '*' or char == '^' or char == '(' or char == ')':
        player_input_list.append({'char':char, 'num':char})
      elif not char in list(map(lambda x : x['char'], self.player[player_num_].hand)):
        self.player[player_num_].hand.extend(player_input_list)
        self.hand_sort()
        return {'type':'turn_continue','text':f'{char}が手札にありません！'}
      elif char == 'X':
        self.player[player_num_].hand.pop( # 削除
          int(
            list(map(lambda x : x['char'], self.player[player_num_].hand)).index(char)
          )
        )
        if text_ == 'X': #一枚出し最強
          player_input_list.append({'num': '1213', 'char': 'X'})
        else:
          player_input_list.append({'num': int(self.joker_memory['replace'].pop(0)), 'char': 'X'})
      else:
        player_input_list.append(
          self.player[player_num_].hand.pop(
            int(
              list(map(lambda x : x['char'], self.player[player_num_].hand)).index(char)
            )
          )
        )
    if self.gouseisu.gouseisu_flag:
      judge_num = ''.join(list(map(lambda x : str(x['num']), player_input_list)))
      judge_num = judge_num.replace('^', '**')
      if int(self.gouseisu.field['obj']['num']) != eval(judge_num):
        return_text = f"合成数として{self.gouseisu.field['obj']['num']}が入力されましたが、\n因数の計算結果が{eval(judge_num)}={text_}であり、異なっています。ペナルティを受け、相手にターンがわたります。"
        print(f"data.player_input 147 self.gouseisu.field['list']={self.gouseisu.field['list']}")
        self.player[player_num_].hand.extend(self.gouseisu.field['list'])
        for i in self.gouseisu.field['list']:
          self.draw(player_num_)
        self.player[player_num_].hand.extend([e for e in player_input_list if str(e['num']).isdecimal()])
        for i in [e for e in player_input_list if str(e['num']).isdecimal()]:
          self.draw(player_num_)
        self.gouseisu = gouseisu()
        self.draw_flag = False
        self.graveyard.extend(self.field)
        self.field = []
        self.turn = teki_num(player_num_)
        return {'type':'turn_end', 'text':return_text}
      judge_num = ''.join(list(map(lambda x : str(x['num']), player_input_list)))
      judge_num_ary = judge_num.replace('(', '').replace(')', '').replace('*', ' ').split()
      judge_num_ary = [e.replace('^', ' ').split() for e in judge_num_ary]
      for n in judge_num_ary:
        if not sympy.isprime(int(n[0])):
          self.player[player_num_].hand.extend(self.gouseisu.field['list'])
          # for i in self.gouseisu.field['list']:
          #   self.draw(player_num_)
          self.player[player_num_].hand.extend([e for e in player_input_list if str(e['num']).isdecimal()])
          # for i in [e for e in player_input_list if str(e['num']).isdecimal()]:
          #   self.draw(player_num_)
          # self.draw_flag = False
          # self.graveyard.extend(self.field)
          # self.field = []
          # self.turn = teki_num(player_num_)
          self.gouseisu = gouseisu()
          return {'type':'turn_end', 'text':f"因数として入力された{n[0]}は素数ではありませんでした。最初から入力をやり直してください"}
      self.graveyard.extend([e for e in player_input_list if str(e['num']).isdecimal()])
      player_input_obj = self.gouseisu.field['obj']
    else:
      player_input_obj =  {'char':''.join(list(map(lambda x : x['char'], player_input_list))), 'num':''.join(list(map(lambda x : str(x['num']), player_input_list)))}
    if self.field != []:
      field_obj =  {'char':''.join(list(map(lambda x : x['char'], self.field))), 'num':''.join(list(map(lambda x : str(x['num']), self.field)))}
      if len(field_obj['char']) != len(player_input_obj['char']):
        self.player[player_num_].hand.extend(player_input_list)
        return {'type':'turn_continue','text':'フィールドの札の枚数と出した札の枚数が違います'}
      if int(field_obj['num']) >= int(player_input_obj['num']) and not self.kakumei:
        self.player[player_num_].hand.extend(player_input_list)
        return {'type':'turn_continue','text':'フィールドの札の数のほうが大きいです'}
      if int(field_obj['num']) <= int(player_input_obj['num']) and self.kakumei:
        self.player[player_num_].hand.extend(player_input_list)
        return {'type':'turn_continue','text':'ラマヌジャン革命中です。フィールドの札の数のほうが小さいです'}
    if self.gouseisu.flag and not self.gouseisu.gouseisu_flag:
      print(f"data.player_input 183 player_input_list={player_input_list}")
      if sympy.isprime(int(player_input_obj['num'])):
        self.player[player_num_].hand.extend(player_input_list)
        return {'type':'turn_continue', 'text':f"合成数出しが指定されていますが{player_input_obj['num']}は素数です。合成数を記入してください。"}
      self.gouseisu.field['list'].extend(player_input_list)
      self.gouseisu.field['obj'] = {'char':player_input_obj['char'], 'num':player_input_obj['num']}
      print(f"data.player_input 186 self.gouseisu.field['list']={self.gouseisu.field['list']}")
      self.gouseisu.gouseisu_flag = True
      return {'type':'turn_continue', 'text':f"{player_input_obj['char']}が入力されました。\n素因数分解の結果を積は*,カッコは(),ベキは^で記入してください。"}
    self.draw_flag = False
    self.graveyard.extend(self.field)
    self.field = []
    self.turn = teki_num(player_num_)
    print(f"data.plyaer_input player_input_obj[num]={int(player_input_obj['num'])}")
    if sympy.isprime(int(player_input_obj['num'])) is False and player_input_obj['num'] != '57' and player_input_obj['num'] != '1729' and not self.gouseisu.flag:
      print('data.plyaer_input 素数ではなかった時')
      self.player[player_num_].hand.extend(player_input_list)
      for i in player_input_list:
        self.draw(player_num_)
      return {'type':'turn_end','text':f"{player_input_obj['num']}は素数ではありません。ペナルティーが発生しました。相手にターンが渡ります。"}
    umekomi_type = 'turn_end'
    if self.player[player_num_].hand == []: # 勝ちフラグ
      print('data.plyaer_input 勝利確定')
      self.turn = "0"
      umekomi_type = 'winner'
    if text_ == 'X':
      self.turn = player_num_
      self.graveyard.extend(player_input_list)
      return {'type':umekomi_type,'text':f"一枚出しジョーカーです。場が流れプレイヤー{player_num_}の番です。"}
    if self.gouseisu.flag:
      return_text = f"{self.gouseisu.field['obj']['num']}={text_}を合成数出しで出しました。相手にターンが渡ります。"
      self.field.extend(self.gouseisu.field['list'])
      self.gouseisu = gouseisu()
      return {'type':umekomi_type,'text':return_text}
    if sympy.isprime(int(player_input_obj['num'])) is True:
      print('data.plyaer_input 素数だったとき')
      self.field.extend(player_input_list)
      print(f"data.player_input 素数だったとき self.field={self.field}")
      return {'type':umekomi_type,'text':f"{player_input_obj['num']}は素数です！相手にターンが渡ります。"}
    if player_input_obj['num'] == '57':
      print('data.plyaer_input グロタン')
      self.turn = player_num_
      self.graveyard.extend(player_input_list)
      return {'type':umekomi_type,'text':f"グロタンディーク素数切りです。場が流れプレイヤー{player_num_}の番です。"}
    if player_input_obj['num'] == '1729':
      print('data.plyaer_input ラマヌジャン')
      self.kakumei = True
      self.field.extend(player_input_list)
      return {'type':umekomi_type,'text':f'ラマヌジャン革命です。今後は値が小さい数を出してください。相手にターンが渡ります。'}

a = game(player(0), player(0))
b = game(player(0), player(0))

def teki_num(e):
  print(f'teki_num: e={e}')
  if e == '1':
    return '2'
  if e == '2':
    return '1'
  return 'error'
