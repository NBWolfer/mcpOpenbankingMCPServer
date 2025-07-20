# OpenBanking MCP Server

An MCP (Model Context Protocol) server that integrates with local Ollama LLMs for OpenBanking applications.

## Features

- **Multiple LLM Agents**: Support for 4 different specialized agents
- **Ollama Integration**: Local LLM model support
- **Tool System**: Comprehensive toolset for various operations
- **OpenBanking Focus**: Specialized tools for banking and financial data

## Architecture

This MCP server follows the architecture shown in the diagram:

- MCP Host communicates with MCP Server
- 4 Specialized Agents (Agent 1-4) with LLM/Model capabilities
- Tool system for specific operations
- Banking Services/API integration

## Agents

1. **Agent 1 - Market Analyst**: Market data analysis and volatile situations
2. **Agent 2 - Portfolio Manager**: Portfolio management and strategy finding
3. **Agent 3 - Risk Analyst**: Risk analysis for users
4. **Agent 4 - Explainability Agent**: LLM for explainability and SWOT analysis

## Project Structure

```
mcpOpenbankingMCPServer/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Main server entry point
│   ├── agents/
│   │   ├── __init__.py
│   │   └── agent_manager.py    # Agent management system
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── tool_registry.py    # Tool registration and management
│   │   ├── portfolio_tools.py  # Portfolio analysis tools
│   │   ├── market_tools.py     # Market data tools
│   │   ├── risk_tools.py       # Risk assessment tools
│   │   ├── strategy_tools.py   # Strategy recommendation tools
│   │   └── analysis_tools.py   # SWOT and explanation tools
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py          # Configuration management
│   └── utils/
│       ├── __init__.py
│       └── utils.py           # Utility functions
├── config/
│   └── config.yaml            # Server configuration
├── requirements.txt           # Python dependencies
├── startup.py                 # Python startup script
├── start_server.ps1          # PowerShell startup script
├── start_server.bat          # Batch file for Windows
├── demo.py                   # Demo examples
├── test_server.py            # Test script
└── README.md                 # This file
```

## Prerequisites

1. **Python 3.8+** with conda environment
2. **Ollama** installed and running locally
3. **Conda environment** named `openbanking-backend`

## Setup

### 1. Create Conda Environment (if not exists)

```bash
conda create -n openbanking-backend python=3.11
conda activate openbanking-backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install and Start Ollama

Download and install Ollama from [https://ollama.ai](https://ollama.ai)

```bash
# Pull a model (example with Llama 3.2)
ollama pull llama3.2:latest

# Start Ollama server
ollama serve
```

### 4. Configure the Server

Edit `config/config.yaml` to customize:
- Ollama connection settings
- Agent configurations
- Model assignments
- Tool settings

## Running the Server

### Option 1: Using PowerShell Script (Recommended for Windows)

```powershell
.\start_server.ps1
```

### Option 2: Using Python Startup Script

```bash
python startup.py
```

### Option 3: Direct Execution

```bash
conda activate openbanking-backend
python src/main.py
```

### Option 4: Development Mode

```bash
python src/main.py --dev
```

## Tools Available

### Portfolio Analysis
- `analyze_portfolio`: Comprehensive portfolio analysis
- `portfolio_optimization`: Portfolio allocation optimization

### Market Analysis
- `market_analysis`: Current market conditions analysis
- `volatility_analysis`: Market volatility assessment

### Risk Assessment
- `assess_risk`: User-specific risk assessment
- `risk_simulation`: Scenario-based risk simulation

### Strategy Recommendations
- `recommend_strategy`: Investment strategy recommendations

### Analysis & Explainability
- `swot_analysis`: SWOT analysis for any subject
- `explain_concept`: Explain financial concepts simply
- `reverse_simulation`: Reverse engineering analysis

## Usage Examples

### Run Demo

```bash
python demo.py
```

### Test the Server

```bash
python test_server.py
```

## Configuration

The server uses `config/config.yaml` for configuration. Key sections:

```yaml
# Ollama connection
ollama:
  host: "localhost"
  port: 11434
  timeout: 30

# Agents configuration
agents:
  - name: "market_analyst"
    model: "llama3.2:latest"
    role: "Market Data Analyst"
    # ... more config

# Tools configuration
tools:
  - name: "portfolio_analysis"
    enabled: true
```

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   - Ensure Ollama is installed and running (`ollama serve`)
   - Check if the default port 11434 is available
   - Verify models are pulled (`ollama list`)

2. **Conda Environment Issues**
   - Make sure `openbanking-backend` environment exists
   - Activate the environment before running
   - Install dependencies in the correct environment

3. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python path and working directory

### Logs

Check the console output for detailed error messages and debugging information.

## Development

### Adding New Tools

1. Create tool class in `src/tools/`
2. Add tool registration in `tool_registry.py`
3. Update configuration if needed

### Adding New Agents

1. Add agent configuration in `config/config.yaml`
2. Implement custom agent logic if needed
3. Test with demo scripts

## License

MIT License
