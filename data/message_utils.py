from data.supa import supabase_client

def load_chat_from_supabase(chat_id):
    chat, count = supabase_client.table('chats').select(chat_id).execute()
    if count is not None:
        return chat, count
    return chat

def save_chat_to_supabase(chat_id, thread):
    data, count = supabase_client.table('threads').insert({"chat_id": chat_id, "thread": thread}).execute()
    return {"data": data, "count": count}

def save_message_to_supabase(user_message, assitant_response, system=None):
    data, count = supabase_client.table('messages').insert({"system": system, "user": user_message, "assistant": assitant_response}).execute()
    return {"data": data, "count": count}

def remove_chat_from_supabase(chat_id):
    is_deleted = supabase_client.table('messages').select(chat_id).execute()
    if not is_deleted:
        supabase_client.table('messages').delete().match({"chat_id": chat_id}).execute()
    else:
        return {"error": "No chat found to delete"}
    
def get_threads():
    threads = supabase_client.table('threads').select("*").execute()
    if threads:
        return threads
    return {"404 error": "No threads found"}