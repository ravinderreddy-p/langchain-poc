from pydantic import BaseModel, Field, computed_field
from pydantic_settings import BaseSettings

class Application(BaseModel):
    name: str = "langchain-chatbot"
    base_url: str = "/chatbot"
    version: str = "0.0.1"

    @computed_field
    @property
    def description(self) -> str:
        return f"Apidcos for {self.name}"


    @computed_field
    @property
    def allowed_origins(self) -> list[str]:
        origins = ["*"]
        return origins
    

class ApplicationSettings(BaseSettings):
    application: Application = Field(default_factory=Application)

settings = ApplicationSettings()
