from tortoise import fields
from tortoise.models import Model


class ThesaurusStoragor(Model):
    _id = fields.TextField()
    matcher = fields.TextField(null=True)
    result = fields.JSONField(null=True)
    need_at = fields.IntField(null=True)
    m_type = fields.IntField(null=True)
    group_id = fields.IntField(null=True)
    operator = fields.TextField(null=True)
    operator_id = fields.IntField(null=True)
    update_time = fields.DatetimeField(null=True)
    is_vote = fields.IntField(null=True)
    vote_list = fields.JSONField(null=True)

    class Meta:
        app = "thesaurusstoragor"


class ThesaurusAuditList(Model):
    _id = fields.TextField()
    matcher = fields.TextField(null=True)
    result = fields.JSONField(null=True)
    need_at = fields.IntField(null=True)
    m_type = fields.IntField(null=True)
    group_id = fields.IntField(null=True)
    operator = fields.TextField(null=True)
    operator_id = fields.IntField(null=True)
    update_time = fields.DatetimeField(null=True)
    is_vote = fields.IntField(null=True)
    vote_list = fields.JSONField(null=True)

    class Meta:
        app = "thesaurusauditlist"
