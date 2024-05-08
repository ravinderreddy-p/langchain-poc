import logging
import uuid


class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    def __init__(self, x_tenant_id: str, x_user_id: str, name: str = "", 
                 trace_id: uuid.UUID | str | None = None) -> None:
        super().__init__(name)
        self.trace_id = trace_id or str(uuid.uuid4())
        self.x_tenant_id = x_tenant_id
        self.x_user_id = x_user_id

    
    def filter(self, record):
        record.x_trace_id = self.trace_id
        record.x_user_id = self.x_user_id
        record.x_tenant_id = self.x_tenant_id
        return True
    

class Logging:
    """
    Logging module for service
    """
    def __init__(self) -> None:
        self.logger = logging.getLogger("chatbot")
        self.logger.setLevel(logging.DEBUG)

    
    def add_stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)4s %(filename)s:%(lineno)d %(x_trace_id)4s %(x_tenant_id)4s %(x_user_id)4s "
            "%(name)4s %(module)4s %(funcName)4s: "
            "%(message)4s"
        )
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        return self.logger
    

LOGGER = Logging().add_stream_handler()
