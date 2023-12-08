#
import subprocess
from dotenv import load_dotenv

# # Pandas Imports
# from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# from langchain.agents import initialize_agent
# from langchain.agents.agent_types import AgentType

# Playwright Imports
from .tools import playwright_tools, router_tools, files_tools

# Chat Imports
from langchain.chains import ConversationChain

# VectorStore Imports
from langchain.chains import VectorDBQA
from langchain.agents.agent_toolkits import create_vectorstore_router_agent

from .models import CHATGPT
from .memory import BUFFER_MEMORY

load_dotenv()

def router_agent():
    agent = initialize_agent(
        router_tools(),
        CHATGPT,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        return_intermediate_steps=True
        )
    return agent

def vectorstore_agent():
    agent_executor = create_vectorstore_router_agent(
        llm=CHATGPT,
        memory=BUFFER_MEMORY,
        toolkit=router_agent(),
        verbose=True,
        return_intermediate_steps=True
    )
    return agent_executor

def chat_agent():
    chat_chain = ConversationChain(
    llm=CHATGPT,
    memory=BUFFER_MEMORY,
    )
    return chat_chain

# def pandas_agent(source):
#     agent = create_pandas_dataframe_agent(
#     CHATGPT,
#     source,
#     verbose=True,
#     agent_type=AgentType.OPENAI_FUNCTIONS,
#     return_intermediate_steps=True,
#     )
#     return agent

def playwright_agent():
    agent_chain = initialize_agent(
        playwright_tools(),
        CHATGPT,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        return_intermediate_steps=True
        )
    return agent_chain

def gpt_engineer_agent(request):
    subprocess.run(["gpt-engineer", request], check=True)

def file_agent():
    agent_chain = initialize_agent(
        files_tools(),
        CHATGPT,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        return_intermediate_steps=True
        )
    return agent_chain


if __name__ == "__main__":
    pass
