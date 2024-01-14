from embedchain import Pipeline
from fastapi import APIRouter, Query, responses
from pydantic import BaseModel

router = APIRouter()

# App config using OpenAI gpt-3.5-turbo-1106 as LLM
app_config = {
    "app": {
        "config": {
            "id": "my-ai-api",
            "collect_metrics": False,
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-3.5-turbo-1106",
        }
    },
    "vectordb": {
        "provider": "pinecone",
        "config": {
            "metric": "cosine",
            "vector_dimension": 1536,
            "collection_name": "embedchain-chat"
        }
    }
}

# Uncomment this configuration to use Mistral as LLM
# app_config = {
#     "app": {
#         "config": {
#             "name": "embedchain-opensource-app"
#         }
#     },
#     "llm": {
#         "provider": "huggingface",
#         "config": {
#             "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
#             "temperature": 0.1,
#             "max_tokens": 250,
#             "top_p": 0.1
#         }
#     },
#     "embedder": {
#         "provider": "huggingface",
#         "config": {
#             "model": "sentence-transformers/all-mpnet-base-v2"
#         }
#     }
# }


ec_app = Pipeline.from_config(config=app_config)


class SourceModel(BaseModel):
    source: str
    namespace: str


class QuestionModel(BaseModel):
    question: str
    session_id: str
    namespace: str


@router.post("/api/v1/add")
async def add_source(source_model: SourceModel):
    """
    Adds a new source to the Embedchain app.
    Expects a JSON with a "source" key.
    """
    source = source_model.source
    namespace = source_model.namespace
    try:
        # Add the source to a specific namespace
        
        # If I want to use the video title as the namespace name, I'd have to parse the YT link here
        # and extract the title of the video
        ec_app.add(source, namespace=namespace)
        return {"message": f"Source '{source}' added successfully to nameapce '{namespace}'."}
    except Exception as e:
        response = f"An error occurred: Error message: {str(e)}. Contact Embedchain founders on Slack: https://embedchain.com/slack or Discord: https://embedchain.com/discord"  # noqa:E501
        return {"message": response}


@router.get("/api/v1/chat")
async def handle_chat(query: str, namespace: str, session_id: str = Query(None)):
    """
    Handles a chat request to the Embedchain app.
    Accepts 'query' and 'session_id' as query parameters.
    """
    print(f"Query: {query}, Session ID: {session_id}, Namespace: {namespace}")
    try:
        response = ec_app.chat(query, session_id=session_id, namespace=namespace)
    except Exception as e:
        response = f"An error occurred: Error message: {str(e)}. Contact Embedchain founders on Slack: https://embedchain.com/slack or Discord: https://embedchain.com/discord"  # noqa:E501
    return {"response": response}


@router.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")
