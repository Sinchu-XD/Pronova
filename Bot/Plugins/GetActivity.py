import asyncio
from datetime import datetime
import pytz

from Bot.Database.Activity import get_gc_activity
from Bot.Database.Chats import get_all_chats


IST = pytz.timezone("Asia/Kolkata")


async def daily_gc_report(app):
    print("📊 Daily GC Report Started")

    while True:
        now = datetime.now(IST)

        # midnight check
        if now.hour == 0 and now.minute == 0:
            print("🕛 Sending daily reports")

            async for chat_id in get_all_chats():
                try:
                    data = await get_gc_activity(chat_id)

                    if not data:
                        continue

                    users = data.get("users", {})
                    total_messages = data.get("total_messages", 0)
                    active_users = len(users)

                    # top 3
                    top = sorted(
                        users.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:3]

                    text = f"""
📊 **Daily Group Activity**

👥 Active Users : {active_users}
💬 Total Messages : {total_messages}

🏆 **Top 3 Users**
"""

                    for i, (uid, count) in enumerate(top, start=1):
                        try:
                            user = await app.get_users(int(uid))
                            mention = user.mention
                        except:
                            mention = f"`{uid}`"

                        text += f"\n{i}. {mention} → {count}"

                    await app.send_message(chat_id, text)

                except Exception:
                    pass

            # wait so duplicate na ho
            await asyncio.sleep(60)

        await asyncio.sleep(20)
      
