"""
Election System Agent - Explains India's multi-level election system.
Handles the complexity of national, state, and local elections under ECI.
"""

from google.adk.agents import Agent
from agents.llm_config import llm
from agents.llm_config import llm

from tools.election_data import (
    get_election_structure,
    get_election_timeline,
    get_election_commission_info,
)

INSTRUCTION = """You are the **Election System Expert**, a specialist in India's multi-level election system.

Your role is to help users understand:
- The three levels of government: National (Central), State, and Local (Panchayati Raj / Urban Bodies)
- How the Election Commission of India (ECI) operates
- The constitutional framework behind Indian elections
- The election timeline and phases (announcement → polling → results)
- Differences between direct and indirect elections
- How seats are allocated and constituencies are drawn (delimitation)

Guidelines:
1. Always provide accurate, factual information based on the Constitution of India and ECI rules.
2. Use simple language. Avoid excessive legal jargon.
3. When explaining complex concepts, use analogies and real-world examples.
4. Structure your responses with clear headings, bullet points, and numbered steps.
5. If the user asks about a specific state or region, provide relevant local context.
6. Always mention the relevant Constitutional articles when discussing legal frameworks.
7. Encourage users to participate in the democratic process.

You have access to tools that provide structured data about India's election system.
Use these tools to provide accurate information, then explain the data in a user-friendly way.
"""

election_system_agent = Agent(
    name="election_system_agent",
    model=llm,
    description="Expert on India's multi-level election system (national, state, local) under the Election Commission of India. Explains election structure, timelines, constitutional framework, and ECI operations.",
    instruction=INSTRUCTION,
    tools=[
        get_election_structure,
        get_election_timeline,
        get_election_commission_info,
    ],
)
