from data.supa import supabase_client

def sign_up(email, password, username):
    res = supabase_client.auth.sign_up({
    "email": email,
    "password": password,
    })
    user = get_current_user()
    supabase_client.table("users").insert({
        "username": username,
        })
    return res

def sign_in_w_password(email, password):
    data = supabase_client.auth.sign_in_with_password({
        "email": email,
        "password": password
        })
    return data

def sign_out():
    supabase_client.auth.sign_out()
    return {"success": True, "message": "Signed out successfully"}

def get_current_user():
    user = supabase_client.auth.get_user()
    return user



if __name__ == "__main__":
    pass