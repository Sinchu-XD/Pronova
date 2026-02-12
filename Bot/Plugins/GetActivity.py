import asyncio
from datetime import datetime
import pytz

from Bot.Database.Activity import get_gc_activity
from Bot.Database.Chats import get_all_chats
from Bot.Helper.Font import sc


IST = pytz.timezone("Asia/Kolkata")

last_sent_date = None
USER_CACHE = {}


async def daily_gc_report(app):
    global last_sent_date

    print("📊 Daily GC Report System Started")

    while True:
        try:
            now = datetime.now(IST)
            today = now.strftime("%d-%m-%Y")

            # run once after midnight
            if now.hour == 0 and last_sent_date != today:
                print("🕛 Sending Daily GC Reports")
                last_sent_date = today

                async for chat_id in get_all_chats():
                    try:
                        data = await get_gc_activity(chat_id)
                        if not data:
                            continue

                        users = data.get("users", {})
                        total_messages = int(data.get("total_messages", 0))

                        if not users and not total_messages:
                            continue

                        active_users = len(users)

                        # ===== GROUP NAME =====
                        try:
                            chat = await app.get_chat(chat_id)
                            gname = chat.title
                        except:
                            gname = str(chat_id)

                        # ===== TOP 3 =====
                        top = sorted(
                            users.items(),
                            key=lambda x: x[1],
                            reverse=True
                        )[:3]

                        text = f"""
📊 Daily Activity Report

🏠 Group : {gname}

👥 Active Users : {active_users}
💬 Total Messages : {total_messages}

🏆 Top 3 Users
"""

                        for i, (uid, count) in enumerate(top, start=1):
                            try:
                                uid = int(uid)

                                if uid in USER_CACHE:
                                    mention = USER_CACHE[uid]
                                else:
                                    user = await app.get_users(uid)
                                    mention = user.mention
                                    USER_CACHE[uid] = mention

                            except:
                                mention = f"`{uid}`"

                            text += f"\n{i}. {mention} → {count}"

                        await app.send_message(chat_id, sc(text))

                        # flood safety
                        await asyncio.sleep(2)

                    except Exception as e:
                        print(f"Report Error in {chat_id}:", e)
                        continue

                # avoid repeat trigger
                await asyncio.sleep(600)

        except Exception as e:
            print("Daily System Error:", e)

        await asyncio.sleep(30)
        
