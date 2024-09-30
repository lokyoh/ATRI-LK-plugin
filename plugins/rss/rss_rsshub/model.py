from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class RssRsshubSubcription(Model):
    _id = fields.TextField()
    group_id = fields.IntField(null=True)
    title = fields.TextField(null=True)
    raw_link = fields.TextField(null=True)
    rss_link = fields.TextField(null=True)
    discription = fields.TextField(null=True)
    update_time = fields.DatetimeField(default=datetime.fromordinal(1))

    class Meta:
        app = "rssrsshubsubscription"
