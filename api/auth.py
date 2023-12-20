from fastapi import APIRouter, HTTPException, Request

from data.user_utils import get_current_user, sign_up, sign_in_w_password, sign_out

router = APIRouter()

current_user = get_current_user()

@router.get("/initiate_oauth")
async def initiate_oauth():
    # Generate code verifier and challenge
    code_verifier, code_challenge = generate_pkce_verifier_and_challenge()
    
    # Define OAuth scopes
    scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]
    
    # Redirect user to Twitter's OAuth authorization URL
    oauth_redirect_url = (
        "https://twitter.com/i/oauth2/authorize"
        f"?client_id={os.environ.get('CLIENT_ID')}"
        f"&redirect_uri={os.environ.get('REDIRECT_URI')}"
        "&response_type=code"
        f"&code_challenge={code_challenge}"
        "&code_challenge_method=S256"
        f"&scope={'+'.join(scopes)}"
    )
    return {"oauth_redirect_url": oauth_redirect_url}

# Endpoint for handling OAuth callback
@router.get("/oauth/callback")
async def callback(request: Request, code: str, state: str):
    received_state = request.query_params.get("state")
    if received_state != state:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    # Exchange received code for access token
    token = await exchange_code_for_token(code)
    
    # Save token to Supabase
    await save_token_to_supabase(token)
    
    return {"message": "OAuth callback handled and token saved"}

@router.post("/signup")
def register(email: str, password: str, username: str):
    return sign_up(email, password, username)

@router.post("/signin")
def sign_in(email: str, password: str):
    return sign_in_w_password(email, password)

@router.post("/signout")
def signout():
    return sign_out()
