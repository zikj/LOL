import os
import re

#-----------------------------------------------------------------------------
# 获得召唤师数据
#-----------------------------------------------------------------------------
async def get_summoner_data(connection):
    data = await connection.request('GET', '/lol-summoner/v1/current-summoner')
    summoner = await data.json()
    summonerId= summoner['summonerId']
    print(f"displayName:    {summoner['displayName']}")
    print(f"summonerId:     {summoner['summonerId']}")
    print(f"puuid:          {summoner['puuid']}")
    print(connection.address)
    print(connection.auth_key)
    print("---------")
    return summonerId
#查找召唤师战绩
def get_accountid(token,address,accountID):
    str ="curl --http2 --insecure -u riot:"+token+" "+address+"/lol-match-history/v3/matchlist/account/"+accountID+" "+"-s"
    text1 = os.popen(str).read().encode('gbk').decode("utf-8")
    print(text1)


#进入选人界面后返回true，否则false：
def get_active(token,address):
    str ="curl --http2 --insecure -u riot:"+token+" "+address+"/lol-champ-select-legacy/v1/implementation-active -s"
    text = os.popen(str).read().encode('gbk').decode("utf-8")
    return text

#获取房间id
def get_team_session(token,address):
    str ="curl --http2 --insecure -u riot:"+token+" "+address+"/lol-champ-select/v1/session -s"
    text = os.popen(str).read().encode('gbk').decode("utf-8")
    pattern_lobbyID = '"id":"(.*?)"'
    #lobbyID = re.findall(pattern_lobbyID, text)[0]
    print(text)
    return text

#获取房间内对话消息拿到房间从成员id
def get_lobby_messages(token,address):
    lobbyId = get_team_session(token,address)
    str = "curl --http2 --insecure -u riot:" + token + " " + address + '/lol-chat/v1/conversations/'+lobbyId+'/'+"messages -s"
    text = os.popen(str).read().encode("gbk").decode("utf-8")
    pattern_gamersID = '"body":"joined_room","fromId":"(.*?)"'
    gamersID = re.findall(pattern_gamersID, text)
    print(gamersID)
    return gamersID

############################获取房间id
async def get_chat(token,address):
    str ="curl --http2 --insecure -u riot:"+token+" "+address+"/lol-chat/v1/conversations -s"
    text1 = os.popen(str).read().encode('gbk').decode("utf-8")
    print(text1)
#添加单个机器人
async def add_bots_team1(connection):
  soraka = {
    'championId':16,
    'botDifficulty':'EASY',
    'teamId':'100'
  }
  soraka1 = {
    'championId':51,
    'botDifficulty':'EASY',
    'teamId':'200'
  }
  await connection.request('POST', '/lol-lobby/v1/lobby/custom/bots', data=soraka)
  #await connection.request('POST', '/lol-lobby/v1/lobby/custom/bots', data=soraka1)


#批量添加机器人
async def add_bots_team2(connection):
  # 获取自定义模式电脑玩家列表
  # activedata = await connection.request('GET', '/lol-lobby/v2/lobby/custom/available-bots')
  # print(activedata)
  # champions = { bot['name']: bot['id'] for bot in await activedata.json()}

  team2 = ['10', '11', '12', '13', '15']

  for name in team2:
    bot = {'championId': name, 'botDifficulty': 'EASY', 'teamId': '200'}
    await connection.request('POST', '/lol-lobby/v1/lobby/custom/bots', data=bot)



# 创建训练模式 5V5 自定义房间
async def create_custom_lobby(connection):
  custom = {
    'customGameLobby': {
      'configuration': {
        'gameMode': 'PRACTICETOOL',
        'gameMutator': '',
        'gameServerRegion': '',
        'mapId': 11,
        'mutators': {'id': 1},
        'spectatorPolicy': 'AllAllowed',
        'teamSize': 5
      },
      'lobbyName': 'PRACTICETOOL',
      'lobbyPassword': ''
    },
    'isCustom': True
  }
  await connection.request('POST', '/lol-lobby/v2/lobby', data=custom)

#查看房间状态
def get_lobby(token,address):
    str ="curl --http2 --insecure -u riot:"+token+" "+address+"/lol-lobby/v2/lobby -s"
    text1 = os.popen(str).read().encode('gbk').decode("utf-8")
    print(text1)