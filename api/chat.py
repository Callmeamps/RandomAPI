from dotenv import load_dotenv
from fastapi import APIRouter

from langchain.chat_models import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain.schema import HumanMessage, messages_to_dict

from data.message_utils import save_chat_to_supabase, load_chat_from_supabase, save_message_to_supabase, get_threads
from utils.agents import chat_agent

load_dotenv()

router = APIRouter()
history = ChatMessageHistory()
chatgpt = ChatOpenAI(model_name="gpt-3.5-turbo-16k")

@router.post("/chat")
def chat(message: str):
    reply = chatgpt([HumanMessage(content=message)])
    response = save_message_to_supabase(message, reply.content)
    return response

@router.get("/chat-history")
def get_chat_threads():
    threads = get_threads()
    if threads:
        return threads
    return {"error": 404, "message": "Error 404! No chat history"}

@router.post("/chat/{chat_id}/save")
def save_chat(chat_id: int):
    threads = get_threads()
    if chat_id in threads.data:
        return "Error! chat already saved."
    response = save_chat_to_supabase(messages_to_dict(history.messages), chat_id)
    return response

@router.get("/chat-history/{chat_id}")
def get_a_chats_history(chat_id: int):
    threads = get_threads()
    if chat_id in threads.data:
        load_chat_from_supabase(chat_id)
        return threads.data[chat_id]
    return "404!"

@router.post("/chat_chain")
def chat_w_memory(message: str):
    return chat_agent().predict(input=message)
