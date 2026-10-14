import os
from datetime import time, timedelta
from random import choice

import aiofiles
from nonebot import get_bots
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.helpers import Cooldown, CooldownIsolateLevel
from nonebot.exception import ActionFailed

from ATRI import TEMP_DIR
from ATRI.bot.utils import BotUtils
from ATRI.configs import Field, PluginConfig
from ATRI.exceptions import str_traceback
from ATRI.log import log
from ATRI.permission import ADMIN
from ATRI.service import Service
from ATRI.utils import request
from ATRI.utils.datetime import fromtimestamp, now
from ATRI.utils.img_editor import get_image_bytes

plugin = Service("每日新闻", "每日新闻订阅服务", "1.6.1", Service.ServiceType.FUNCTION)

_lmt_notice = [
    "慢...慢一..点❤",
    "冷静1下",
    "歇会歇会~~",
    "呜呜...别急",
    "太快了...受不了",
    "不要这么快呀",
]


class DailyNewsConfig(PluginConfig):
    groups = Field(list, [], "订阅群", item_type=str)
    hour = Field(int, 8, "每日推送小时", min=0, max=23)
    minute = Field(int, 0, "每日推送分钟", min=0, max=59)
    url = Field(str, "https://60s.viki.moe/v2/60s", "新闻接口地址")


config: DailyNewsConfig = plugin.add_plugin_config(DailyNewsConfig)

today_news = plugin.on_command(cmd="今日新闻", docs="查看今日新闻")


@today_news.handle(
    [
        Cooldown(
            60,
            prompt=choice(_lmt_notice),
            isolate_level=CooldownIsolateLevel.GROUP_USER,
        )
    ]
)
async def _():
    _, news = await get_news(False)
    try:
        await today_news.finish(news)
    except ActionFailed:
        await today_news.finish(
            MessageSegment.text(text="很遗憾，发送今日份新闻失败了捏")
        )


news_sub = plugin.on_command(
    cmd="每日新闻订阅", docs="管理本群的新闻订阅", permission=ADMIN
)


@news_sub.handle()
async def _(event: GroupMessageEvent):
    group_id = str(event.group_id)
    groups = config.get("groups", [])
    if group_id in groups:
        groups.remove(group_id)
        config.set("groups", groups)
        await news_sub.finish("本群每日新闻订阅已关闭")
    else:
        groups.append(group_id)
        config.set("groups", groups)
        await news_sub.finish("本群每日新闻订阅已开启")


async def daily_job():
    _, message = await get_news()
    for bot in get_bots().values():
        if type(bot) is Bot:
            group_list = await bot.get_group_list()
            for group in group_list:
                group_id = str(group["group_id"])
                if group_id in config.get("groups", []):
                    try:
                        await BotUtils.send_message(
                            bot=bot,
                            service="每日新闻",
                            group_id=group_id,
                            message=Message().append(message),
                        )
                    except ActionFailed:
                        log.warning(f"发送每日新闻至 {group_id} 失败")


plugin.scheduler_jobs().add_job(
    daily_job,
    "新闻订阅",
    "cron",
    hour=config.get("hour"),
    minute=config.get("minute"),
)


def delay_task():
    run_time = now() + timedelta(hours=4)
    if not (
        time(
            hour=(config.get("hour") - 4) % 24,
            minute=config.get("minute"),
        )
        <= run_time.time()
        <= time(
            hour=(config.get("hour") + 4) % 24,
            minute=config.get("minute"),
        )
    ):
        scheduler_jobs = plugin.scheduler_jobs()
        if scheduler_jobs.has_job("新闻订阅延时"):
            scheduler_jobs.remove_job("新闻订阅延时")
        scheduler_jobs.add_job(daily_job, "新闻订阅延时", "date", run_date=run_time)


async def get_news(task: bool = True) -> tuple[bool, MessageSegment]:
    path = TEMP_DIR / "news.png"
    if os.path.exists(path) and fromtimestamp(os.path.getmtime(path)) == get_now_date():
        return True, MessageSegment.image(get_image_bytes(path))
    retry = 0
    while retry < 3:
        try:
            resp = await request.get(config.get("url"))
            resp.raise_for_status()
            url_json = resp.json()
            if url_json["data"]["date"] != get_now_date().strftime("%Y-%m-%d"):
                break
            image_url = str(url_json["data"]["image"])
            resp = await request.get(image_url)
            resp.raise_for_status()
            content = resp.content
            async with aiofiles.open(path, "wb") as wf:
                await wf.write(content)
            return True, MessageSegment.image(get_image_bytes(path))
        except Exception as e:
            log.warning(f"第{retry + 1}次获取新闻错误:\n{str_traceback(e)}")
            retry += 1
    if task:
        delay_task()
    return False, MessageSegment.text(text="很遗憾，获取今日份新闻失败了捏")


def get_now_date():
    _now = now()
    custom_date = _now - timedelta(days=1) if _now.hour < config.get("hour") else _now
    return custom_date.date()
