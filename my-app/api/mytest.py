from openai import OpenAI 
import os
import pinecone

# initialize connection to pinecone (get API key at app.pinecone.io)
pinecone.init(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment=os.environ.get("PINECONE_ENV")
)

index = pinecone.Index('embedchain-chat-1536')


query = "What is this video about?"

MODEL="text-embedding-ada-002"

openaiClient = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

emb = openaiClient.embeddings.create(input=query, model=MODEL).data[0].embedding

res = index.query(emb, top_k=5, include_metadata=True, namespace="microservices")

for match in res['matches']:
    print(f"{match['score']:.2f}: {match['metadata']['text']}")

