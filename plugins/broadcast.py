# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import datetime, time, asyncio
from pyrogram import Client, filters
from database.users_chats_db import db
from info import ADMINS

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def pm_broadcast(bot, message):
    b_msg = await bot.ask(chat_id=message.from_user.id, text="Now Send Me Your Broadcast Message")
    try:
        users = await db.get_all_users()
        sts = await message.reply_text('Broadcasting your messages...')
        start_time = time.time()
        total_users = await db.total_users_count()
        done = 0
        blocked = 0
        deleted = 0
        failed = 0
        success = 0

        async for user in users:
            if 'id' in user:
                try:
                    sent = await b_msg.copy(chat_id=int(user['id']))
                    try:
                        await bot.pin_chat_message(chat_id=int(user['id']), message_id=sent.id, disable_notification=False)
                    except:
                        pass
                    success += 1
                except Exception as e:
                    if "blocked" in str(e).lower():
                        blocked += 1
                    elif "chat not found" in str(e).lower():
                        deleted += 1
                    else:
                        failed += 1
                done += 1
                if not done % 20:
                    await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")
            else:
                done += 1
                failed += 1
                if not done % 20:
                    await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")

        time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
        await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users: {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")
    except Exception as e:
        print(f"error: {e}")


@Client.on_message(filters.command("grp_broadcast") & filters.user(ADMINS))
async def broadcast_group(bot, message):
    b_msg = await bot.ask(chat_id=message.from_user.id, text="Now Send Me Your Broadcast Message")
    groups = await db.get_all_chats()
    sts = await message.reply_text(text='Broadcasting your messages To Groups...')
    start_time = time.time()
    total_groups = await db.total_chat_count()
    done = 0
    failed = 0
    success = 0

    async for group in groups:
        try:
            sent = await b_msg.copy(chat_id=int(group['id']))
            try:
                await bot.pin_chat_message(chat_id=int(group['id']), message_id=sent.id, disable_notification=False)
            except:
                pass
            success += 1
        except:
            failed += 1
        done += 1
        if not done % 20:
            await sts.edit(f"Broadcast in progress:\n\nTotal Groups {total_groups}\nCompleted: {done} / {total_groups}\nSuccess: {success}")

    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Groups {total_groups}\nCompleted: {done} / {total_groups}\nSuccess: {success}")
