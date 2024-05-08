from fastapi import APIRouter
from fastapi.responses import JSONResponse

from langchain_chat_msg_history import chat_history_response
from langchain_retrieval_chain import get_answer
from logger import LOGGER


CHAT_ROUTER = APIRouter(tags=['chatbot'])

@CHAT_ROUTER.get("/chat")
def get_chat():
    LOGGER.info("responding to client request...")
    return JSONResponse({"msg": "success"})


@CHAT_ROUTER.post("/chat")
def q_and_a_chat(query: str):
    # response = get_answer(query)
    LOGGER.info("answering your query")
    response = chat_history_response(query)
    return response
