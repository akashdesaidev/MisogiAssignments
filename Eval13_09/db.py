
from langchain import hub
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.chat_models import init_chat_model
import getpass
import os
from langgraph.prebuilt import create_react_agent

import dotenv
dotenv.load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")


DB_URL = "sqlite:///./database.sqlite"

db = SQLDatabase.from_uri(
    DB_URL,
)

llm = init_chat_model("gpt-4o-mini", model_provider="openai")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
toolkit.get_tools()

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=5)
agent_executor = create_react_agent(llm, tools=toolkit.get_tools(), prompt=system_message)

def get_data(query: str):
    response = agent_executor.invoke({"input": query})
    return response