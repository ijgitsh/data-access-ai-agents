import os
import sqlite3
import requests
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from crewai.tools import tool
import yaml



# Set up environment variables (Replace with your credentials)
os.environ["SERPER_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""
ALPHA_VANTAGE_API_KEY = ""


# Initialize Internet Search Tool
search_tool = SerperDevTool()


def get_user_roles(username):
    with open('user_roles.yaml', 'r') as file:
        users = yaml.safe_load(file)['users']
    for user in users:
        if user['username'] == username:
            return user['roles']
    return []

@tool("query row level filtered finance data")
def query_row_level_finance_data():
    """Queries an SQLite finance database with limited access and returns financial data at row level."""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM finance WHERE user_role = 'restricted'")
    data = cursor.fetchall()
    conn.close()
    return str(data)

@tool("query limited finance data")
def query_limited_finance_data():
    """Queries an SQLite finance database with limited access and returns financial data."""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT company, stock_price FROM finance")
    data = cursor.fetchall()
    conn.close()
    return str(data)

# SQLite Tool to query financial data
@tool("query finance data")
def query_finance_data():
    """Queries an SQLite finance database and returns financial data."""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM finance")
    data = cursor.fetchall()
    conn.close()
    return str(data)

# API Tool to fetch financial data
@tool("fetch_financial_data")
def fetch_financial_data():
    """Fetches financial data from Alpha Vantage API."""
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return "Failed to fetch financial data"

# Data Collector Agent
data_collector = Agent(
    role="Data Collector",
    goal="Gather financial data from multiple sources",
    verbose=True,
    model="gpt4",
    memory=True,
    backstory="An AI researcher focused on collecting financial insights from various sources.",
    tools=[search_tool, query_finance_data, fetch_financial_data],
)

# Data Presenter Agent
data_presenter = Agent(
    role="Data Presenter",
    goal="Format and present financial data",
    verbose=True,
    model="gpt4",
    memory=True,
    backstory="An AI specializing in summarizing and formatting financial insights for reporting.",
)

# Tasks
internet_search_task = Task(
    description="Fetch IBM's Q4 results from the provided link.",
    expected_output="Summary of IBM's Q4 results.",
    tools=[search_tool],
    agent=data_collector,
)

database_query_task = Task(
    description="Retrieve financial data from the SQLite database.",
    expected_output="Extracted financial data from the database.",
    tools=[query_finance_data],
    agent=data_collector,
)

database_query_task_Limited = Task(
    description="Retrieve limited financial data from the SQLite database.",
    expected_output="Extracted financial data from the database.",
    tools=[query_limited_finance_data],
    agent=data_collector,
)


database_query_task_Limited_row = Task(
    description="Retrieve row level financial data from the SQLite database.",
    expected_output="Extracted financial data from the database.",
    tools=[query_row_level_finance_data],
    agent=data_collector,
)

api_fetch_task = Task(
    description="Fetch IBM stock data from Alpha Vantage API.",
    expected_output="Latest IBM stock data from API.",
    tools=[fetch_financial_data],
    agent=data_collector,
)

presentation_task = Task(
    description="Format and present the collected financial data in a structured format.",
    expected_output="A well-structured financial report with insights from all sources.",
    agent=data_presenter,
)

masking_task = Task(
    description="Format and present the collected financial data in a structured format.Mask revenue and net income information from the results.",
    expected_output="A well-structured financial report with insights from all sources",
    agent=data_presenter,
)

current_user = "user_b"
roles = get_user_roles(current_user)

crew = Crew(
    agents=[data_collector, data_presenter],
    tasks=[internet_search_task, database_query_task, api_fetch_task, presentation_task],
    process=Process.sequential
)

if "restricted" in roles:
    crew.tasks.remove(database_query_task)

if "limited_api_access" in roles:
    crew.tasks.remove(api_fetch_task)

if "restricted_db" in roles:
    crew.tasks.append(database_query_task_Limited)

if "row_restricted" in roles:
    crew.tasks.remove(database_query_task_Limited)
    crew.tasks.append(database_query_task_Limited_row)

if "mask_data" in roles:
    crew.tasks.remove(presentation_task)
    crew.tasks.append(masking_task)

#print(crew.tasks)
# Run the Crew
result = crew.kickoff()
print(result)
