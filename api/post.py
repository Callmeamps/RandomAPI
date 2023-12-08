from dotenv import load_dotenv
from fastapi import APIRouter

from utils.bots import write_new_post, write_new_post_w_image

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
        platform: platform
        }