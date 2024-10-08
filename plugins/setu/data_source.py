import re
from typing import Tuple
from nonebot.adapters.onebot.v11 import MessageSegment

from ATRI.utils import request
from ATRI.exceptions import RequestError

from .config import config
from .models import LoliconResponse, SetuInfo

_LOLICON_URL = "https://api.lolicon.app/setu/v2"


class Setu:
    def __init__(self, url: str):
        self.url = url

    @classmethod
    async def new(cls, tag: str = str()) -> Tuple[MessageSegment, SetuInfo]:
        """new 一个涩图

        Args:
            tag (str, optional): 附加 tag, 默认无

        Raises:
            RequestError: 涩图请求失败

        Returns:
            Tuple[MessageSegment, dict]: 涩图本体, 涩图信息
        """
        url = _LOLICON_URL + (f"?tag={tag}" if tag else str())
        try:
            req = await request.get(url)
        except Exception:
            raise RequestError("setu: 请求失败")

        raw_data = LoliconResponse.parse_obj(req.json()).data
        if not raw_data:
            return MessageSegment.text(str()), SetuInfo(
                title=str(), pid=int(), url=str()
            )
        data = raw_data[0]
        title = data.title
        pid = data.pid
        url = data.urls.original

        if config.reverse_proxy:
            patt = "://(.*?)/"
            domain = re.findall(patt, url)[0]
            url = url.replace(domain, config.reverse_proxy_domain)

        setu_data = SetuInfo(title=title, pid=pid, url=url)
        setu = MessageSegment.image(
            file=url,
            timeout=114514,
        )

        return setu, setu_data
