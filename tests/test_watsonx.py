import os

from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters


load_dotenv()

required = [
    "WATSONX_APIKEY",
    "WATSONX_URL",
    "WATSONX_PROJECT_ID",
]

for name in required:
    if not os.getenv(name):
        raise RuntimeError(f"Missing environment variable: {name}")

credentials = Credentials(
    url=os.getenv("WATSONX_URL"),
    api_key=os.getenv("WATSONX_APIKEY"),
)

params = TextChatParameters(
    temperature=0,
    max_completion_tokens=50,
)

model = ModelInference(
    model_id=os.getenv("WATSONX_TEXT_MODEL", "ibm/granite-4-h-small"),
    credentials=credentials,
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    params=params,
)

response = model.chat(
    messages=[
        {
            "role": "system",
            "content": "You are a test assistant.",
        },
        {
            "role": "user",
            "content": "Reply with exactly the word WORKING.",
        },
    ]
)

print(response["choices"][0]["message"]["content"])
