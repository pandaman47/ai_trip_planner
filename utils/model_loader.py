import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
#from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

load_dotenv()

class ConfigLoader:
    def __init__(self):
        print(f"Loading config....")
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]



class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
        
    class Config:
        """Pydantic configuration for ModelLoader."""
        """This lets you include custom classes (like ConfigLoader) as fields
          in your Pydantic model without Pydantic raising an error about unknown types."""
        arbitrary_types_allowed = True

    def load_llm(self):
        """
        Load and return the llm model
        """
        print(f"Loading {self.model_provider} model...")
        if self.model_provider == "groq":
            llm = ChatGroq(
                model_name=self.config["llm"]["groq"]["model_name"],
                api_key=os.getenv("GROQ_API_KEY")
            )
        elif self.model_provider == "openai":
            llm = ChatOpenAI(
                model_name=self.config["llm"]["openai"]["model_name"],
                api_key=os.getenv("OPENAI_API_KEY")
            )

        return llm
    
if __name__ == "__main__":
    loader = ModelLoader(model_provider="groq")
    llm = loader.load_llm()
    print("LLM loaded:", llm)