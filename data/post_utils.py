from data.supa import supabase_client

def get_all_posts():
    res = supabase_client.table('posts').select("*").execute()
    if res:
        return res
    return {"404 error": "No posts found"}

def get_post(post_id):
    chat, count = supabase_client.table('posts').select(post_id).execute()
    if count is not None:
        return chat, count
    return chat