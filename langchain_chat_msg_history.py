from typing import Dict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def parse_retriever_input(params: Dict):
    return params["messages"][-1].content


loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(k=4)

# docs = retriever.invoke("how can langsmith help with testing?")

llm = ChatOpenAI(model="gpt-3.5-turbo-1106")
question_answering_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user's questions based on the below context:\n\n{context}",
        ),
        MessagesPlaceholder(variable_name="messages"),
        
    ]
)
output_parser = StrOutputParser()

document_chain = create_stuff_documents_chain(llm, question_answering_prompt, output_parser=output_parser)

demo_chat_history = ChatMessageHistory()

# Creating Retrieval Chain
retrieval_chain = RunnablePassthrough.assign(
    context=parse_retriever_input | retriever,
).assign(
    answer = document_chain
)

def chat_history_response(question):
    demo_chat_history.add_user_message(question)
    resp = retrieval_chain.invoke(
    {
        "messages": demo_chat_history.messages,
    }
    )
    demo_chat_history.add_ai_message(resp["answer"])
    print(resp)
    return resp["answer"]
