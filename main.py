import json
from fastapi import APIRouter, FastAPI, Response

from chatbot.chat import CHAT_ROUTER


app = FastAPI(title='langchain-chat-bot',
              docs_url="/chatbot/apidocs",
              redoc_url="/chatbot/redoc",
              description="API docs for chatbot application",
              openapi_url="/chatbot/openapi.json",
              version="0.0.1")

app.include_router(
    CHAT_ROUTER,
    prefix="/chatbot"

)


@app.get("/chatbot/ping")
def ping():
    return Response(
        json.dumps(dict(ping='pong')),
        headers={"Content-type": "application"}
        )
