from agents import Agent
from typing import List, Optional, Dict, Any

class BaseAgentWrapper:
    def __init__(self, 
                 name: str,
                 instructions: str,
                 handoff_description: Optional[str] = None,
                 handoffs: Optional[List[Agent]] = None):
        """Initialize a base agent wrapper.
        
        Args:
            name (str): Name of the agent
            instructions (str): Instructions for the agent's behavior
            handoff_description (Optional[str]): Description for handoff routing
            handoffs (Optional[List[Agent]]): List of agents this agent can hand off to
        """
        self.agent = Agent(
            name=name,
            instructions=instructions,
            handoff_description=handoff_description,
            handoffs=handoffs or []
        )
        
    def add_handoff(self, agent: Agent):
        """Add a handoff option to the agent.
        
        Args:
            agent (Agent): Agent to add as a handoff option
        """
        if agent not in self.agent.handoffs:
            self.agent.handoffs.append(agent)
            
    def add_handoffs(self, agents: List[Agent]):
        """Add multiple handoff options to the agent.
        
        Args:
            agents (List[Agent]): Agents to add as handoff options
        """
        for agent in agents:
            self.add_handoff(agent)