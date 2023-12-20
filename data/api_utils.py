import base64
import hashlib
import secrets

from data.supa import supabase_client

async def save_token_to_supabase(token: str):
    # Example: Storing token in a Supabase table named 'tokens'
    response = await supabase.table('tokens').insert({'token': token})
    if response['status'] == 201:
        return {"message": "Token saved successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to save token in Supabase")

async def get_token_from_supabase():
    # Example: Retrieving token from Supabase table named 'tokens'
    response = await supabase_client.table('tokens').select('token').single()
    if response['status'] == 200:
        return response['data']['token']
    else:
        raise HTTPException(status_code=500, detail="Failed to retrieve token from Supabase")

def generate_pkce_verifier_and_challenge():
    code_verifier = secrets.token_urlsafe(100)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().replace('=', '')
    return code_verifier, code_challenge
