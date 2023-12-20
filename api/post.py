from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from utils.bots import write_new_post, write_new_post_w_image
from data.api_utils import get_token_from_supabase

load_dotenv()

router = APIRouter()

@router.post("/generate-post")
def generate_post(title: str, topic: str, post_format: str, platform: str):
    response = write_new_post(
        title,
        topic,
        post_format,
        platform,
        required_result="increase engagement"
    )
    return {
        title: title,
        topic: topic,
        post: response,
        platform: platform
        }

@router.post("/generate-post-w-image")
def generate_post_w_image(title: str, topic: str, post_format: str, platform: str):
    response = write_new_post_w_image(
        title,
        topic,
        post_format,
        platform,
        required_result="increase engagement"
    )
    return {
        title: title,
        topic: topic,
        post_data: response,
        platform: platform,
        image: response
        }

@router.post("/tweet")
async def post_tweet(message: str):
    # Get token from Supabase
    token = await get_token_from_supabase()
    
    # Logic for posting Tweets using obtained token
    payload = {"text": message}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    url = "https://api.twitter.com/2/tweets"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return {"message": "Tweet posted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to post tweet")