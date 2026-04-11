from langchain_groq import ChatGrpq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_prebuilt import create_react_agent
from langchain_core.message.ai import AIMessage
from app.config.settings import Settings

def get_response_from_ai_agents(llm_id, query,allow_search,system_prompt):
    llm=ChatGrpq(model=llm_id)
    tools=[TavilySearchResults(max_results=2)] if allow_search else []

    agent=create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt

    )

    state = {"messages":query}
    response= agent.invoke(state)
    messages=response.get("messges")
    ai_messages=[message.content for message in messages if isinstance(message,AIMessage)]
    return ai_messages[-1]
