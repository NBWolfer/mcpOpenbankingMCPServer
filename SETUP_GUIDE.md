# OpenBanking MCP Server - Setup Guide

## Quick Start

### 1. Prerequisites Check
- [ ] Python 3.8+ installed
- [ ] Conda environment `openbanking-backend` exists
- [ ] Ollama installed (download from https://ollama.ai)

### 2. Environment Setup
```powershell
# Activate conda environment
conda activate openbanking-backend

# Install Python dependencies
pip install PyYAML typing-extensions httpx pydantic ollama

# Optional: Install MCP packages (if available)
pip install mcp
```

### 3. Ollama Setup
```bash
# Install a model (choose one)
ollama pull llama3.2:latest
ollama pull llama3.2:3b
ollama pull codellama:latest

# Start Ollama server (keep this running)
ollama serve
```

### 4. Test the Server
```powershell
# Test basic functionality
python simple_server.py

# Run demo examples
python demo.py

# Full server (if MCP dependencies are available)
python src/main.py
```

## Server Components

### Core Architecture
```
MCP Host ←→ MCP Server ←→ 4 Specialized Agents ←→ Ollama LLMs
                ↓
            Tool System
                ↓
         Banking APIs/Services
```

### Agents Configuration
1. **Market Analyst Agent**
   - Model: llama3.2:latest
   - Role: Market data analysis and volatility assessment
   - Tasks: Market trends, technical analysis, economic indicators

2. **Portfolio Manager Agent**
   - Model: llama3.2:latest
   - Role: Portfolio optimization and strategy development
   - Tasks: Asset allocation, rebalancing, performance analysis

3. **Risk Analyst Agent**
   - Model: llama3.2:latest
   - Role: Risk assessment and management
   - Tasks: Risk profiling, stress testing, scenario analysis

4. **Explainability Agent**
   - Model: llama3.2:latest
   - Role: Education and explanation
   - Tasks: SWOT analysis, concept explanation, decision support

### Available Tools

#### Portfolio Tools
- `analyze_portfolio`: Comprehensive portfolio analysis
- `portfolio_optimization`: Asset allocation optimization
- `performance_attribution`: Performance breakdown analysis

#### Market Tools
- `market_analysis`: Current market conditions
- `volatility_analysis`: Volatility patterns and forecasting
- `sector_analysis`: Sector-specific analysis
- `correlation_analysis`: Asset correlation study

#### Risk Tools
- `assess_risk`: User-specific risk assessment
- `simulate_scenarios`: Stress testing and scenarios
- `liquidity_risk_analysis`: Liquidity risk evaluation
- `tail_risk_analysis`: Extreme event analysis

#### Strategy Tools
- `recommend_strategy`: Investment strategy recommendations
- `tactical_allocation`: Short-term allocation adjustments
- `rebalancing_strategy`: Portfolio rebalancing plans
- `hedge_strategy`: Risk hedging recommendations

#### Analysis Tools
- `swot_analysis`: SWOT analysis framework
- `explain_concept`: Financial concept explanations
- `reverse_simulation`: Reverse engineering analysis
- `decision_analysis`: Decision support framework
- `trend_analysis`: Trend identification and forecasting

## Configuration Files

### config/config.yaml
```yaml
server_name: "openbanking-mcp"
development_mode: false

ollama:
  host: "localhost"
  port: 11434
  timeout: 30

agents:
  - name: "market_analyst"
    model: "llama3.2:latest"
    role: "Market Data Analyst"
    # ... (see full config)

tools:
  - name: "portfolio_analysis"
    enabled: true
```

## Troubleshooting

### Common Issues

1. **"Import could not be resolved" errors**
   - These are IDE warnings, not runtime errors
   - Code will run correctly if dependencies are installed

2. **Ollama connection failed**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # Start Ollama if not running
   ollama serve
   ```

3. **Conda environment issues**
   ```bash
   # Create environment if missing
   conda create -n openbanking-backend python=3.11
   
   # Activate environment
   conda activate openbanking-backend
   ```

4. **Dependencies missing**
   ```bash
   # Install core dependencies
   pip install PyYAML httpx pydantic ollama typing-extensions
   ```

### Testing Steps

1. **Test Configuration Loading**
   ```python
   from src.config.config import Config
   config = Config.load("config/config.yaml")
   print(f"Loaded {len(config.agents)} agents")
   ```

2. **Test Ollama Connection**
   ```python
   import ollama
   client = ollama.Client()
   models = client.list()
   print([m['name'] for m in models['models']])
   ```

3. **Test Agent Communication**
   ```bash
   python simple_server.py
   ```

## Next Steps

1. **Customize Agents**: Modify agent prompts in `config/config.yaml`
2. **Add Custom Tools**: Create new tool classes in `src/tools/`
3. **Integrate APIs**: Add real market data APIs
4. **Deploy**: Set up production environment
5. **Monitor**: Add logging and monitoring

## File Structure Summary

```
mcpOpenbankingMCPServer/
├── src/                    # Source code
│   ├── main.py            # Full MCP server
│   ├── agents/            # Agent management
│   ├── tools/             # Tool implementations
│   ├── config/            # Configuration management
│   └── utils/             # Utilities
├── config/                # Configuration files
├── simple_server.py       # Simplified test server
├── demo.py               # Example usage
├── startup.py            # Startup script
├── start_server.ps1      # PowerShell script
└── requirements.txt      # Dependencies
```

## Support

For issues or questions:
1. Check this setup guide
2. Review error messages in terminal
3. Verify Ollama is running and accessible
4. Ensure conda environment is activated
5. Check that all dependencies are installed

The server is designed to work even if some components fail, with graceful degradation and helpful error messages.
