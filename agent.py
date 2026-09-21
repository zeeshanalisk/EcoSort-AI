import json
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from llm import chat_text
from rag import retrieve_guidance


ALLOWED_CATEGORIES = [
    "Organic / Food Waste",
    "Paper / Cardboard",
    "Plastic",
    "Glass",
    "Metal",
    "E-Waste",
    "Batteries",
    "Sanitary / Hygiene Waste",
    "Hazardous / Chemical Waste",
    "Mixed / Unknown",
]


SPECIAL_CATEGORIES = {
    "E-Waste",
    "Batteries",
    "Sanitary / Hygiene Waste",
    "Hazardous / Chemical Waste",
}


class EcoSortState(TypedDict, total=False):
    item_input: str
    image_description: str
    location: str
    item_name: str
    category: str
    uncertainty: bool
    classification_reason: str
    retrieved_guidance: list
    final_answer: str


def classify_item(state: EcoSortState):
    item_input = state.get("item_input", "")
    image_description = state.get("image_description", "")

    combined_input = f"User description:\n{item_input}\n\nImage analysis:\n{image_description}"

    prompt = f"""
You are the classification component for EcoSort AI.

Classify one household waste item.

Allowed categories:
{json.dumps(ALLOWED_CATEGORIES, indent=2)}

Rules:
1. Choose exactly one category.
2. Do not invent information.
3. If the evidence is insufficient, use \"Mixed / Unknown\".
4. Treat uncertainty honestly.
5. Return only valid JSON.

Required JSON format:
{{
  \"item_name\": \"short item name\",
  \"category\": \"one allowed category\",
  \"uncertainty\": false,
  \"reason\": \"brief explanation\"
}}

Input:
{combined_input}
"""

    response = chat_text([
        {
            "role": "system",
            "content": "Classify waste carefully and never fabricate missing facts.",
        },
        {"role": "user", "content": prompt},
    ])

    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        result = {
            "item_name": "Unknown item",
            "category": "Mixed / Unknown",
            "uncertainty": True,
            "reason": "The classification response could not be reliably interpreted.",
        }

    category = result.get("category", "Mixed / Unknown")
    if category not in ALLOWED_CATEGORIES:
        category = "Mixed / Unknown"
        result["uncertainty"] = True

    return {
        "item_name": result.get("item_name", "Unknown item"),
        "category": category,
        "uncertainty": bool(result.get("uncertainty", False)),
        "classification_reason": result.get("reason", ""),
    }


def retrieve(state: EcoSortState):
    query = " ".join([
        state.get("item_name", ""),
        state.get("category", ""),
        state.get("item_input", ""),
        state.get("image_description", ""),
    ])

    return {"retrieved_guidance": retrieve_guidance(query, top_k=3)}


def route_after_retrieval(state: EcoSortState):
    if state.get("uncertainty", True):
        return "uncertain"
    if state.get("category") in SPECIAL_CATEGORIES:
        return "special"
    return "standard"


def create_recommendation(state: EcoSortState):
    guidance_text = "\n\n".join(
        item["text"] for item in state.get("retrieved_guidance", [])
    )

    prompt = f"""
You are the recommendation component of EcoSort AI.

Waste item: {state.get('item_name', 'Unknown')}
Category: {state.get('category', 'Mixed / Unknown')}
User location: {state.get('location', 'Not provided')}

Retrieved guidance:
{guidance_text}

Create a short, practical recommendation with these sections:

**Detected item**
**Waste category**
**What to do**
**Important caution**
**Local-rule note**

Rules:
- Use the retrieved guidance as the main factual basis.
- Do not invent municipal rules.
- Do not claim one disposal route is universally valid.
- If location-specific information is unavailable, say that local rules may differ.
- Do not give dangerous handling instructions.
- Make special-handling warnings clear for batteries, e-waste, sanitary waste, and hazardous materials.
- If the classification is uncertain, ask the user for more information instead of guessing.
"""

    response = chat_text([
        {
            "role": "system",
            "content": "Give clear, safety-conscious waste-handling guidance grounded in the supplied context.",
        },
        {"role": "user", "content": prompt},
    ])

    return {"final_answer": response}


def uncertain_response(state: EcoSortState):
    return {
        "final_answer": (
            "**Detected item**\n"
            "The item could not be identified reliably.\n\n"
            "**Waste category**\n"
            "Mixed / Unknown\n\n"
            "**What to do**\n"
            "Provide a clearer description or a clearer image and, if possible, mention the material.\n\n"
            "**Important caution**\n"
            "The system should not guess the disposal method for an uncertain or potentially hazardous item.\n\n"
            "**Local-rule note**\n"
            "Waste-management requirements can vary by location."
        )
    }


builder = StateGraph(EcoSortState)
builder.add_node("classify_item", classify_item)
builder.add_node("retrieve", retrieve)
builder.add_node("create_recommendation", create_recommendation)
builder.add_node("uncertain_response", uncertain_response)

builder.add_edge(START, "classify_item")
builder.add_edge("classify_item", "retrieve")
builder.add_conditional_edges(
    "retrieve",
    route_after_retrieval,
    {
        "standard": "create_recommendation",
        "special": "create_recommendation",
        "uncertain": "uncertain_response",
    },
)
builder.add_edge("create_recommendation", END)
builder.add_edge("uncertain_response", END)


eco_sort_graph = builder.compile()


def run_ecosort(item_input: str, image_description: str = "", location: str = ""):
    state = {
        "item_input": item_input,
        "image_description": image_description,
        "location": location,
    }
    return eco_sort_graph.invoke(state)
