from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import asyncio
from agents.specialized_agents import process_request

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/api/query", methods=["POST"])
async def query():
    """
    Process a query through the agent system
    """
    try:
        data = request.json
        if not data or "query" not in data:
            return jsonify({"error": "Missing query parameter"}), 400

        response = await process_request(data["query"])
        return jsonify({"response": response})

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
        <title>OpenAI Agents Demo</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { margin-top: 20px; }
            .input-container { margin-bottom: 20px; }
            textarea { width: 100%; height: 100px; margin-bottom: 10px; }
            button { padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            .response { margin-top: 20px; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>OpenAI Agents Demo</h1>
        <div class="container">
            <div class="input-container">
                <h2>Ask a Question</h2>
                <p>Our system will automatically route your query to the most appropriate agent:</p>
                <ul>
                    <li>Research Agent: For information gathering and analysis</li>
                    <li>Data Analysis Agent: For data processing and statistics</li>
                    <li>Code Generation Agent: For programming help</li>
                </ul>
                <textarea id="query" placeholder="Enter your query..."></textarea>
                <button onclick="submitQuery()">Submit</button>
            </div>
            <div id="response" class="response"></div>
        </div>

        <script>
            async function submitQuery() {
                const query = document.getElementById('query').value;
                const response = document.getElementById('response');
                response.textContent = 'Processing...';
                
                try {
                    const result = await fetch('/api/query', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ query }),
                    });
                    
                    const data = await result.json();
                    response.textContent = data.response;
                } catch (error) {
                    response.textContent = `Error: ${error.message}`;
                }
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)