from embedchain import App
from embedchain.llm.openai import OpenAILlm
import requests
from pydantic import BaseModel, Field, ValidationError, field_validator

# app = App()
# app.add('https://www.youtube.com/watch?v=hkgLxhrjfUE', data_type='youtube_video')

# app.deploy()





import requests



url = "https://app.embedchain.ai/api/v1/pipelines/b43e518d-0daa-4eb1-89b5-853c81fc95fe/context/"

payload = {
  "query": "What is Istio rate limiter?",
  "count": 1
}
headers = {
  'Authorization': 'Token ec-hOoYW3NXtULPoY2Oe5d08CREgSqSTjkDztICy4xO',
}

response = requests.request("POST", url, headers=headers, json=payload)

print(response.text)



# result = app.query("Hey I am Sid. What is a mountain? A mountain is a hill.")


# print(result)


# app.add("https://www.forbes.com/profile/elon-musk")
# app.add("https://en.wikipedia.org/wiki/Elon_Musk")

# app.add("advanced-react.pdf", data_type="pdf_file")


# result = app.query("What is the net worth of Elon Musk today?")


# print(result)

# print(app.query("how created the video?"))
