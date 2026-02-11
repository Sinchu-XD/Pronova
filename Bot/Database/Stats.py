from datetime import datetime, timedelta
from .Core import db


def today():
    return datetime.utcnow().strftime("%d-%m-%Y")


# lifetime
async def inc_lifetime(key):
    await db.lifetime.update_one(
        {"_id": key},
        {"$inc": {"count": 1}},
        upsert=True,
    )


async def get_lifetime(key):
    data = await db.lifetime.find_one({"_id": key})
    return data["count"] if data else 0


# daily
async def inc_daily(key):
    await db.daily.update_one(
        {"date": today()},
        {"$inc": {key: 1}},
        upsert=True,
    )


async def sum_range(days, key):
    total = 0
    for i in range(days):
        d = datetime.utcnow() - timedelta(days=i)
        data = await db.daily.find_one({"date": d.strftime("%d-%m-%Y")})
        if data:
            total += data.get(key, 0)
    return total
  
