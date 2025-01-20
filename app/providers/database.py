from contextvars import ContextVar
import os
import redis
from peewee import _ConnectionState, MySQLDatabase
from playhouse.pool import PooledMySQLDatabase
from pymongo import MongoClient

from config.database import myslq_settings, redis_settings, mongo_settings

# Check environment variables to decide whether to use databases
USE_DB = os.getenv('DB_USE', 'false').lower() == 'true'
USE_REDIS = os.getenv('REDIS_USE', 'false').lower() == 'true'
USE_MONGO = os.getenv('MONGO_USE', 'false').lower() == 'true'

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(_ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


async def reset_db_state():
    if myslq_settings.DB_USE:
        db._state._state.set(db_state_default.copy())
        db._state.reset()


# MySQL Database
if myslq_settings.DB_USE:
    db = MySQLDatabase(
        myslq_settings.DB_DATABASE,
        user=myslq_settings.DB_USER,
        host=myslq_settings.DB_HOST,
        password=myslq_settings.DB_PASSWORD,
        port=myslq_settings.DB_PORT
    )
    db._state = PeeweeConnectionState()
else:
    # Use fake data when DB is not used
    db = None  # Add your fake data logic here
    # Example: fake_data = [{'id': 1, 'name': 'Test'}]

# Redis
if redis_settings.REDIS_USE:
    redis_pool = redis.ConnectionPool(
        host=redis_settings.REDIS_HOST,
        port=redis_settings.REDIS_PORT,
        db=redis_settings.REDIS_DB,
        password=redis_settings.REDIS_PASSWORD,
        decode_responses=True
    )
    redis_client = redis.Redis(connection_pool=redis_pool)
else:
    # Use fake data when Redis is not used
    redis_pool = None
    redis_client = None  # Add your fake data logic here
    # Example: fake_cache = {}

# MongoDB
if mongo_settings.MONGO_USE:
    mongo_client = MongoClient(mongo_settings.MONGO_URI)
    mongo_db = mongo_client[mongo_settings.MONGO_DB]
else:
    # Use fake data when MongoDB is not used

    mongo_client = None  # Add your fake data logic here
    mongo_db = None
    # Example: fake_mongo_data = [{'id': 1, 'name': 'Test'}]

# 添加模拟数据
MOCK_USERS = [
    {"id": 1, "username": "fake_user1", "password": "$2b$12$qn3Hjh8zCfYsSnbqHBq63eXjaTwWs4r/SH3yLycDAOTFUi80em6Ju", "cellphone": "13800138000"},  # 密码: 123456
    {"id": 2, "username": "fake_user2", "password": "$2b$12$qn3Hjh8zCfYsSnbqHBq63eXjaTwWs4r/SH3yLycDAOTFUi80em6Ju", "cellphone": "13800138001"}   # 密码: 123456
]

MOCK_VERIFICATION_CODES = {}  # 模拟验证码存储
