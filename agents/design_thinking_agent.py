from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI 
from langchain_community.tools.tavily_search import TavilySearchResults
import operator
import json

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class DesignThinkingAgent:
    jsonFormat = {
        "customer_personas": [
            {
                "name": "Persona 1",
                "demographics": {"age": 0, "gender": "", "occupation": ""},
                "description": "Brief background and lifestyle information.",
                "needs": ["Need 1", "Need 2", "Need 3"],
                "pain_points": ["Pain Point 1", "Pain Point 2", "Pain Point 3"]
            },
            {
                "name": "Persona 2",
                "demographics": {"age": 0, "gender": "", "occupation": ""},
                "description": "Brief background and lifestyle information.",
                "needs": ["Need 1", "Need 2", "Need 3"],
                "pain_points": ["Pain Point 1", "Pain Point 2", "Pain Point 3"]
            },
            {
                "name": "Persona 3",
                "demographics": {"age": 0, "gender": "", "occupation": ""},
                "description": "Brief background and lifestyle information.",
                "needs": ["Need 1", "Need 2", "Need 3"],
                "pain_points": ["Pain Point 1", "Pain Point 2", "Pain Point 3"]
            }
        ],
        "empathy_map": {
            "says": ["What the persona verbally expresses about the problem."],
            "thinks": ["What the persona is thinking internally."],
            "does": ["Actions the persona takes to address the problem."],
            "feels": ["Emotions experienced by the persona."]
        },
        "customer_journey_map": {
            "awareness": "How the persona becomes aware of the product or problem.",
            "comparison": "How the persona evaluates different options.",
            "purchase": "Factors influencing the purchase decision.",
            "installation": "Persona's experience with setting up or using the product."
        },
        "problem_statement": "A clear, concise statement that defines the issue the product is trying to solve."
    }

    prompt = f""" You are a smart researcher who must utilize design thinking to generate customer personas, create empathy maps, and expand the problem definition, given a problem statement or product description. 
    You are allowed to make multiple calls (either together or in sequence).
    Only look up information when you are sure of what you want.
    If you need to look up some information before asking a follow up question, you are allowed to do that!
    Use Tavilly to do research on the problem statement and use the information gained to create 3 customer personas that give insight into the type of users that could benefit from the specified product. 
    Describe each customer persona and list out their needs and pain points.
    Then, create an empathy map for a typical user by researching to understand the users’ emotions and challenges. An empathy map consists of what a user says, thinks, does, and feels.
    Also, create a customer journey map for a typical user. A customer journey map consists of 4 stages: awareness, comparison, purchase, and installation.
    Utilize this information gained to create a clear problem statement for the issue that the product attempts to solve.

    Give output in plaintext and in JSON, using the following JSON format:
    {json.dumps(jsonFormat, indent = 4)}
    """

    def __init__(self, model, tools, system = prompt):
        self.system = system

        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm", 
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def take_action(self, state: AgentState):
        toolCalls = state['messages'][-1].tool_calls
        results = []
        for toolCall in toolCalls:
            if not toolCall['name'] in self.tools:
                result = "Unknown tool name; please retry."
            else:
                result = self.tools[toolCall['name']].invoke(toolCall['args'])
            results.append(ToolMessage(tool_call_id = toolCall['id'], name = toolCall['name'], content = str(result)))
        return {'messages': results}
    
    def run(self, inputData):
        messages = [HumanMessage(content = inputData)]
        result = self.graph.invoke({"messages": messages})
        return result