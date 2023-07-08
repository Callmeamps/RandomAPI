from dotenv import load_dotenv

# Pandas Imports
from langchain.agents import create_pandas_dataframe_agent, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

# Playwright Imports
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import (create_async_playwright_browser)

# Chat Imports
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

load_dotenv()

async_browser = create_async_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
playwright_toolkit = toolkit.get_tools()

CHATGPT = ChatOpenAI(temperature=0, client="gpt-3.5-turbo-0613")
BUFFER_MEMORY = ConversationBufferMemory()

def pandas_agent(source):
    agent = create_pandas_dataframe_agent(
    CHATGPT,
    source,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    return_intermediate_steps=True,
    )
    return agent

def playwright_agent():
    agent_chain = initialize_agent(
        playwright_toolkit,
        CHATGPT,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        return_intermediate_steps=True
        )
    return agent_chain

def chat_agent():
    chat_chain = ConversationChain(
    llm=CHATGPT,
    memory=BUFFER_MEMORY
    )
    return chat_chain

if __name__ == "__main__":
    pass
