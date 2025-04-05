from typing import Dict, Any, List
import json
from .base_agent import BaseAgent

class ResearchAgent(BaseAgent):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        super().__init__(api_key, model)
        self.context = {}
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "Search the web for information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "save_to_context",
                    "description": "Save information to agent's context",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "key": {
                                "type": "string",
                                "description": "Context key"
                            },
                            "value": {
                                "type": "string",
                                "description": "Information to save"
                            }
                        },
                        "required": ["key", "value"]
                    }
                }
            }
        ]

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data using research capabilities.
        
        Args:
            input_data (Dict[str, Any]): Input data containing query
            
        Returns:
            Dict[str, Any]: Research results and context
        """
        query = input_data.get("query", "")
        self._update_history("user", query)
        
        # Add context to the message if available
        messages = self.conversation_history.copy()
        if self.context:
            context_str = "Current context:\n" + json.dumps(self.context, indent=2)
            messages.append({
                "role": "system",
                "content": context_str
            })
        
        response = await self._create_response(messages, self.tools)
        
        # Process tool calls if any
        if response.choices[0].message.tool_calls:
            for tool_call in response.choices[0].message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                
                if func_name == "save_to_context":
                    self.context[func_args["key"]] = func_args["value"]
                elif func_name == "search_web":
                    # Implement web search functionality here
                    pass
        
        response_content = response.choices[0].message.content
        self._update_history("assistant", response_content)
        
        return {
            "response": response_content,
            "context": self.context
        }