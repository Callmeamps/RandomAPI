from data.supa import supabase_client

def load_chat_from_supabase(chat_id):
    chat, count = supabase_client.table('chats').select(chat_id).execute()
    if count is not None:
        return chat, count
    return chat

def save_chat_to_supabase(chat_id, thread):
    data, count = supabase_client.table('threads').insert({"chat_id": chat_id, "thread": thread}).execute()
    return {"data": data, "count": count}

def save_message_to_supabase(user_message, assitant_response, system=None, thread=None):
    data, count = supabase_client.table('messages').insert({
        "user_message": user_message,
        "assistant_message": assitant_response,
        "assistant_type": "Chat",
        "system_message": system if system else None,
        "thread_id": thread if thread else None,
        }).execute()
    return {"data": data, "count": count}

def remove_chat_from_supabase(chat_id):
    is_deleted = supabase_client.table('messages').select(chat_id).execute()
    if not is_deleted:
        supabase_client.table('messages').delete().match({"chat_id": chat_id}).execute()
    else:
        return {"error": "No chat found to delete"}

def get_threads():
    res = supabase_client.table('threads').select("*").execute()
    if res:
        return res
    return {"404 error": "No threads found"}

if __name__ == "__main__":
    pass
