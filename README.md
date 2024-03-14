# UniVoyaJ
The Voyage of finding the right University for higher education

# Technologies 
## Scraping 
BeautifulSoup, 
selenium, 
Chrome webdriver

## Webpage and graphs
Streamlit,  
Pandas, 
Folium, 
Altair

## LLM Agents 
Duckduckgo, 
CrewAI, 
Openai, 
lmstudio-zephyr

# For Testing used the below but not for the final application
Janai- mistral-ins-7b-q4
Ollama-orca2
Webui textgen-openhermes

# Web portal to assist students seeking undergrad and graduation eduction 
Many students rely on information from websites, consultants and their seniors for deciding on the universities they need to apply for higher education. They often waste time and money applying to universities where they dont stand a chance, cannot afford or dont like the demographics. This portal assists students by making the information available in a manner that they can easily navigate. The LLM Agents further assist them in summarizing their preferences. 


# Components of the system

# scraper code
After looking at multiple university ranking sites like USNews, QS Ranking etc, I narrowed down the below site as the data is more consistent in this site. This exercise has been very tedious and difficult. 

Finally I am retrieving the university ranks from this website https://www.shanghairanking.com/rankings/arwu/2023 using the code
'scraper_shanghai_ranking_recursive_csv.py' code. This writes to the 'univ_rank.csv' file. I am using Chrome webdriver to achieve this. 

There are " " for some of the university names and it can also be seen that the ranking information retrieved is as below 
"98,Brown University,us.png,38,25.1
98,McMaster University,ca.png,5,25.1
98,Stockholm University,se.png,3,25.1
101-150,Arizona State University,us.png,39-51,
101-150,Beijing Institute of Technology,cn.png,11-23,
101-150,Boston University,us.png,39-51,"

To clean this, I am using the 'scraper_shanghai_clean.py' code. The cleaned data is stored in 'univ_rank_clean.csv' file. 

This data is as below
"97,Purdue University  West Lafayette,US,37,25.2
98,Brown University,US,38,25.1
99,McMaster University,CA,5,25.1
100,Stockholm University,SE,3,25.1
101,Arizona State University,US,39-51,
102,Beijing Institute of Technology,CN,11-23,"

Now I am using 'scraper_shanghai_uni_details.py' code to recursively go and get the detailed information for the top 10 sites so that I can show the details on my webpage. I am not doing this for all the 1000 universities as I will do it once I get all the data including the contact details and email information and store it in my database once for all. This is static information and I plan to scrape one in 6 months by setting up the github actions. 

# website main page

The main website displays a left panel with a country and a state selection dropdowns based on which the top 10 universities are show in the right panel along with the location information on a map.

Based on the selection criteria, the relevant universities are filtered and shown in the right panel and on the map.
This is the 'app.py' code which uses streamlit to run as a web application.

# Details page. 
By clicking on the Show 'Univ details' button below each of the universities, you can navigate to the university detail page. 
Here  I am using the 'univ_details.py' which is also a streamlit web page.

# Analytics page
Here I am showing the 3 bar graphs of the top 1000 universities using the filters based on country, world ranking and national ranking. 
I am using altair and running the 'graphs.py' file as a streamlit web application. 

# LLM Agents

Here I exprerimented with openai, duckduckgo, lmstudio-zephyr, janai- mistral-ins-7b-q4, ollama-orca2, webui textgen-openhermes
I ran all these LLMS simultaneously assigning them to do one agent task each. This can be seen in 'agent_test.py'. This ran into latency and GPU issues. I then used only lmsstudio and duckduckgo to write the below agents using 'agents.py' code.

Create a Researcher agent to search for the best university in different countries for Robotics.
An insight_researcher to look into the financial viability
A Writer agent to check out compatible weather in these universities 
A Formatter agent to build a report

The output from the this code can be seen at 'result.txt'

# Videos

# Website
The video of the website walkthrough is shared at
https://drive.google.com/file/d/1ZpkJMyKh9xRhPyCq6CKaHZ_SUrBaOtth/view?usp=sharing

# Scraper
The video of the scraping walkthrough is shared at
https://drive.google.com/file/d/1F8-nPBIa1bVXjyoNTUOXv5QWrOY26KpR/view?usp=sharing

# LLM Agents
The video of the agents walkthrough is shared at
https://drive.google.com/file/d/16FnVkyYtKrQvln75YYuY5_6Ih9WjxfME/view?usp=sharing
