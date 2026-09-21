import base64
import os
from functools import lru_cache

from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters


load_dotenv()


def get_config(name: str):
    value = os.getenv(name)
    if value:
        return value

    try:
        import streamlit as st
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return None


def get_credentials():
    api_key = get_config("WATSONX_APIKEY")
    url = get_config("WATSONX_URL")

    if not api_key or not url:
        raise RuntimeError(
            "IBM watsonx credentials are missing. Check your .env file "
            "or Streamlit secrets."
        )

    return Credentials(url=url, api_key=api_key)


@lru_cache(maxsize=1)
def get_text_model():
    project_id = get_config("WATSONX_PROJECT_ID")
    model_id = get_config("WATSONX_TEXT_MODEL") or "ibm/granite-4-h-small"

    if not project_id:
        raise RuntimeError("WATSONX_PROJECT_ID is missing.")

    params = TextChatParameters(
        temperature=0.1,
        max_completion_tokens=700,
    )

    return ModelInference(
        model_id=model_id,
        credentials=get_credentials(),
        project_id=project_id,
        params=params,
    )


@lru_cache(maxsize=1)
def get_vision_model():
    project_id = get_config("WATSONX_PROJECT_ID")
    model_id = get_config("WATSONX_VISION_MODEL") or "ibm/granite-vision-3-3-2b"

    if not project_id:
        raise RuntimeError("WATSONX_PROJECT_ID is missing.")

    params = TextChatParameters(
        temperature=0,
        max_completion_tokens=500,
    )

    return ModelInference(
        model_id=model_id,
        credentials=get_credentials(),
        project_id=project_id,
        params=params,
    )


def chat_text(messages):
    response = get_text_model().chat(messages=messages)
    return response["choices"][0]["message"]["content"]


def analyze_image(image_bytes: bytes, mime_type: str):
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{encoded_image}"

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Analyze this waste item image. Describe the visible object, "
                        "material, and useful clues for waste classification. Do not "
                        "invent details that cannot be seen."
                    ),
                },
                {
                    "type": "image_url",
                    "image_url": {"url": data_url},
                },
            ],
        }
    ]

    response = get_vision_model().chat(messages=messages)
    return response["choices"][0]["message"]["content"]
