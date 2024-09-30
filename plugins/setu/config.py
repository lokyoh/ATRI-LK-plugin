from ATRI.configs import PluginConfig
from ATRI.utils.model import BaseModel


class Setu(BaseModel):
    reverse_proxy: bool = True
    reverse_proxy_domain: str = "i.pixiv.re"


config: Setu = PluginConfig("涩图", Setu).config()
