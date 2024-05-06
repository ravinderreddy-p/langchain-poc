from fastapi import APIRouter

from langchain_chat_msg_history import chat_history_response
from langchain_retrieval_chain import get_answer


CHAT_ROUTER = APIRouter(tags=['chatbot'])

@CHAT_ROUTER.get("/chat")
def get_chat():
    return "welcome to chat"


@CHAT_ROUTER.post("/chat")
def q_and_a_chat(query: str):
    # response = get_answer(query)
    response = chat_history_response(query)
    return response
