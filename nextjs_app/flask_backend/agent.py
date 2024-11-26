from langgraph.graph import StateGraph, END
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:
    def __init__(self, model, tools, system_prompt):
        self.last_message = ""
        self.system = system_prompt
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

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
            results.append(ToolMessage(tool_call_id=toolCall['id'], name=toolCall['name'], content=str(result)))
        return {'messages': results}

    def run(self, inputData):
        messages = [HumanMessage(content=inputData)]
        result = self.graph.invoke({"messages": messages})
        self.last_message = self.cleanJsonContent(result['messages'][-1].content)
        return result
    
    def cleanJsonContent(self, content):
        # Remove the Markdown code block delimiters (```json and ```
        content = content.strip().strip("`").replace("json", "").strip().replace("\n", "").replace("  ", "") 
        return content
    
    def cleanHtmlContent(self, content):
        # Remove the Markdown code block delimiters (```html and ```
        content = content.strip().strip("`").replace("html", "").strip().replace("\n", "").replace("  ", "") 
        return content