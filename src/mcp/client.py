import asyncio
import json
from typing import Dict, Any, Optional, List
import websockets
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPClient:
    def __init__(self, server_url: str, api_key: Optional[str] = None):
        """Initialize MCP client.
        
        Args:
            server_url (str): URL of the MCP server
            api_key (Optional[str]): API key for authentication
        """
        self.server_url = server_url
        self.api_key = api_key
        self.websocket = None
        self.connected = False
        
    async def connect(self):
        """Establish connection with MCP server."""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            self.websocket = await websockets.connect(self.server_url, extra_headers=headers)
            self.connected = True
            logger.info(f"Connected to MCP server at {self.server_url}")
            
            # Start heartbeat
            asyncio.create_task(self._heartbeat())
            
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {str(e)}")
            raise
            
    async def _heartbeat(self):
        """Maintain connection with periodic heartbeats."""
        while self.connected:
            try:
                await self.websocket.ping()
                await asyncio.sleep(30)
            except:
                self.connected = False
                break
                
    async def send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send request to MCP server.
        
        Args:
            method (str): Method name
            params (Dict[str, Any]): Method parameters
            
        Returns:
            Dict[str, Any]: Server response
        """
        if not self.connected:
            await self.connect()
            
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": id(params)
        }
        
        await self.websocket.send(json.dumps(request))
        response = await self.websocket.recv()
        return json.loads(response)
        
    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools from MCP server."""
        response = await self.send_request("get_tools", {})
        return response.get("result", [])
        
    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool on the MCP server.
        
        Args:
            tool_name (str): Name of the tool to execute
            params (Dict[str, Any]): Tool parameters
            
        Returns:
            Dict[str, Any]: Tool execution results
        """
        response = await self.send_request("execute_tool", {
            "tool": tool_name,
            "parameters": params
        })
        return response.get("result", {})
        
    async def close(self):
        """Close connection with MCP server."""
        if self.websocket:
            self.connected = False
            await self.websocket.close()
            logger.info("Disconnected from MCP server")