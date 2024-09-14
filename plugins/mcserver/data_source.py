import re
from mcstatus import JavaServer


async def check_mc_status(s_name: str, name: str):
    try:
        js = await JavaServer.async_lookup(name, timeout=5)
        status = js.status()
        description = "获取介绍失败"
        if status.description.strip():
            description = re.sub(r'§.', '', status.description)
        online = f"{status.players.online}/{status.players.max}"
        player_list = []
        if status.players.online:
            if status.players.sample:
                player_list = [
                    p.name
                    for p in status.players.sample
                    if p.id != "00000000-0000-0000-0000-000000000000"
                ]
            if player_list:
                player_list = ", ".join(player_list)
            else:
                player_list = "没返回玩家列表"
        else:
            player_list = "没人在线"
        msg = f"{s_name}\n{name}\n{description}\n在线：{online}\n◤ {player_list} ◢"
    except Exception as e:
        msg = f"名称：{s_name} 查询失败！\n错误：{repr(e)}"
    return msg
