from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain_openai import ChatOpenAI #langchain wrapper for openAI
from langchain_community.tools.tavily_search import TavilySearchResults
import os

os.environ['OPENAI_API_KEY'] = "sk-proj-9AoKhDUqjgakEV8pr6hKT3BlbkFJtH39ixCJjv121zdvFibD"
openai_api_key = os.getenv("OPENAI_API_KEY")

os.environ['TAVILY_API_KEY'] = "" #set tavily api key here
tavily_api_key= os.getenv("TAVILY_API_KEY")

tool = TavilySearchResults(max_results=1, api_key=tavily_api_key)

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:
    def __init__(self, model, tools, system=""):
        self.system = system #saving system as an attribute of this class
        graph = StateGraph(AgentState) #initalizing state graph with agent state, has no nodes
        graph.add_node("llm", self.call_openai)  #node that executes the llm
        graph.add_node("action", self.take_action) #action node that calls tools
        graph.add_conditional_edges( #if there is an action, go to the action node, if there isn't go to the end
            "llm", #node where the edge starts
            self.exists_action, #function that determins where to go
            {True: "action", False: END} #if function above returns true, go to action, if false, go to end
        )
        graph.add_edge("action", "llm") #makes edge (line) from action node to llm node
        graph.set_entry_point("llm") #entry point for the graph
        self.graph = graph.compile() #compile the graph to make a langchain runable, save as an attribute
        self.tools = {t.name: t for t in tools} #model has these tools available to it
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state['messages'][-1] #get last message from state - most recent call
        return len(result.tool_calls) > 0 #if there's any tool calls, return true else false

    # AgentState has all nodes/edges
    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]} #returns the result of the llm

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls #getting last message from message list
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools: #check for bad tool name from LLM
                print("\n bad tool name")
                result = "bad tool name, retry" #instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args']) #invoke tool name and pass in the arguments
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result))) #appending the tool call to the results
        # print("Back to the model!")
        return {'messages': results}
    
json_format = {"customer_personas":[{"name":"Persona 1","demographics":{"age":0,"gender":"","occupation":""},"description":"Brief background and lifestyle information.","needs":["Need 1","Need 2","Need 3"],"pain_points":["Pain Point 1","Pain Point 2","Pain Point 3"]},{"name":"Persona 2","demographics":{"age":0,"gender":"","occupation":""},"description":"Brief background and lifestyle information.","needs":["Need 1","Need 2","Need 3"],"pain_points":["Pain Point 1","Pain Point 2","Pain Point 3"]},{"name":"Persona 3","demographics":{"age":0,"gender":"","occupation":""},"description":"Brief background and lifestyle information.","needs":["Need 1","Need 2","Need 3"],"pain_points":["Pain Point 1","Pain Point 2","Pain Point 3"]}],"empathy_map":{"says":["What the persona verbally expresses about the problem."],"thinks":["What the persona is thinking internally."],"does":["Actions the persona takes to address the problem."],"feels":["Emotions experienced by the persona."]},"customer_journey_map":{"awareness":"How the persona becomes aware of the product or problem.","comparison":"How the persona evaluates different options.","purchase":"Factors influencing the purchase decision.","installation":"Persona's experience with setting up or using the product."},"problem_statement":"A clear, concise statement that defines the issue the product is trying to solve."}

prompt = f""" You are a smart researcher who must utilize design thinking to generate customer personas, create empathy maps, and expand the problem definition, given a problem statement or product description. 
You are allowed to make multiple calls (either together or in sequence).
Only look up information when you are sure of what you want.
If you need to look up some information before asking a follow up question, you are allowed to do that!
Use Tavilly to do research on the problem statement and use the information gained to create 3 customer personas that give insight into the type of users that could benefit from the specified product. 
Describe each customer persona and list out their needs and pain points.
Then, create an empathy map for a typical user by researching to understand the users’ emotions and challenges. An empathy map consists of what a user says, thinks, does, and feels.
Also, create a customer journey map for a typical user. A customer journey map consists of 4 stages: awareness, comparison, purchase, and installation.
Utilize this information gained to create a clear problem statement for the issue that the product attempts to solve.

Give output in plaintext and in json, using the following json format:
{json_format}
"""
#can expand on what a journey map is, can ask it to create empathy/journey maps for each persona

# replace with input from website
print("Enter your problem statement here: ")
query = input() # "web app about game development" 
messages = [HumanMessage(content=query)]
model = ChatOpenAI(model="gpt-3.5-turbo") 
agent = Agent(model, [tool], system=prompt) #only have 1 tavilly search tool
result = agent.graph.invoke({"messages": messages})

# for testing this output without calling the api

# printing each message in result - the content of the last message is what we really need
for message in result['messages']:
    print("message type: " + str(type(message)).split(".")[-1][:-2])

    content = message.content
    if (content != ""):
        print(message.content)
    else:
        print("empty content")
        print("query: " + message.tool_calls[0]["args"]["query"])
    
    print("")

# print(result['messages'][-1].content) #last message's content
