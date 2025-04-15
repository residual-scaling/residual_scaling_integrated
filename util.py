from db.base_db import BaseDB
from db.keyword_db import KeywordDB
from db.vector_db import VectorDB
from model.base_model import BaseModel
from model.local_model import LocalModel
from model.openai_model import OpenAIModel


def load_model(model_type: str, model: str) -> BaseModel:
    if model_type == "openai":
        return OpenAIModel(model)
    elif model_type == "local":
        return LocalModel(model)
    else:
        raise Exception("In util.py load_model(), model_type is not recognized.")


def load_db(db_type: str) -> BaseDB:
    if db_type == "vector":
        return VectorDB()
    elif db_type == "keyword":
        return KeywordDB()
    else:
        raise Exception("In util.py load_db(), model_type is not recognized.")
