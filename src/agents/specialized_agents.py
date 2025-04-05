from agents import Agent, Runner
from pydantic import BaseModel
from typing import List

class SearchOutput(BaseModel):
    query: str
    sources: List[str]
    summary: str

# Research Agent for web searches and information gathering
research_agent = Agent(
    name="Research Agent",
    instructions="""You are a research specialist who helps find and analyze information.
    Break down complex topics, find relevant sources, and provide comprehensive summaries.""",
    handoff_description="Specialist agent for research and information gathering",
    output_type=SearchOutput
)

# Data Analysis Agent for handling data processing tasks
data_analysis_agent = Agent(
    name="Data Analysis Agent",
    instructions="""You help analyze data and provide insights.
    Break down complex datasets, perform statistical analysis, and explain findings clearly.""",
    handoff_description="Specialist agent for data analysis and statistics"
)

# Code Generation Agent for programming tasks
code_agent = Agent(
    name="Code Generation Agent",
    instructions="""You help write and explain code.
    Follow best practices, provide clear documentation, and explain your implementation choices.""",
    handoff_description="Specialist agent for programming and code generation"
)

# Triage agent to route requests to appropriate specialists
triage_agent = Agent(
    name="Triage Agent",
    instructions="""You determine which specialist agent is best suited for the user's request.
    Consider the nature of the task and required expertise.""",
    handoffs=[research_agent, data_analysis_agent, code_agent]
)

async def process_request(query: str) -> str:
    """Process a user request through the agent system.
    
    Args:
        query (str): User's query
        
    Returns:
        str: Agent's response
    """
    result = await Runner.run(triage_agent, query)
    return result.final_output