import os
import re
#获取port和token
token = "C2plxyyE0R-n260uG65smg"
address = "https://127.0.0.1:56865"
def get_accountid(token,address):
    str ="curl --http2 --insecure -u riot:"+token+" "+address+"/lol-match-history/v3/matchlist/account/4050855651 -s"
    text1 = os.popen(str).read().encode('gbk').decode("utf-8")
    print(text1)
get_accountid(token,address)