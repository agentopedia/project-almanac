import os
import json
import operator

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END

from typing import TypedDict, Annotated

os.environ['GOOGLE_API_KEY'] = ""
gemini_api_key = os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.environ['TAVILY_API_KEY']

# Initialize the Gemini LLM
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

tools = [TavilySearchResults(max_results = 1, api_key = tavily_api_key)]


class ProductViabilityState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class ProductViabilityAgent:
    jsonFormat = {
        "market_demand": "",
        "competitive_analysis": "",
        "financial_analysis": {
            "revenue_projections": "",
            "cost_projections": "",
            "break_even_analysis": ""
        },
        "feature_set": []
    }

    prompt = f"""You are a product viability analyst tasked with evaluating the feasibility of a Minimum Viable Product (MVP) based on the output of a design thinking agent and a business model agent.
    Based on the provided information, describe the following components:
    1. Market Demand: Evaluate the size and growth potential of the target market.
    2. Competitive Analysis: Analyze the existing solutions in the market and identify opportunities for differentiation.
    3. Financial Analysis:
        - Revenue Projections: Estimate potential revenue streams based on the business model canvas. Determine a realistic dollar amount for each stream.
        - Cost Projections: Calculate the costs associated with developing and maintaining the MVP, also using reasonable dollar amounts.
        - Break-Even Analysis: Determine the break-even point for the MVP. 
    4. Feature Set: Propose a feature set for the MVP that addresses the problem statement and meets the needs of the customer segments.

    Return the output in both plaintext and JSON in the following JSON format:
    {json.dumps(jsonFormat, indent = 4)}
    """

    def __init__(self, model, tools, system=prompt):
        self.system = system
        graph = StateGraph(ProductViabilityState)
        graph.add_node("llm", self.evaluateProductViability)
        graph.add_node("action", self.performResearch)
        graph.add_conditional_edges(
            "llm",
            self.needsAdditionalResearch,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {tool.name: tool for tool in tools}
        self.model = model.bind_tools(tools)

    def needsAdditionalResearch(self, state: ProductViabilityState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    """
    def evaluateProductViability(self, state: ProductViabilityState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        # Add a tool call to trigger the performResearch method
        messages.append(ToolMessage(tool_call_id="1", name="tavily_search", arguments={"query": "financial data for the target market"}))
        message = self.model.invoke(messages)
        return {'messages': [message]}
    """

    def performResearch(self, state: ProductViabilityState):
        toolCalls = state['messages'][-1].tool_calls
        results = []
        for call in toolCalls:
            if call['name'] not in self.tools:
                result = "Unknown tool name; please retry."
            else:
                # Extract relevant information from the previous agents' responses
                previous_messages = state['messages'][:-1]
                target_market = self.extractTargetMarket(previous_messages)
                financial_data_points = self.extractFinancialDataPoints(previous_messages)

                # Construct a specific query for Tavily
                query = f"Financial data for the {target_market} industry, including global {target_market} worth, demand, and expected growth."
                result = self.tools[call['name']].invoke({"query": query})
                #financial_data = self.extractFinancialData(search_results)
                #result = self.analyzeFinancialData(financial_data)
            results.append(ToolMessage(tool_call_id=call['id'], name=call['name'], content=str(result)))
        return {'messages': results}

    def extractTargetMarket(self, messages):
        target_market = ""
        for message in messages:
            if message.content.startswith("{") and message.content.endswith("}"):
                try:
                    data = json.loads(message.content)
                    if "target_market" in data:
                        target_market = ", ".join(data["target_market"])
                        break
                except json.JSONDecodeError:
                    pass
        return target_market


    def run(self, inputData):
        messages = [HumanMessage(content = inputData)]
        result = self.graph.invoke({"messages": messages})
        return result
