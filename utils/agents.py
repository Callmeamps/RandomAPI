import os
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

# File Management Imports
from langchain.tools.file_management import (
    ReadFileTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    WriteFileTool,
    ListDirectoryTool,
)
from langchain.agents.agent_toolkits import FileManagementToolkit
from tempfile import TemporaryDirectory

#
import subprocess

# VectorStore Imports
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.text_splitter import CharacterTextSplitter
from langchain import VectorDBQA
from langchain.document_loaders import TextLoader
from langchain.document_loaders import WebBaseLoader
from langchain.agents.agent_toolkits import (
    create_vectorstore_router_agent,
    VectorStoreRouterToolkit,
    VectorStoreInfo,
)

load_dotenv()


CHATGPT = ChatOpenAI(temperature=0, client="gpt-3.5-turbo")
BUFFER_MEMORY = ConversationBufferMemory()
DEEPLAKE_ACCOUNT_NAME = os.getenv("DEEPLAKE_ACCOUNT_NAME")
embeddings = OpenAIEmbeddings()
TEXT_SPLITTER = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

def text_loader(src_filename):
    loader = TextLoader("../../../state_of_the_union.txt")
    documents = loader.load()
    texts = TEXT_SPLITTER.split_documents(documents)
    return texts

def web_base_loader(address):
    web_loader = WebBaseLoader(address)
    docs = web_loader.load()
    texts = TEXT_SPLITTER.split_documents(docs)
    return texts

def save_to_deep_lake(texts):
    store = DeepLake.from_documents(
        texts, embeddings, dataset_path=f"hub://{DEEPLAKE_ACCOUNT_NAME}/langchain-code"
    )
    return store

vectorstore_info = VectorStoreInfo(
    name="state_of_union_address",
    description="the most recent state of the Union adress",
    vectorstore=state_of_union_store,
)

ruff_vectorstore_info = VectorStoreInfo(
    name="ruff",
    description="Information about the Ruff python linting library",
    vectorstore=ruff_store,
)


def router_agent(vector_stores):
    router_toolkit = VectorStoreRouterToolkit(
    vectorstores=vector_stores,
    llm=CHATGPT
    )
    tools = router_toolkit.get_tools()
    agent = initialize_agent(
        tools,
        CHATGPT,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        return_intermediate_steps=True
        )
    return agent


def vectorstore_agent(router_toolkit):
    agent_executor = create_vectorstore_router_agent(
        llm=CHATGPT,
        memory=BUFFER_MEMORY,
        toolkit=router_toolkit,
        verbose=True,
        return_intermediate_steps=True
    )
    return agent_executor


async_browser = create_async_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
playwright_toolkit = toolkit.get_tools()

working_directory = TemporaryDirectory()
file_toolkit = FileManagementToolkit(
    root_dir=str(working_directory.name)
)  # If you don't provide a root_dir, operations will default to the current working directory
toolkit.get_tools()

def chat_agent():
    chat_chain = ConversationChain(
    llm=CHATGPT,
    memory=BUFFER_MEMORY,
    )
    return chat_chain

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

def gpt_engineer_agent(request):
    subprocess.run(["gpt-engineer", request], check=True)

def file_agent():
    agent_chain = initialize_agent(
        file_toolkit,
        CHATGPT,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        return_intermediate_steps=True
        )
    return agent_chain


if __name__ == "__main__":
    pass
