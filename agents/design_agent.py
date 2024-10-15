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
    
prompt = """
Imagine you are a smart researcher who must utilize design thinking to generate customer personas, create empathy maps, and expand the problem definition, given a problem statement or product description. 
Design thinking emphasizes human thinking design and focuses on the solution to the problem rather than the problem itself. 
You are allowed to make multiple calls (either together or in sequence).
Only look up information when you are sure of what you want.
If you need to look up some information before asking a follow up question, you are allowed to do that!
Given the product description, create three customer personas to give insight into the type of users that could potentially benefit from the specified product. 
Describe each customer persona and list out their needs and pain points.
Then, create an empathy map for a typical user by researching to understand the users’ emotions and challenges. An empathy map consists of what a user says, thinks, does, and feels.
Also, create a customer journey map for a typical user. A customer journey map consists of 4 stages: awareness, comparison, purchase, and installation.
Utilize this information gained to create a clear problem statement for the issue that the product attempts to solve.
"""
#could add something to format the response of this prompt
#can expand on what a journey map is, can ask it to create empathy/journey maps for each persona

# replace with input from website
print("Enter your problem statement here: ")
query = input() # "web app about game development" 
messages = [HumanMessage(content=query)]
model = ChatOpenAI(model="gpt-3.5-turbo") 
agent = Agent(model, [tool], system=prompt) #only have 1 tavilly search tool
result = agent.graph.invoke({"messages": messages})

# for testing this output without calling the api
# result = {'messages': [HumanMessage(content='What are some customer personas for a web app about game development?', additional_kwargs={}, response_metadata={}), AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_EZfG7UXH9kiRq1MQcOcoU8EQ', 'function': {'arguments': '{"query":"customer personas for a web app about game development"}', 'name': 'tavily_search_results_json'}, 'type': 'function'}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 26, 'prompt_tokens': 159, 'total_tokens': 185, 'completion_tokens_details': {'audio_tokens': None, 'reasoning_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-c57a71df-1a16-490e-b89f-a1674b318027-0', tool_calls=[{'name': 'tavily_search_results_json', 'args': {'query': 'customer personas for a web app about game development'}, 'id': 'call_EZfG7UXH9kiRq1MQcOcoU8EQ', 'type': 'tool_call'}], usage_metadata={'input_tokens': 159, 'output_tokens': 26, 'total_tokens': 185, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}), ToolMessage(content="[{'url': 'https://gameanalytics.com/blog/how-to-create-user-personas-as-unique-as-your-audience/', 'content': 'How To Get Started Creating Unique Personas For Your Game Drawing insights from your game’s analytics and any other data that you possess \\xa0to create user personas is often best accomplished as a group exercise. This is why your personas should include some clever background details but also what type of technology each theoretical individual uses, the types of content they consume online, the social networks they participate in, their other favorite games and media, and anything else that might make an impact on the choices of the design, development, and marketing teams. As a bonus, personas can help you understand and make better use of the data in your game’s analytics by putting user behaviors into real world contexts. Building great games starts with understanding your player’s behavior – and developing detailed personas is whatof technology each theoretical individual uses, the types of content they consume online, the social networks they participate in, their other favorite games and media, and anything else that might make an impact on the choices of the design, development, and marketing teams. As a bonus, personas can help you understand and make better use of the data in your game’s analytics by putting user behaviors into real world contexts. Building great games starts with understanding your player’s behavior – and developing detailed personas is whatgame’s analytics by putting user behaviors into real world contexts. Building great games starts with understanding your player’s behavior – and developing detailed personas is what takes that understanding to the next level.'}]", name='tavily_search_results_json', tool_call_id='call_EZfG7UXH9kiRq1MQcOcoU8EQ'), AIMessage(content="One approach to creating customer personas for a web app about game development involves drawing insights from the game's analytics and other available data. The personas should include background details, the type of technology each theoretical individual uses, the content they consume online, the social networks they participate in, their favorite games and media, and other factors that  takes that understanding to the next level.'}]", name='tavily_search_results_json', tool_call_id='call_EZfG7UXH9kiRq1MQcOcoU8EQ'), AIMessage(content="One approach to creating customer personas for a web app about game development involves drawing insights from the game's analytics and other available data. The personas should include background details, the type of technology each theoretical individual uses, the content they consume online, the social networks they participate in, their favorite games and media, and other factors that ype of technology each theoretical individual uses, the content they consume online, the social networks they participate in, their favorite games and media, and other factors that can impact design, development, and marketing decisions. Building detailed personas can help understand user behaviors and enhance the understanding of player behavior for better game development. For more detailed information, you can refer to this link: [Creating Unique Personas For Your Game](https://gameanalytics.com/blog/how-to-create-user-personas-as-unique-as-your-audience/)", additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 138, 'prompt_tokens': 389, 'total_tokens': 527, 'completion_tokens_details': {'audio_tokens': None, 'reasoning_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None}, id='run-bc740dd9-9340-419a-a9a9-4752e51ddba0-0', usage_metadata={'input_tokens': 389, 'output_tokens': 138, 'total_tokens': 527, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}})]}

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
