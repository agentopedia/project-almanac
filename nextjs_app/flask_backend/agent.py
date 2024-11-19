from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:
    
    def __init__(self, model, tools, system=""):
        self.system = system 
        graph = StateGraph(AgentState) #initalizing state graph with agent state, has no nodes
        graph.add_node("llm", self.call_llm)  #node that executes the llm
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
    def call_llm(self, state: AgentState):
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
    
    def run(self, inputData):
        messages = [HumanMessage(content = inputData)]
        result = self.graph.invoke({"messages": messages})
        return result