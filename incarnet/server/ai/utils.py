from chromadb import Collection
from chromadb.utils import embedding_functions
from flask import current_app
from flask_jwt_extended import get_jwt_identity

from incarnet.server.models import User
from incarnet.server import chroma


def get_user_collection() -> Collection:
    user: User | None = User.query.filter_by(username=get_jwt_identity()).first()
    if not user:
        raise ValueError(f"no user found for {user}")

    return chroma.get_or_create_collection(name=user.username,
                                           embedding_function=embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-ada-002", api_key=current_app.config.get("OPENAI_API_KEY", ""))
                                           )
