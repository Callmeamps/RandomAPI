from fastapi import FastAPI
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

from langchain.memory import ChatMessageHistory
from langchain.schema import (HumanMessage)
from langchain.schema import messages_to_dict


from data.message_utils import save_chat_to_supabase, load_chat_from_supabase, save_message_to_supabase, get_threads
from data.user_utils import get_current_user, sign_up, sign_in_w_password, sign_out
from utils.agents import chat_agent

load_dotenv()

FOT_PROMPT = """
Imagine three different experts are answering this question.
They will brainstorm the answer step by step reasoning carefully and taking all facts into consideration
All experts will write down 1 step of their thinking, then share it with the group.
They will each critique their response, and the all the responses of others
They will check their answer based on science and the laws of physics
Then all experts will go on to the next step and write down this step of their thinking.
They will keep going through steps until they reach their conclusion taking into account the thoughts of the other experts
If at any time they realise that there is a flaw in their logic they will backtrack to where that flaw occurred
If any expert realises they're wrong at any point then they acknowledges this and start another train of thought
Each expert will assign a likelihood of their current assertion being correct
Continue until the experts agree on the single most likely location.
"""
app = FastAPI()

current_user = get_current_user()
print(current_user)
threads = get_threads()
print(threads)
history = ChatMessageHistory()
print(history)
chatgpt = ChatOpenAI(model_name="gpt-3.5-turbo-16k")
batch_agent_msgs = []

@app.get("/")
def welcome():
    return {"Message": "Hello"}

@app.post("/signup")
def register(email: str, password: str, username: str):
    return sign_up(email, password, username)

@app.post("/signin")
def sign_in(email: str, password: str):
    return sign_in_w_password(email, password)

@app.post("/signout")
def signout():
    return sign_out()

@app.post("/chat")
def chat(message: str):
    reply = chatgpt([HumanMessage(content=message)])
    response = save_message_to_supabase(message, reply.content)
    return response

@app.get("/chat-history")
def get_chat_threads():
    if threads:
        return threads
    return {"error": 404, "message": "Error 404! No chat history"}

@app.post("/chat/{chat_id}/save")
def save_chat(chat_id: int):
    if chat_id == threads.data[chat_id].chat_id:
        return "Error! chat alread saved."
    response = save_chat_to_supabase(messages_to_dict(history.messages), chat_id)
    return response

@app.get("/chat-history/{chat_id}")
def get_a_chats_history(chat_id: int):
    if chat_id in threads.data:
        load_chat_from_supabase(chat_id)
        return threads.data[chat_id]
    return "404!"

@app.post("/chat_chain")
def chat_w_memory(message: str):
    return chat_agent().predict(input=message)



# @app.post("/pandas_agent")
# def chat_w_pandas_agent(message: str):
#     response = pandas_agent().run(message)
#     return response