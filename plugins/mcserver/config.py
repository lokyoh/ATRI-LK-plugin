from pydantic import Field

from ATRI.utils.model import BaseModel


class McServerConfig(BaseModel):
    server_dict: dict[str, str] = Field(default_factory=dict[str, str])
