# OpenAI-Agents

This repository demonstrates the use of OpenAI's Agents SDK to create a system of specialized agents that can collaborate to handle various tasks. The implementation includes a web interface for interacting with these agents.

## Features

- Multiple specialized agents:
  - Research Agent: For information gathering and analysis
  - Data Analysis Agent: For data processing and statistics
  - Code Generation Agent: For programming help
- Automatic query routing through a Triage Agent
- Simple web interface for agent interaction
- Async processing support

## Setup

1. Clone the repository:
```bash
git clone https://github.com/tenuss2012/OpenAI-Agents.git
cd OpenAI-Agents
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. Set up your environment:
```bash
cp .env.example .env
```
Then edit `.env` with your settings:
- Add your OpenAI API key
- Adjust other settings as needed (port, debug mode, etc.)

4. Run the web application:
```bash
python src/app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

- `src/`: Source code directory
  - `agents/`: Agent implementations
    - `base_agent.py`: Base agent wrapper
    - `specialized_agents.py`: Specialized agent definitions
  - `app.py`: Flask web application
- `.env.example`: Template for environment variables
- `requirements.txt`: Python dependencies

## Environment Variables

The following environment variables can be configured in your `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `FLASK_ENV`: Application environment (development/production)
- `FLASK_DEBUG`: Enable debug mode (1/0)
- `PORT`: Port number for the web server

## Using the Web Interface

1. Open the web interface at `http://localhost:5000`
2. Enter your query in the text area
3. Click "Submit" to process your query
4. The system will automatically route your query to the most appropriate agent
5. View the agent's response

## Viewing Traces

To review what happened during your agent runs, navigate to the Trace viewer in the OpenAI Dashboard.

## Contributing

Feel free to open issues or submit pull requests. Some areas for potential improvement:

- Additional specialized agents
- Enhanced agent capabilities
- Improved web interface
- Better error handling
- User authentication

## License

MIT License