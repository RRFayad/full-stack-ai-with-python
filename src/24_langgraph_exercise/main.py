from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated, Literal, Optional
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(model="gpt-4.1-mini", model_provider="openai")


class State(TypedDict):
    user_message: str
    category: Optional[Literal["billing", "technical", "general"]]
    response: Optional[str]


def classify_message(state: State):
    user_message = state["user_message"]

    if "invoice" in user_message or "payment" in user_message:
        return {"category": "billing"}
    elif "bug" in user_message or "error" in user_message:
        return {"category": "technical"}
    else:
        return {"category": "general"}


def route_message(state: State):
    if state["category"] == "billing":
        return "billing_node"
    elif state["category"] == "technical":
        return "technical_node"
    return "general_node"


def billing_node(state: State):
    response = "This looks like a billing issue. I will route you to the billing team."
    return {"response": response}


def technical_node(state: State):
    response = (
        "This looks like a technical issue. I will route you to technical support."
    )
    return {"response": response}


def general_node(state: State):
    response = "This looks like a general question. I will route you to support."
    return {"response": response}


graph_builder = StateGraph(State)

graph_builder.add_node("classify_message", classify_message)
graph_builder.add_node("billing_node", billing_node)
graph_builder.add_node("technical_node", technical_node)
graph_builder.add_node("general_node", general_node)


graph_builder.add_edge(START, "classify_message")
graph_builder.add_conditional_edges("classify_message", route_message)
graph_builder.add_edge("billing_node", END)
graph_builder.add_edge("technical_node", END)
graph_builder.add_edge("general_node", END)


graph = graph_builder.compile()

initial_state = State(
    {
        "user_message": "I got an error when trying to upload my file",
        "category": None,
        "response": None,
    }
)
final_state = graph.invoke(initial_state)

print("\n\nIHAA:", final_state)
