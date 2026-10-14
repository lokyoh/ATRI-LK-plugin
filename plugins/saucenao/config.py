from ATRI.configs import Field, PluginConfig


class SauceNAOConfig(PluginConfig):
    key = Field(str, "", "SauceNAO API Key", required=True)


config: SauceNAOConfig = SauceNAOConfig("以图搜图")
