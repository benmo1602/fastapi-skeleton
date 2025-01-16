from contextvars import ContextVar

import redis
from peewee import _ConnectionState, MySQLDatabase
from playhouse.pool import PooledMySQLDatabase

from config.database import myslq_settings, redis_settings, mongo_settings

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
    db._state._state.set(db_state_default.copy())
    db._state.reset()


db = MySQLDatabase(
    myslq_settings.DB_DATABASE,
    user=myslq_settings.DB_USER,
    host=myslq_settings.DB_HOST,
    password=myslq_settings.DB_PASSWORD,
    port=myslq_settings.DB_PORT
)

db._state = PeeweeConnectionState()

# redis
# redis_client = redis.Redis(
#     host=redis_settings.REDIS_HOST,
#     port=redis_settings.REDIS_PORT,
#     db=redis_settings.REDIS_DB,
#     password=redis_settings.REDIS_PASSWORD,
#     decode_responses=True
# )
redis_pool = redis.ConnectionPool(
    host=redis_settings.REDIS_HOST,
    port=redis_settings.REDIS_PORT,
    db=redis_settings.REDIS_DB,
    password=redis_settings.REDIS_PASSWORD,
    decode_responses=True
)
redis_client = redis.Redis(connection_pool=redis_pool)


# mongodb
from pymongo import MongoClient

# MongoDB client connection using URI
mongo_client = MongoClient(mongo_settings.MONGO_URI)
# Access the specified database
mongo_db = mongo_client[mongo_settings.MONGO_DB]
