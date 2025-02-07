# Data Access with AI Agents

## Overview
This project is an AI-powered financial data aggregator that collects, processes, and presents financial data from multiple sources, including:

- Internet search

- SQLite database queries

- Alpha Vantage API

The system is built using CrewAI to manage AI agents and tasks, it is using gpt4 as LLM however this code can be modified to include any LLM such as watsonx.ai


## Features
- Internet Search: Uses SerperDevTool to fetch financial reports from the web.

- Database Querying: Retrieves financial data stored in an SQLite database.

- API Integration: Fetches real-time stock data using the Alpha Vantage API.

- Automated AI Agents: AI-powered agents collect, process, and format financial data into a structured report.

## Installation

### Prerequisites
- Python 3.8+

- SQLite

- API keys for:

   - Serper API
   - Alpha Vantage API
### Setup
1- Clone the repository:
```
git clone https://github.com/ijgitsh/data-access-ai-agents.git
cd data-access-ai-agents
```
2- Install dependencies:
```
pip install -r requirements.txt
```
3- Set up environment variables:
Replace API keys with your own in the script or export them in your terminal:
```
export SERPER_API_KEY="your_serper_api_key"
export OPENAI_API_KEY="your_openai_api_key"
export ALPHA_VANTAGE_API_KEY="your_alpha_vantage_api_key"
```
### Database Setup
To set up the SQLite database with sample financial data, run:
```
python dbsetup.py
```
## Usage
you can run the two scripts to see various scenarios based on the article

```
python agent-data-acesss-scenario_one.py
python agent-data-acesss-scenarios_limited.py
'''
