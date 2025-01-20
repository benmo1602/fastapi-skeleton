from peewee import CharField, DateTimeField, IntegerField

from app.models.base_model import BaseModel
from app.providers.database import MOCK_USERS, myslq_settings


class User(BaseModel):
    class Meta:
        table_name = 'users'

    id = IntegerField(primary_key=True)
    username = CharField(max_length=50, unique=True)
    password = CharField()
    cellphone = CharField(max_length=20, null=True)
    email = CharField(unique=True)
    email_verified_at = DateTimeField(null=True)
    state = CharField(default='enabled')
    nickname = CharField()
    gender = CharField(default='unknown')
    avatar = CharField()

    @classmethod
    def get_or_none(cls, *query):
        if not myslq_settings.DB_USE:
            # 使用模拟数据
            for user in MOCK_USERS:
                if query[0].lhs.column == 'id' and user['id'] == query[0].rhs:
                    return cls(**user)
                if query[0].lhs.column == 'username' and user['username'] == query[0].rhs:
                    return cls(**user)
                if query[0].lhs.column == 'cellphone' and user['cellphone'] == query[0].rhs:
                    return cls(**user)
            return None

        return super().get_or_none(*query)

    def is_enabled(self):
        return self.state == 'enabled'
