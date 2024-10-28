from design_thinking_agent import DesignThinkingAgent
from business_model_agent import BusinessModelAgent

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

import os

openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

model = ChatOpenAI(model = "gpt-3.5-turbo")
tool = TavilySearchResults(max_results = 1, api_key = tavily_api_key)

designThinkingAgent = DesignThinkingAgent(model, [tool])
businessModelAgent = BusinessModelAgent(model, [tool])

query = input("Enter your problem statement or product description here: ")

print("\n\n############ Running Design Thinking Agent... ############")
designOutput = designThinkingAgent.run(query)
print("\n\n############ Design Output ############\n\n", designOutput)

if designOutput is None or 'messages' not in designOutput:
    print("Error: Design output is None or does not contain messages.")
else:
    parsedOutput = designOutput['messages'][-1].content
    print("\n\n############ Parsed Output from Design Thinking Agent ############\n", parsedOutput)

    print("\n\n############ Running Business Model Agent... ############")
    businessModelResult = businessModelAgent.run(parsedOutput)

    if businessModelResult is None:
        print("Error: Business Model result is None.")
    elif 'messages' not in businessModelResult:
        print("Error: Business Model result does not contain messages.")
    else:
        print("\n\n############ Business Model Canvas ############")
        parsedBusinessOutput = businessModelResult['messages'][-1].content
        print("\n\n" + parsedBusinessOutput)