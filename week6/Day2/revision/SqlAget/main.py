from dotenv import load_dotenv
load_dotenv()
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI


db_path = "zeptoInventory/zepto_inventory.db"
db_uri = f"sqlite:///{db_path}"

db = SQLDatabase.from_uri(db_uri)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True  # Set to False to reduce output
)

# 4. Run sample queries
while True:
    user_query = input("\nEnter your query (or 'exit' to quit): ")
    if user_query.lower() == "exit":
        break
    try:
        result = agent_executor.invoke({"input": user_query})
        print("\nResult:\n", result,result["output"])
    except Exception as e:
        print("Error:", e)


