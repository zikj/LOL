from lcu_driver import Connector
import LcuApi
import time
connector = Connector()


#-----------------------------------------------------------------------------
# 查看战绩
#-----------------------------------------------------------------------------
async def macth_history(connection):
  activedata = await connection.request('GET', '/lol-match-history/v3/matchlist/account/4124031491')
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
    summonerId =str(await LcuApi.get_summoner_data(connection))

    await LcuApi.create_custom_lobby(connection)
    await LcuApi.add_bots_team1(connection)
    await macth_history(connection)
    #await LcuApi.add_bots_team2(connection)
    # while True:
    #     time.sleep(1)
    #     state = LcuApi.get_active(token=connection.auth_key,address=connection.address)
    #     if state =="true":
    #         await get_chat(connection)
    #         print("--------------------启动牛马分析程序------------------------")

    #await LcuApi.get_accountid(token=connection.auth_key, address=connection.address, accountID=summonerId)

    #await LcuApi.get_team_session(connection.address,connection.auth_key)

#监听创建房间事件
@connector.ws.register('/lol-lobby/v2/lobby', event_types=('CREATE',))
async def icon_changed(connection, event):
    print(f'创建房间')

#监听房间更新事件
@connector.ws.register('/lol-lobby/v2/lobby', event_types=('UPDATE',))
async def icon_changed(connection, event):
    print(f'房间状态已跟新')







#-----------------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------------
connector.start()

