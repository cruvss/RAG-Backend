import redis
import json
from app.config import REDIS_CONFIG

r = redis.Redis(**REDIS_CONFIG)

def store_message(session_id: str, user_input: str, bot_response: str):
    msg = {"user": user_input, "bot": bot_response}
    r.rpush(session_id, json.dumps(msg))

def fetch_history(session_id: str, limit: int = 5):
    messages = r.lrange(session_id, -limit, -1)
    return [json.loads(m) for m in messages]


