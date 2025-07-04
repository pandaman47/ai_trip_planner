import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


class ConfigLoader:
    def __init__(self):
        print(f"Loading config....")
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]



class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def __model_post_init__(self) -> None:
        self.config = ConfigLoader()
        
    class Config:
        """Pydantic configuration for ModelLoader."""
        arbitrary_types_allowed = True

    