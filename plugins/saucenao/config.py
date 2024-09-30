from ATRI.configs import PluginConfig
from ATRI.utils.model import BaseModel


class SauceNAO(BaseModel):
    key: str


config: SauceNAO = PluginConfig("以图搜图", SauceNAO).config()
