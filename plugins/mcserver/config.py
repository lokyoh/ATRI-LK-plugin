from ATRI.configs import Field, PluginConfig


class McServerConfig(PluginConfig):
    server_dict = Field(
        dict,
        {},
        "服务器地址",
        key_field=Field(str, "", "服务器名称"),
        item_type=Field(str, "", "服务器IP地址"),
    )
