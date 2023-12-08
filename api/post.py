from dotenv import load_dotenv
from fastapi import APIRouter

from utils.bots import write_new_post

load_dotenv()

router = APIRouter()

@router.post("/generate-post")
def chat(message: str):
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