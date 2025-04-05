from abc import ABC, abstractmethod
import openai
from typing import Dict, Any, List

class BaseAgent(ABC):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """Initialize the base agent.
        
        Args:
            api_key (str): OpenAI API key
            model (str, optional): Model to use. Defaults to "gpt-4".
        """
        self.client = openai.Client(api_key=api_key)
        self.model = model
        self.conversation_history = []
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return a response.
        
        Args:
            input_data (Dict[str, Any]): Input data for processing
            
        Returns:
            Dict[str, Any]: Processed response
        """
        pass
    
    async def _create_response(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a response using the OpenAI API.
        
        Args:
            messages (List[Dict[str, str]]): Message history
            tools (List[Dict[str, Any]], optional): Tools available to the agent
            
        Returns:
            Dict[str, Any]: API response
        """
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        return response
    
    def _update_history(self, role: str, content: str):
        """Update conversation history.
        
        Args:
            role (str): Message role (user/assistant/system)
            content (str): Message content
        """
        self.conversation_history.append({
            "role": role,
            "content": content
        })