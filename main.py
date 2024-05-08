import json
from fastapi import APIRouter, Depends, FastAPI, Header, Response, status

from chatbot.chat import CHAT_ROUTER
from logger import LOGGER, ContextFilter
from settings import settings


app = FastAPI(title=settings.application.name,
              docs_url=settings.application.base_url + "/apidocs",
              redoc_url=settings.application.base_url + "/redoc",
              description=settings.application.description,
              openapi_url=settings.application.base_url + "openapi.json",
              version=settings.application.version
              )

origins = settings.application.allowed_origins

def include_trace_id(x_tenant_id: str = Header(default="tenant1"),
                     x_user_id: str = Header(default="Ravi"),
                     x_trace_id: str = Header(default=None)
                     ):
    context_filter = ContextFilter(trace_id=x_trace_id, 
                                   x_tenant_id=x_tenant_id, x_user_id=x_user_id)
    LOGGER.filters.clear()
    LOGGER.addFilter(context_filter)
    response = Response(status_code=status.HTTP_200_OK)
    return response


app.include_router(
    CHAT_ROUTER,
    prefix=settings.application.base_url,
    dependencies=[Depends(include_trace_id)]

)


@app.get("/chatbot/ping")
def ping():
    return Response(
        json.dumps(dict(ping='pong')),
        headers={"Content-type": "application"}
        )
