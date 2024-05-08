import json
from fastapi import Depends, FastAPI, Header, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(GZipMiddleware)

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


@app.middleware("http")
async def general_exception_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
    except Exception as ex:
        LOGGER.error("An Unhandled exception was intercepted")
        LOGGER.error("Error is as follows: %s", ex)
        response = JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                content={"msg": "Something went wrong", "error": True})
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
