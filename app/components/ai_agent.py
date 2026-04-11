from langchain_groq import ChatGrpq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_prebuilt import create_react_agent
from langchain_core.message.ai import AIMessage
from app.config.settings import Settings

def get_response_from_ai_agents(llm_id, query,allow_search,system_prompt):
    llm=ChatGrpq(model=llm_id)
    tools=[TavilySearchResults(max_results=2)] if allow_search else []
