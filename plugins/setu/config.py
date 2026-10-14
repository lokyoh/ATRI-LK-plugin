from ATRI.configs import Field, PluginConfig


class SetuConfig(PluginConfig):
    reverse_proxy = Field(bool, True, "启用反向代理")
    reverse_proxy_domain = Field(str, "i.pixiv.re", "反向代理域名")


config: SetuConfig = SetuConfig("涩图")
