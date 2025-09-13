from fastmcp import FastMCP
from langchain_community.utilities import SQLDatabase
from db import db


mcp=FastMCP("MCP-SQL-Agent-Eval")



dialect=db.dialect
table_info=db.get_table_info()


def sql_query_execute(query: str) -> str:
    try:
        result = db.run(query)
    except Exception as e:
        raise f"Error executing SQL query after multiple attempts: {str(e)}"

    return str(result)

    
@mcp.tool
def execute_query(query: str) -> str:
    """Pass the query from llm to sql db and return the result."""
    return sql_query_execute(query)

@mcp.tool
def query_player_stats(player_name: str) -> str:
    """Query player statistics by player name. Create a SQL query to retrieve player statistics. and then use execute_query tool to execute the query."""
    prompt = f"""
    You are an expert SQL agent. Given the database dialect and table information, generate a SQL query to retrieve statistics for the player named '{player_name}'.
    Use the following table information:
    {table_info}
    Ensure the SQL query is syntactically correct for the '{dialect}' dialect.
    """
    return prompt


@mcp.tool
def match_analysis(match_id: int) -> str:
    """Analyze a specific match by match ID. Create a SQL query to analyze the match. and then use execute_query tool to execute the query."""
    prompt = f"""
    You are an expert SQL agent. Given the database dialect and table information, generate a SQL query to analyze the match with ID '{match_id}'.
    Use the following table information:
    {table_info}
    Ensure the SQL query is syntactically correct for the '{dialect}' dialect.
    """
    return prompt

@mcp.tool
def team_performance(team_name: str) -> str:
    """Evaluate team_performance: Team statistics and trends by team name. Create a SQL query to evaluate the team performance. and then use execute_query tool to execute the query."""
    prompt = f"""
    You are an expert SQL agent. Given the database dialect and table information, generate a SQL query to evaluate the performance of the team named '{team_name}'.
    Use the following table information:
    {table_info}
    Ensure the SQL query is syntactically correct for the '{dialect}' dialect.
    """
    return prompt     

@mcp.tool
def season_comparision( season1: int, season2: int) -> str:
    "season_comparisons: Cross-season analysis"
    prompt = f"""
    You are an expert SQL agent. Given the database dialect and table information, generate a SQL query to compare the performance of two seasons: {season1} and {season2}.
    Use the following table information:
    {table_info}
    Ensure the SQL query is syntactically correct for the '{dialect}' dialect.
    """
    return prompt   

@mcp.tool
def head_to_head(team1: str, team2: str) -> str:
    """head_to_head: Team vs team historical data"""
    prompt = f"""
    You are an expert SQL agent. Given the database dialect and table information, generate a SQL query to analyze the head-to-head historical performance between '{team1}' and '{team2}'.
    Use the following table information:
    {table_info}
    Ensure the SQL query is syntactically correct for the '{dialect}' dialect.
    """

    return prompt


if __name__ == "__main__":
    mcp.run()