# OpenAI-Agents

This repository contains exploration and development of OpenAI Agents with a focus on the new Responses API. The project includes a web application that demonstrates agent capabilities using Memory, Context, and Planning (MCP) principles.

## Features

- Research Agent with web search capabilities
- Context maintenance across conversations
- Simple web interface for agent interaction
- Async processing for better performance

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

3. Create a .env file with your OpenAI API key:
```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

4. Run the web application:
```bash
python src/app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

- `src/`: Source code directory
  - `agents/`: Agent implementations
    - `base_agent.py`: Base agent class with common functionality
    - `research_agent.py`: Research agent implementation
  - `app.py`: Flask web application
- `tests/`: Test files
- `examples/`: Example usage and demonstrations
- `docs/`: Documentation

## Using the Web Interface

1. Open the web interface at `http://localhost:5000`
2. Enter your research query in the text area
3. Click "Submit" to process your query
4. View the response and context information

## Contributing

Feel free to open issues or submit pull requests. Some areas for potential improvement:

- Additional agent types
- Enhanced web search capabilities
- Better context management
- Improved error handling
- User authentication
- Advanced web interface features

## License

MIT License