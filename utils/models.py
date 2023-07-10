from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

CHATGPT = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
GPT4 = ChatOpenAI(temperature=0, model="gpt4")
ADA_EMBEDDINGS = OpenAIEmbeddings()

if __name__ == "__main__":
    pass
