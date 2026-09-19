import os

from typing import TypedDict

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, START, END

from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
import streamlit as st

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=st.secrets["OPENAI_API_KEY"]
)
from tools import (
    analyze_student,
    compare_students
)

from rag import search_knowledge


load_dotenv()


# --------------------------------
# LLM
# --------------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# --------------------------------
# RAG Tool
# --------------------------------

def knowledge_search(query: str):
    """
    Search the career knowledge base.
    """

    return search_knowledge(query)


# --------------------------------
# LangChain Tools
# --------------------------------

tools = [
    analyze_student,
    compare_students
]


# We wrap RAG as a tool
from langchain_core.tools import tool


@tool
def career_knowledge(query: str):
    """
    Search the career knowledge base using RAG.
    Use this when the user asks about career skills,
    learning paths, interview preparation or project ideas.
    """

    return knowledge_search(query)


tools.append(career_knowledge)


# Bind tools to LLM

llm_with_tools = llm.bind_tools(tools)


# --------------------------------
# State
# --------------------------------

class AgentState(TypedDict):

    messages: list


# --------------------------------
# Agent Node
# --------------------------------

def agent_node(state):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# --------------------------------
# Graph
# --------------------------------

graph = StateGraph(AgentState)


graph.add_node(
    "agent",
    agent_node
)

graph.add_node(
    "tools",
    ToolNode(tools)
)


graph.add_edge(
    START,
    "agent"
)


graph.add_conditional_edges(
    "agent",
    tools_condition
)


graph.add_edge(
    "tools",
    "agent"
)


graph.add_edge(
    "agent",
    END
)


app = graph.compile()


# --------------------------------
# Main Agent Function
# --------------------------------

def ask_agent(question):

    system_message = """
You are SkillPilot, an AI learning and career assistant.

You can use three tools:

1. analyze_student
   Use this for student performance and skill analysis.

2. compare_students
   Use this to compare students.

3. career_knowledge
   Use this to search the RAG knowledge base.

Always use tools when they are relevant.

Do not invent student scores.

Give practical recommendations.

Explain your reasoning in simple language suitable
for college students.
"""

    result = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content=system_message
                    + "\n\nUser question:\n"
                    + question
                )
            ]
        }
    )

    messages = result["messages"]

    return messages[-1].content