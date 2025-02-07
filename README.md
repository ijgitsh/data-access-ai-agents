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

-- Serper API

-- Alpha Vantage API
