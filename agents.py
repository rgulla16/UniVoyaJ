import os
import openai
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

load_dotenv()
search_tool = DuckDuckGoSearchRun()


openai_api_key = os.getenv("OPENAI_API_KEY")
print(openai_api_key)

llm_lmstudio = ChatOpenAI(
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="",                 
    model_name="zephyr"
)

llm_janai = ChatOpenAI(
    openai_api_base="http://localhost:1337/v1",
    openai_api_key="",                 
    model_name="mistral-ins-7b-q4"
)

llm_ollama = Ollama(model="orca2")

llm_textgen = ChatOpenAI(
    openai_api_base="http://localhost:5001/v1",
    openai_api_key="",                 
    model_name="openhermes"
)

# Create a researcher agent
researcher = Agent(
  role='Country',
  goal='Discover the best country for graduate engineering education',
  backstory='Universities are researching on innovative technologies across the globe mostly in USA, UK, Europe, India and China. Tech innovation is growwing at an exponential pace',
  verbose=True,
  tools=[search_tool],
  allow_delegation=False,
  llm=llm_lmstudio
)

insight_researcher = Agent(
  role='Finance',
  goal='Discover the finaces for education',
  backstory='Graduation education is expensive, so you are able to find the cost of eduction from the data you are given.',
  verbose=True,
  tools=[search_tool],
  allow_delegation=False,
  llm=llm_lmstudio
)

writer = Agent(
  role='Weather',
  goal='Find out the weather at these universities around the year',
  backstory='Students from different countries are unable to adjust to the weather. Need to identify if the weather conditions are suitable',
  verbose=True,
  tools=[search_tool],
  allow_delegation=False,
  llm=llm_lmstudio
)

formater = Agent(
  role='Markdown Formater',
  goal='Format the text in markdown',
  backstory='You are able to convert the text into markdown format',
  verbose=True,
  tools=[search_tool],
  allow_delegation=False,
  llm=llm_lmstudio
)

# Tasks
# research_task = Task(
#   description='Identify the next big trend in AI by searching internet',
#   agent=researcher
# )
research_task = Task(
    description="Identify the top universities providing best education in Robotics",
    expected_output="Everything about Robotics.",
    input_type=dict,
    agent=researcher
)

# insights_task = Task(
#   description='Identify few key insights from the data in points format. Dont use any tool',
#   agent=insight_researcher
# )

insights_task = Task(
    description="Identify the universities that are financially viable and are great value for money",
    expected_output="The insights you can derive by looking at low cost options in top universities",
    input_type=dict,
    agent=insight_researcher
)


# writer_task = Task(
#   description='Write a short blog post with sub headings. Dont use any tool',
#   agent=writer
# )
print('before writer_task')

writer_task = Task(
    description="Write a short blog post with the weather information for the university. Dont use any tool",
    expected_output="A well-written document that is informative and easy to understand.",
    input_type=dict,
    agent=writer
)

# format_task = Task(
#   description='Convert the text into markdown format. Dont use any tool',
#   agent=formater
# )

format_task = Task(
    description="Convert the text into markdown format. Dont use any tool",
    expected_output="A well-written document that is informative and easy to understand.",
    input_type=dict,
    agent=writer
)

# Instantiate your crew
tech_crew = Crew(
  agents=[researcher, insight_researcher, writer, formater],
  tasks=[research_task, insights_task, writer_task, format_task],
  process=Process.sequential  # Tasks will be executed one after the other
)
# Instantiate your crew
# tech_crew = Crew(
#   agents=[insight_researcher, writer, formater],
#   tasks=[insights_task, writer_task, format_task],
#   process=Process.sequential  # Tasks will be executed one after the other
# )

# Begin the task execution
print('before kickoff')
result = tech_crew.kickoff()
print('after kickoff')
print(result)