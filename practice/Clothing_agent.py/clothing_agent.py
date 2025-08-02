import os
import requests
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from dotenv import load_dotenv

# --- 1. Load Environment Variables ---
# Load API keys from the .env file
load_dotenv()

# Check if the required API keys are set
if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENWEATHERMAP_API_KEY"):
    raise ValueError("Please set your OPENAI_API_KEY and OPENWEATHERMAP_API_KEY in a .env file.")

# --- 2. Define Custom Tool for Weather API ---
@tool
def get_current_weather(location: str) -> str:
    """
    Get the current weather for a specified location.
    The location should be in the format 'city,country_code' (e.g., 'London,uk').
    """
    # First, get coordinates for the location using Geocoding API
    geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
    geocoding_params = {
        "q": location,
        "limit": 1,
        "appid": os.getenv("OPENWEATHERMAP_API_KEY")
    }
    
    try:
        # Get coordinates for the location
        geocoding_response = requests.get(geocoding_url, params=geocoding_params)
        geocoding_response.raise_for_status()
        geocoding_data = geocoding_response.json()
        
        if not geocoding_data:
            return f"Could not find coordinates for {location}. Please check the location name."
        
        lat = geocoding_data[0]["lat"]
        lon = geocoding_data[0]["lon"]
        city_name = geocoding_data[0]["name"]
        country = geocoding_data[0]["country"]
        
        # Now get current weather data using Current Weather API
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            "lat": lat,
            "lon": lon,
            "appid": os.getenv("OPENWEATHERMAP_API_KEY"),
            "units": "metric"  # Use Celsius for temperature
        }
        
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        # Extract relevant weather information from Current Weather API response
        temperature = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        description = weather_data["weather"][0]["description"]
        wind_speed = weather_data["wind"]["speed"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]
        
        return f"The current weather in {city_name}, {country} is {temperature}°C (feels like {feels_like}°C) with {description}. Wind speed is {wind_speed} m/s, humidity is {humidity}%, and pressure is {pressure} hPa."

    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"
    except KeyError as e:
        return f"Could not retrieve weather data for {location}. Error: {e}. Please ensure the location is correct."

# --- 3. Set Up the Agent ---

# Initialize the Language Model (LLM)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Define the list of tools the agent can use
tools = [get_current_weather]

# Create the prompt template
# This template guides the agent's reasoning process.
prompt_template = """
You are a helpful AI assistant that provides clothing recommendations based on weather data. You have access to the following tools:

{tools}

Use the following format EXACTLY:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)


# Create the agent
# The create_react_agent function creates an agent that uses the ReAct (Reasoning and Acting) framework.
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

# Create the agent executor
# The AgentExecutor is what runs the agent and its tools. [7]
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)


# --- 4. Run the Agent ---

if __name__ == "__main__":
    print("Clothing Advisor Agent is ready. Ask me what to wear for a specific location.")
    print("For example: 'What kind of clothes should I wear in Berlin,de today?' or 'Is a jacket needed in New York,us?'")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            # Invoke the agent with the user's input
            response = agent_executor.invoke({"input": f"Based on the current weather, provide clothing recommendations. {user_input}"})
            
            print(f"Agent: {response['output']}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again or type 'exit' to quit.")