from random import choice

from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11.helpers import Cooldown
from nonebot.internal.params import ArgPlainText
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

from ATRI.service import Service

from .data_source import check_mc_status

plugin = Service("MC服务器").document("查看MC服务器状态").type(Service.ServiceType.FUNCTION).version("1.1.1")

_lmt_notice = ["慢...慢一..点❤", "冷静1下", "歇会歇会~~", "呜呜...别急", "太快了...受不了", "不要这么快呀"]

mc = plugin.on_command(cmd="/mc", docs="查看MINECRAFT服务器状态")

s_names = {}


@mc.handle([Cooldown(30, prompt=choice(_lmt_notice))])
async def _(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("server_name", args)


@mc.got("server_name", "要查询那个服务器呢")
async def _(s_name=ArgPlainText("server_name")):
    s_name = s_name.replace(" ", "")
    msg = await check_mc_status(s_name, s_names[s_name] if s_name in s_names else "我的世界服务器")
    await mc.finish(msg)
