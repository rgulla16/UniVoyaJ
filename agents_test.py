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
  role='Senior Researcher',
  goal='Discover groundbreaking technologies',
  backstory='A curious mind fascinated by cutting-edge innovation and the potential to change the world, you know everything about tech.',
  verbose=True,
  tools=[search_tool],
  allow_delegation=False,
  llm=llm_lmstudio
)

insight_researcher = Agent(
  role='Insight Researcher',
  goal='Discover Key Insights',
  backstory='You are able to find key insights from the data you are given.',
  verbose=True,
  allow_delegation=False,
  llm=llm_janai
)

writer = Agent(
  role='Tech Content Strategist',
  goal='Craft compelling content on tech advancements',
  backstory="""You are a content strategist known for making complex tech topics interesting and easy to understand.""",
  verbose=True,
  allow_delegation=False,
  llm=llm_ollama
)

formater = Agent(
  role='Markdown Formater',
  goal='Format the text in markdown',
  backstory='You are able to convert the text into markdown format',
  verbose=True,
  allow_delegation=False,
  llm=llm_textgen
)

# Tasks
# research_task = Task(
#   description='Identify the next big trend in AI by searching internet',
#   agent=researcher
# )
research_task = Task(
    description="Identify the next big trend in AI by searching internet...",
    expected_output="Everything about tech.",
    input_type=dict,
    agent=researcher
)

# insights_task = Task(
#   description='Identify few key insights from the data in points format. Dont use any tool',
#   agent=insight_researcher
# )

insights_task = Task(
    description="Identify few key insights from the data in points format. Dont use any tool",
    expected_output="The insights you can derive from the data you are given.",
    input_type=dict,
    agent=insight_researcher
)


# writer_task = Task(
#   description='Write a short blog post with sub headings. Dont use any tool',
#   agent=writer
# )
print('before writer_task')

writer_task = Task(
    description="Write a short blog post with sub headings. Dont use any tool",
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

# Begin the task execution
print('before kickoff')
result = tech_crew.kickoff()
print('after kickoff')
print(result)