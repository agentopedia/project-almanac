import os
import json
import operator

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from typing import TypedDict, Annotated

gemini_api_key = os.environ["GEMINI_API_KEY"]
tavily_api_key = os.environ['TAVILY_API_KEY']
secret_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

tools = [TavilySearchResults(max_results = 1, api_key = tavily_api_key)]

settings = {
    "client_config_backend": "service",
    "service_config": {
        "client_json_file_path": secret_file,
    }
}

gauth = GoogleAuth(settings = settings)
gauth.ServiceAuth()
drive = GoogleDrive(gauth)

class BusinessModelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class BusinessModelAgent:
    jsonFormat = {
        "target_market": [],
        "customer_segments": [],
        "value_propositions": [],
        "channels": [],
        "customer_relationships": [],
        "revenue_streams": [],
        "key_resources": [],
        "key_activities": [],
        "key_partnerships": [],
        "cost_structure": []
    }

    prompt = f"""You are a strategic business analyst tasked with creating a comprehensive business model canvas for a product. 
    Based on a provided problem statement, describe the following components of a business model canvas:
    0. Target Market: What is the target market?
    1. Customer Segments: Who are the customers?
    2. Value Propositions: What value does the product provide?
    3. Channels: How does the product reach customers?
    4. Customer Relationships: How does the product interact with customers?
    5. Revenue Streams: How does the product make money?
    6. Key Resources: What resources are essential?
    7. Key Activities: What activities are crucial for the business?
    8. Key Partnerships: Who are the partners?
    9. Cost Structure: What are the main costs?

    Return the output in both plaintext and JSON in the following JSON format:
    {json.dumps(jsonFormat, indent = 4)}
    """

    def __init__(self, model, tools, system=prompt):
        self.system = system
        graph = StateGraph(BusinessModelState)
        graph.add_node("llm", self.generateBusinessModel)
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

    def needsAdditionalResearch(self, state: BusinessModelState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def generateBusinessModel(self, state: BusinessModelState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def performResearch(self, state: BusinessModelState):
        toolCalls = state['messages'][-1].tool_calls
        results = []
        for call in toolCalls:
            if call['name'] not in self.tools:
                result = "Unknown tool name; please retry."
            else:
                result = self.tools[call['name']].invoke(call['args'])
            results.append(ToolMessage(tool_call_id=call['id'], name=call['name'], content=str(result)))
        return {'messages': results}

    def run(self, inputData):
        def createDocument(content):
            gdoc = drive.CreateFile({'title': 'Business Model Canvas'})
            gdoc.SetContentString(content)
            gdoc.Upload()
            gdoc.InsertPermission({"type": "anyone", "value": "anyone", "role": "writer"})
            return gdoc["alternateLink"]

        messages = [HumanMessage(content = inputData)]
        result = self.graph.invoke({"messages": messages})

        documentURL = createDocument("Business Model Canvas", result['messages'][-1].content)
        print(f"\n\nBusiness Model Canvas document created. You can view it at: {documentURL}")
        return result