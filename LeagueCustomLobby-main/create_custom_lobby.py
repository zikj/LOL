from lcu_driver import Connector
import LcuApi

connector = Connector()

#-----------------------------------------------------------------------------
# 获得召唤师数据
#-----------------------------------------------------------------------------
async def get_summoner_data(connection):
    data = await connection.request('GET', '/lol-summoner/v1/current-summoner')
    summoner = await data.json()
    print(f"displayName:    {summoner['displayName']}")
    print(f"summonerId:     {summoner['summonerId']}")
    print(f"puuid:          {summoner['puuid']}")
    print(summoner)
    print(connection.address)
    print(connection.auth_key)
    print("---------")


#-----------------------------------------------------------------------------
#  lockfile
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# 创建训练模式 5V5 自定义房间
#-----------------------------------------------------------------------------
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

#-----------------------------------------------------------------------------
# 添加单个机器人
#-----------------------------------------------------------------------------
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

#-----------------------------------------------------------------------------
# 批量添加机器人
#-----------------------------------------------------------------------------
async def add_bots_team2(connection):
  # 获取自定义模式电脑玩家列表
  # activedata = await connection.request('GET', '/lol-lobby/v2/lobby/custom/available-bots')
  # print(activedata)
  # champions = { bot['name']: bot['id'] for bot in await activedata.json()}

  team2 = ['10', '11', '12', '13', '15']

  for name in team2:
    bot = {'championId': name, 'botDifficulty': 'EASY', 'teamId': '200'}
    await connection.request('POST', '/lol-lobby/v1/lobby/custom/bots', data=bot)

#-----------------------------------------------------------------------------
# 查看战绩
#-----------------------------------------------------------------------------
async def macth_history(connection):
  # 获取自定义模式电脑玩家列表
  activedata = await connection.request('GET', '/lol-match-history/v3/matchlist/account/4050855651')
  macth = await activedata.json()
  print(macth)

##获取房间内最新的一条消息
async  def get_chat(connection):
    activedata = await connection.request('GET','/lol-chat/v1/conversations/')
    macth = await activedata.json()
    print(macth)
#-----------------------------------------------------------------------------
# websocket
#-----------------------------------------------------------------------------
@connector.ready
async def connect(connection):
  #await get_summoner_data(connection)
  #await create_custom_lobby(connection)
  #await add_bots_team1(connection)
  #await add_bots_team2(connection)
  #await get_chat(connection)
  await LcuApi.get_accountid(connection.address,connection.auth_key)

#监听创建房间事件
@connector.ws.register('/lol-lobby/v2/lobby', event_types=('CREATE',))
async def icon_changed(connection, event):
    print(f'创建房间')
#监听房间更新事件
@connector.ws.register('/lol-lobby/v2/lobby', event_types=('UPDATE',))
async def icon_changed(connection, event):
    print(f'房间状态已跟新')

#监听头像改变事件/lol-game-data/assets/v1/profile-icons/4804.jpg
@connector.ws.register('/lol-game-data/assets/v1/profile-icons/4804.jpg', event_types=('UPDATE',))
async def icon_changed(connection, event):
    print(f'头像更换')


#-----------------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------------
connector.start()

