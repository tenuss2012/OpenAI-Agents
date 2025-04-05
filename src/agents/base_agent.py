from abc import ABC, abstractmethod
import openai
from typing import Dict, Any, List, Optional
from ..mcp.client import MCPClient

class BaseAgent(ABC):
    def __init__(self, 
                 openai_api_key: str, 
                 mcp_server_url: Optional[str] = None,
                 mcp_api_key: Optional[str] = None,
                 model: str = "gpt-4"):
        """Initialize the base agent.
        
        Args:
            openai_api_key (str): OpenAI API key
            mcp_server_url (Optional[str]): URL of the MCP server
            mcp_api_key (Optional[str]): API key for MCP server
            model (str, optional): Model to use. Defaults to "gpt-4".
        """
        self.client = openai.Client(api_key=openai_api_key)
        self.model = model
        self.conversation_history = []
        
        # Initialize MCP client if URL is provided
        self.mcp_client = MCPClient(mcp_server_url, mcp_api_key) if mcp_server_url else None
        self.available_tools = []
        
    async def initialize(self):
        """Initialize agent by connecting to MCP server and getting available tools."""
        if self.mcp_client:
            await self.mcp_client.connect()
            self.available_tools = await self.mcp_client.get_available_tools()
            
    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool through MCP server.
        
        Args:
            tool_name (str): Name of the tool to execute
            params (Dict[str, Any]): Tool parameters
            
        Returns:
            Dict[str, Any]: Tool execution results
        """
        if not self.mcp_client:
            raise ValueError("MCP client not initialized")
            
        return await self.mcp_client.execute_tool(tool_name, params)
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return a response.
        
        Args:
            input_data (Dict[str, Any]): Input data for processing
            
        Returns:
            Dict[str, Any]: Processed response
        """
        pass
    
    async def _create_response(self, 
                             messages: List[Dict[str, str]], 
                             tools: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a response using the OpenAI API.
        
        Args:
            messages (List[Dict[str, str]]): Message history
            tools (List[Dict[str, Any]], optional): Tools available to the agent
            
        Returns:
            Dict[str, Any]: API response
        """
        # Combine OpenAI tools with MCP tools if available
        all_tools = tools or []
        if self.available_tools:
            all_tools.extend(self.available_tools)
            
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=all_tools,
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
        
    async def cleanup(self):
        """Cleanup resources when agent is no longer needed."""
        if self.mcp_client:
            await self.mcp_client.close()