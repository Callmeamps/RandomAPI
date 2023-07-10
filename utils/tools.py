import os
from tempfile import TemporaryDirectory

from langchain.vectorstores import DeepLake
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.document_loaders import WebBaseLoader
from langchain.agents.agent_toolkits import (
    VectorStoreRouterToolkit,
    VectorStoreInfo,
)

from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit, FileManagementToolkit
from langchain.tools.playwright.utils import create_async_playwright_browser

from .models import CHATGPT, ADA_EMBEDDINGS

DEEPLAKE_ACCOUNT_NAME = os.getenv("DEEPLAKE_ACCOUNT_NAME")


TEXT_SPLITTER = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

def playwright_tools():
    async_browser = create_async_playwright_browser()
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
    playwright_toolkit = toolkit.get_tools()
    return playwright_toolkit

def files_tools():
    with TemporaryDirectory() as working_directory:
        toolkit = FileManagementToolkit(
            root_dir=str(working_directory.name)
        )  
        file_toolkit = toolkit.get_tools()
        return file_toolkit

def router_tools(vector_stores):
    router_toolkit = VectorStoreRouterToolkit(
    vectorstores=vector_stores,
    llm=CHATGPT
    )
    tools = router_toolkit.get_tools()
    return tools

def text_loader(src_filename):
    loader = TextLoader(src_filename)
    documents = loader.load()
    texts = TEXT_SPLITTER.split_documents(documents)
    return texts

def web_base_loader(address):
    web_loader = WebBaseLoader(address)
    docs = web_loader.load()
    texts = TEXT_SPLITTER.split_documents(docs)
    return texts


def get_info_vectorstore(name, description, vectorstore):
    return VectorStoreInfo(
        name=name,
        description=description,
        vectorstore=vectorstore,
    )

def save_to_deep_lake(texts):
    store = DeepLake.from_documents(
        texts, ADA_EMBEDDINGS, dataset_path=f"hub://{DEEPLAKE_ACCOUNT_NAME}/langchain-code"
    )
    return store


if __name__ == '__main__':
    pass
