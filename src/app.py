from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import asyncio
from agents.research_agent import ResearchAgent

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize agents with MCP configuration
research_agent = ResearchAgent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    mcp_server_url=os.getenv("MCP_SERVER_URL"),
    mcp_api_key=os.getenv("MCP_API_KEY")
)

async def initialize_agents():
    """Initialize all agents."""
    await research_agent.initialize()

@app.route("/api/research", methods=["POST"])
async def research():
    """
    Endpoint for research agent queries
    """
    try:
        data = request.json
        if not data or "query" not in data:
            return jsonify({"error": "Missing query parameter"}), 400

        response = await research_agent.process(data)
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tools", methods=["GET"])
async def get_available_tools():
    """
    Get list of available tools from MCP server
    """
    try:
        tools = research_agent.available_tools
        return jsonify({"tools": tools})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    """
    Serve the main HTML page
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OpenAI Agents with MCP Demo</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { margin-top: 20px; }
            .input-container { margin-bottom: 20px; }
            textarea { width: 100%; height: 100px; margin-bottom: 10px; }
            button { padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            .response { margin-top: 20px; white-space: pre-wrap; }
            .tools { margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>OpenAI Agents with MCP Demo</h1>
        
        <div class="container">
            <div class="tools">
                <h2>Available Tools</h2>
                <div id="tools-list"></div>
            </div>
            
            <div class="input-container">
                <h2>Research Agent</h2>
                <textarea id="research-query" placeholder="Enter your research query..."></textarea>
                <button onclick="submitResearch()">Submit</button>
            </div>
            <div id="research-response" class="response"></div>
        </div>

        <script>
            // Fetch available tools on page load
            async function fetchTools() {
                try {
                    const result = await fetch('/api/tools');
                    const data = await result.json();
                    const toolsList = document.getElementById('tools-list');
                    toolsList.innerHTML = JSON.stringify(data.tools, null, 2);
                } catch (error) {
                    console.error('Error fetching tools:', error);
                }
            }
            
            async function submitResearch() {
                const query = document.getElementById('research-query').value;
                const response = document.getElementById('research-response');
                
                try {
                    const result = await fetch('/api/research', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ query }),
                    });
                    
                    const data = await result.json();
                    response.textContent = JSON.stringify(data, null, 2);
                } catch (error) {
                    response.textContent = `Error: ${error.message}`;
                }
            }
            
            // Fetch tools on page load
            fetchTools();
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    # Initialize agents before starting the server
    asyncio.run(initialize_agents())
    app.run(debug=True)