from nonebot.adapters.onebot.v11 import Message
from nonebot.internal.params import ArgPlainText
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

from ATRI.service import Service

from .config import McServerConfig
from .data_source import check_mc_status

plugin = Service(
    "MC服务器",
    "查看MC服务器状态",
    "1.2.0",
    Service.ServiceType.FUNCTION,
)

config: McServerConfig = plugin.add_plugin_config(McServerConfig).config

mc = plugin.on_command(cmd="mc", docs="查看MINECRAFT服务器状态")


@mc.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("server_name", args)


@mc.got("server_name", "要查询那个服务器呢")
async def _(s_name=ArgPlainText("server_name")):
    s_name = s_name.replace(" ", "").replace("：", ":")
    for server_name, server_ip in config.server_dict:
        if server_name == s_name or server_ip == s_name:
            msg = await check_mc_status(server_ip, server_name)
            await mc.finish(msg)
            return
    msg = await check_mc_status(s_name, "MineCraft服务器")
    await mc.finish(msg)
