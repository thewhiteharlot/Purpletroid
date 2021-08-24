# ported from kensurBot to ultroid by @Kakashi_HTK(tg)/@ashwinstr(gh)
"""
✘ Commands Available -
"`.fban_ <id/username> <reason>`"
"\nUsage: Bans user from connected federations."
"\nYou can reply to the user whom you want to fban or manually pass the username/id."
"\n`.fbanp` does the same but forwards the replied message as proof to FBAN_LOG_CHANNEL."
"\n\n`>.unfban <id/username> <reason>`"
"\nUsage: Same as fban but unbans the user"
"\n\n`>.fedlog <public channel ID (optional)>`"
"\nUsage: Adds channel as FBAN_LOG_CHANNEL"
"\n\n>`.addf <name>`"
"\nUsage: Adds current group and stores it as <name> in connected federations."
"\nAdding one group is enough for one federation."
"\n\n>`.delf`"
"\nUsage: Removes current group from connected federations."
"\n\n>`.listf`"
"\nUsage: Lists all connected federations by specified name."
"\n\n>`.listidf`"
"\nUsage: Lists all connected federations by specified name and ID."
"\n\n>`.clearf`"
"\nUsage: Disconnects from all connected federations. Use it carefully."
"""

from . import *



@ultroid_cmd(pattern=r"addf ?(.*)", ignore_dualmode=True, groups_only=True)
async def addf_(event):
    await event.edit("`Checking the list of connected federations...`")
    chat_id = event.chat_id
    name_ = event.pattern_match.group(1)
    if udB.get("FLIST"):
        flist = eval(Redis("FLIST"))
    else:
        flist = ""
    verb = "added"
    updated = False
    try:
        if flist["chat_id"] == chat_id:
            flist["chat_name"] = name_
            verb = "updated"
            updated = True
            udB.delete("FLIST")
            udB.append("FLIST", str(flist))
    except:
        int = 0
        end = len(flist)
        try:
            for one in flist:
                if one["chat_id"] == chat_id:
                    one["chat_name"] = name_
                    verb = "updated"
                    updated = True
                    udB.delete("FLIST")
                    udB.append("FLIST", str(flist))
        except:
            await event.edit("`Something unexpected happened...`")
            return
    if updated:
        await event.edit(f"• **'{chat_id}' - {name_}** {verb} in FEDLIST.")
        return
    if flist != "":
        udB.append("FLIST", ", ")
    entry = {"chat_id": chat_id, "chat_name": name_}
    udB.append("FLIST", str(entry))
    await event.edit(f"• **'{chat_id}' - {name_}** {verb} in FEDLIST.")

    
@ultroid_cmd(pattern=r"delf ?(.*)", ignore_dualmode=True, groups_only=True)
async def delf_(event):
    await event.edit("`Checking the list of connected federations...`") 
    chat_id = event.chat_id
    if udB.get("FLIST"):
        flist = eval(Redis("FLIST"))
    else:
        await event.edit("`FEDLIST is empty...`")
        return
    once = True
    found = False
    try:
        chat_id_1 = flist["chat_id"]
        chat_n_1 = flist["chat_name"]
        if chat_id_1 == chat_id:
            udB.delete("FLIST")
            await event.edit(f"'`{chat_id}`' - **{chat_n_1}** removed from FEDLIST.")
        else:
            await event.edit("`This chat doesn't exist in FEDLIST...`")
        return
    except:
        once = True
        deleted = False
        try:
            for one in flist:
                if not once:
                    udB.append("FLIST_temp", ", ")
                if one["chat_id"] != chat_id:
                    udB.append("FLIST_temp", str(one))
                    once = False
                else:
                    deleted = True
                    deleted_n = one["chat_name"]
        except:
            await event.edit("`Something unexpected happened...`")
            return
    udB.delete("FLIST")
    temp = eval(Redis("FLIST_temp"))
    udB.append("FLIST", str(temp))
    udB.delete("FLIST_temp")
    if deleted:
        await event.edit(f"'`{chat_id}` - **{deleted_n}** removed from FEDLIST.")
    else:
        await event.edit("`This chat doesn't exist in FEDLIST...`")


@ultroid_cmd(pattern=r"listf ?(.*)", ignore_dualmode=True)
async def listf_(event):
    await event.edit("`Getting the list of connected federations...`")
    if udB.get("FLIST"):
        flist = eval(Redis("FLIST"))
    else:
        await event.edit("`FEDLIST is empty...`")
        return
    fname_ = ""
    try:
        chat_n_1 = flist["chat_name"]
        total = 1
        fname_ = f"• FED: **{chat_n_1}**"
    except:
        total = 0
        for name_ in flist:
            chat_n = name_["chat_name"]
            total += 1
            fname_ += f"• FED: **{chat_n}**\n"
    list_ = f"**Connected federations:** [**{total}**]"
    await event.edit(f"{list_}\n\n{fname_}") 


@ultroid_cmd(pattern=r"listidf ?(.*)", ignore_dualmode=True)
async def listf_(event):
    await event.edit("`Getting the list of connected federations...`")
    if udB.get("FLIST"):
        flist = eval(Redis("FLIST"))
    else:
        await event.edit("`FEDLIST is empty...`")
        return
    fname_ = ""
    try:
        chat_n_1 = flist["chat_name"]
        chat_id_1 = flist["chat_id"]
        total = 1
        fname_ = f"• FED: '`{chat_id_1}`' - **{chat_n_1}**"
    except:
        total = 0
        for name_ in flist:
            chat_n = name_["chat_name"]
            chat_id = name_["chat_id"]
            total += 1
            fname_ += f"• FED: '`{chat_id}`' - **{chat_n}**\n"
    list_ = f"**Connected federations:** [**{total}**]"
    await event.edit(f"{list_}\n\n{fname_}")

    

@ultroid_cmd(pattern=r"clearf ?(.*)", ignore_dualmode=True)
async def clearf_(event):
    await event.edit("`Deleting all connected federations...`")
    try:
        udB.delete("FLIST")
    except:
        await event.edit("`Something unexpected happened...`")
        return
    await event.edit("**Cleared the FEDLIST.**")


@ultroid_cmd(pattern=r"fedlog ?(.*)", ignore_dualmode=True)
async def fedlog_c(event):
    id_ = event.pattern_match.group(1) or event.chat_id
    await event.edit(f"Adding channel '`{id_}`'as FBAN_LOG_CHANNEL...")
    if not id_:
        await event.edit("`Please provide a channel ID...`")
        return
    id_ = int(id_)
    channel_ = await event.client.get_entity(id_)
    if channel_.first_name:
        await event.edit("`Doesn't work with private chats...`")
        return
    if not (channel_.broadcast or id_.isdigit):
        await event.edit(f"Input '`{id_}`' is not a channel, please provide a proper channel ID...")
        return
    if not channel_.username:
        await event.edit("Provide a **public** channel ID...")
        return
    udB.delete("FBAN_LOG_CHANNEL")
    udB.set("FBAN_LOG_CHANNEL", int(id_))
    await event.edit(f"**FBAN_LOG_CHANNEL** set to '`{id_}`'.")
    

@ultroid_cmd(pattern=r"fban_ ?(.*)", ignore_dualmode=True)
async def fban_normal(event):
    await event.edit("`Fbanning...`")
    log_channel = udB.get("LOG_CHANNEL")
    if udB.get("FBAN_LOG_CHANNEL"):
        log_c = udB.get("FBAN_LOG_CHANNEL")
    else:
        log_c = log_channel
    reply_userid = False
    if event.reply_to_msg_id:
        reply_userid = True
        reply_ = await event.get_reply_message()
        me_ = await event.client.get_me()
        if reply_.sender_id == (me_.id or OWNER_ID):
            reply_userid = False
    input_ = event.text.split(" ", 2)
    if not reply_userid:
        try:
            user_ = input_[1]
        except:
            await event.edit("Please provide a user to fban...")
            return
        try:
            reason_ = input_[2]
        except:
            reason_ = "Not specified"
    else:
        user_ = reply_.sender_id
        try:
            reason_ = input[1]
        except:
            reason_ = "Not specified"
    if user_.isdigit:
        user_ = int(user_)
    try:
        user_e = await event.client.get_entity(user_)
        user_id = user_e.id
        user_n = " ".join([user_e.first_name, user_e.last_name or ""])
    except:
        await event.edit(f"Couldn't find user `{user_}`, proceeding with fban, it might fail...")
        user_id = user_
        user_n = "Unkown"
    flist = eval(Redis("FLIST"))
    total = 0
    failed = []
    try:
        flist_id = flist["chat_id"]
        flist_name = flist["chat_name"]
        total += 1
        try:
            await event.client.send_message(
                int(flist_id),
                f"/fban {user_id} {reason_}"
            )
        except:
            await event.edit(f"Fban complete...\nUser: `{user_id}`\nStatus: **{flist_name}** - failed")
            await event.client.send_message(
                int(log_channel),
                f"Failed to fban in '`{flist_id}`' - **{flist_name}**, check if the group ID is correct..."
            )
            return
    except:
        for one in flist:
            chat_id = one["chat_id"]
            chat_n = one["chat_name"]
            try:
                await event.client.send_message(
                    int(chat_id),
                    f"/fban {user_id} {reason_}"
                )
            except:
                failed.append(f"• '`{chat_id}`' - **{chat_n}**")
    user_link = f"[{user_n}](tg://user?id={user_id})"
    msg_ = f"Fbanned **{user_link}**...\n**User ID:** `{user_id}`\n**Reason:** {reason_}"
    await event.edit(
        msg_
    )
    await event.client.send_message(
        int(log_c),
        msg_
    )
    failed = "\n".join(failed)
    if not failed:
        return
    await event.client.send_message(
        int(log_channel),
        f"**Failed** to fban user `{user_id}` in following feds:\n\n{failed}"
    )


@ultroid_cmd(pattern=r"fbanp ?(.*)", ignore_dualmode=True)
async def fbanp_(event):
    await event.edit("`Fbanning...`")
    if udB.get("FBAN_LOG_CHANNEL"):
        log_c = udB.get("FBAN_LOG_CHANNEL")
    else:
        await event.edit("`Please add FBAN_LOG_CHANNEL to log proofs...`")
        return
    log_channel = udB.get("LOG_CHANNEL")
    if event.reply_to_msg_id:
        reply_userid = True
        reply_ = await event.get_reply_message()
        me_ = await event.client.get_me()
        if reply_.sender_id == (me_.id or OWNER_ID):
            reply_userid = False
    else:
        await event.edit("`Reply to proof to fban...`")
        return
    input_ = event.text.split(" ", 2)
    if not reply_userid:
        try:
            user_ = input_[1]
        except:
            await event.edit("Please provide a user to fban...")
            return
        try:
            reason_ = input_[2]
        except:
            reason_ = "Not specified"
    else:
        user_ = reply_.sender_id
        try:
            reason_ = input[1]
        except:
            reason_ = "Not specified"
    if user_.isdigit:
        user_ = int(user_)
    try:
        user_e = await event.client.get_entity(user_)
        user_id = user_e.id
        user_n = " ".join([user_e.first_name, user_e.last_name or ""])
    except:
        await event.edit(f"Couldn't find user `{user_}`, proceeding with fban, it might fail...")
        user_id = user_
        user_n = "Unkown"
    flist = eval(Redis("FLIST"))
    total = 0
    failed = []
    proof_ = await event.client.forward_messages(
        int(log_c),
        reply_,
        silent=True
    )
    proof_u = (await event.client.get_entity(int(log_c))).username
    proof_link = f"https://t.me/{proof_u}/{proof_.id}"
    reason_ = f"{reason_}" + " || {" + f"{proof_link}" + "}"
    try:
        flist_id = flist["chat_id"]
        flist_name = flist["chat_name"]
        total += 1
        try:
            await event.client.send_message(
                int(flist_id),
                f"/fban {user_id} {reason_}",
                link_preview=False
            )
        except:
            await event.edit(f"Fban complete...\nUser: `{user_id}`\nStatus: **{flist_name}** - failed")
            await event.client.send_message(
                int(log_channel),
                f"Failed to fban in '`{flist_id}`' - **{flist_name}**, check if the group ID is correct...",
                link_preview=False
            )
            return
    except:
        for one in flist:
            chat_id = one["chat_id"]
            chat_n = one["chat_name"]
            try:
                await event.client.send_message(
                    int(chat_id),
                    f"/fban {user_id} {reason_}",
                    link_preview=False
                )
            except:
                failed.append(f"• '`{chat_id}`' - **{chat_n}**")
    user_link = f"[{user_n}](tg://user?id={user_id})"
    msg_ = f"Fbanned **{user_link}**\n**User ID:** `{user_id}`\n**Reason:** {reason_}"
    await event.edit(
        msg_
    )
    await event.client.send_message(
        int(log_c),
        msg_,
        link_preview=False
    )
    failed = "\n".join(failed)
    if not failed:
        return
    await event.client.send_message(
        int(log_channel),
        f"**Failed** to fban user `{user_id}` in following feds:\n\n{failed}"
    )

