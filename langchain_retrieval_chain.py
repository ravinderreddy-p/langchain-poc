from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

llm = ChatOpenAI()

output_parser = StrOutputParser()

loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
docs = loader.load()

embeddings = OpenAIEmbeddings()

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}
"""
)

document_chain = create_stuff_documents_chain(llm, prompt)

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)


def get_answer(question):
    response = retrieval_chain.invoke({"input": question})
    return response["answer"]
