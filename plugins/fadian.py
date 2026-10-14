import json
import random

import anyio
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.helpers import Cooldown
from nonebot.adapters.onebot.v11.message import Message
from nonebot.matcher import Matcher
from nonebot.params import Arg, CommandArg

from ATRI import TEXT_DIR
from ATRI.service import Service
from ATRI.system.lkapi import lk_util

daily_fa_dian = Service(
    "每日发癫",
    "不每天对Ta发癫很难受呀！",
    "1.0.2",
    Service.ServiceType.ENTERTAINMENT,
    "l_o_o_k",
)

fa_dian = daily_fa_dian.on_command(
    "每日发癫", docs="不每天对Ta发癫很难受呀！", aliases={"每日发电", "发电", "发癫"}
)


@fa_dian.handle([Cooldown(60)])
async def _(matcher: Matcher, args: Message = CommandArg()):
    if args:
        matcher.set_arg("fa_dian_name", args)


@fa_dian.got("fa_dian_name", prompt="所以你要对谁发癫呢")
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = Arg("fa_dian_name")):
    cost = msg.extract_plain_text()
    for segment in msg:
        if segment.type == "at":
            qq = str(segment.data["qq"])
            if not qq.isdigit():
                continue
            elif lk_util.is_valid_user(qq):
                cost = lk_util.get_name(qq)
            else:
                info = await bot.get_group_member_info(
                    group_id=event.group_id, user_id=int(qq)
                )
                cost = info["nickname"]
            break
    if not cost or not cost.strip():
        await fa_dian.finish("没有检测到对象")
    file_path = TEXT_DIR / "fa_dian.json"
    async with await anyio.open_file(file_path, "r", encoding="utf-8") as f:
        content = await f.read()
    nami = json.loads(content)["post"]
    random_post = random.choice(nami).replace("阿咪", cost)
    await fa_dian.finish(f"{random_post}\n大家快来看看，又有🦐头仁在这发癫了")
