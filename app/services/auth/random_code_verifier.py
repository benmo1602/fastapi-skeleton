from app.providers.database import redis_pool, redis_settings, MOCK_VERIFICATION_CODES
import redis
import random


def make(key: str) -> str:
    """
    生成验证码
    """
    code = str(random.randint(100000, 999999))
    print(redis_settings.REDIS_USE) # 是否启用redis
    if redis_settings.REDIS_USE:
        redis_client = redis.Redis(connection_pool=redis_pool)
        redis_client.set(f"verification_code:{key}", code, ex=300)  # 5分钟过期
    else:
        # 使用模拟存储
        MOCK_VERIFICATION_CODES[key] = code

    return code


def check(key: str, code: str) -> bool:
    """
    验证验证码
    """
    if redis_settings.REDIS_USE:
        redis_client = redis.Redis(connection_pool=redis_pool)
        stored_code = redis_client.get(f"verification_code:{key}")
        return stored_code and stored_code.decode() == code
    else:
        # 使用模拟存储
        return MOCK_VERIFICATION_CODES.get(key) == code
