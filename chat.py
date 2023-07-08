from fastapi import FastAPI
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ChatMessageHistory
from langchain.schema import (HumanMessage, SystemMessage)
from langchain.schema import messages_to_dict

from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

from data.message_utils import save_chat_to_supabase, load_chat_from_supabase, save_message_to_supabase, get_threads

openai_api_key = load_dotenv()

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

threads = get_threads()
history = ChatMessageHistory()
memory = ConversationBufferMemory()
chatgpt = ChatOpenAI(model_name="gpt-3.5-turbo-16k")
batch_agent_msgs = []
convo = ConversationChain(
    llm=chatgpt,
    memory=memory
)

@app.get("/")
def welcome():
    return {"Message": "Hello"}

@app.post("/chat")
def chat(message: str):
    reply = chatgpt([HumanMessage(content=message)])
    response = save_message_to_supabase(message, reply.content)
    return response

@app.get("/chat-history")
def get_threads():
    if threads:
        return threads
    return "Error 404! No chat history"

@app.post("/chat/{chat_id}/save")
def save_chat(chat_id: int):
    if chat_id in threads:
        return "Error! chat alread saved."
    response = save_chat_to_supabase(messages_to_dict(history.messages), chat_id)
    return response

@app.get("/chat-history/{chat_id}")
def get_chat_history(chat_id: int):
    if chat_id in threads:
        load_chat_from_supabase(chat_id)
        return threads[chat_id]
    return "404!"

@app.post("/chat_chain")
def chat_w_memory(message: str):
    return convo.predict(input=message)

def pandas_agent():
    agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, client="gpt-3.5-turbo-0613"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    )
    return agent

@app.post("/pandas_agent")
def chat_w_pandas_agent(message: str):
    response = pandas_agent().run(message)
    return response