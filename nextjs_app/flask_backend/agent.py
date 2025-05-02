import os
import json
import operator
from typing import TypedDict, Annotated
import copy

from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END

# --- Agent State Definition ---
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

# --- Base Agent Class (Modified with Print Statements) ---
class Agent:
    def __init__(self, model, tools, system_prompt):
        print("--- Agent Initializing ---")
        self.last_message = ""
        self.system = system_prompt
        self.tools = {t.name: t for t in tools}
        print(f"Tools loaded: {list(self.tools.keys())}")
        self.model = model.bind_tools(tools)
        print("Model bound with tools.")

        # --- Graph Definition ---
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        print("Added node: llm")
        graph.add_node("action", self.take_action)
        print("Added node: action")

        # Conditional Edge: llm -> exists_action -> action or END
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END} # Route to action if tool calls exist, else end
        )
        print("Added conditional edge from 'llm' based on 'exists_action'")

        # Edge: action -> llm
        graph.add_edge("action", "llm")
        print("Added edge from 'action' to 'llm'")

        # Set Entry Point
        graph.set_entry_point("llm")
        print("Set graph entry point to 'llm'")

        # Compile Graph
        self.graph = graph.compile()
        print("--- Agent Graph Compiled ---")
        # --- End Graph Definition ---

    def exists_action(self, state: AgentState):
        print("\n--- Checking for Action ---")
        result = state['messages'][-1]
        # Check if the last message has the 'tool_calls' attribute and if it's non-empty
        has_tool_calls = hasattr(result, 'tool_calls') and len(result.tool_calls) > 0
        print("hasattr(result, 'tool_calls'): ", hasattr(result, 'tool_calls'))
        print("len(result.tool_calls) > 0: ", len(result.tool_calls) > 0)

        if has_tool_calls:
            print(f"Action Required: YES. Tool calls found: {result.tool_calls}")
            return True
        else:
            print("Action Required: NO. No tool calls found in last message.")
            # Optionally print the last message content if no tool calls
            # print(f"Last Message Content: {result.content}")
            return False

    def call_openai(self, state: AgentState):
        print("\n--- Calling LLM ---")
        messages = state['messages']
        print(f"Messages received by call_openai node: {messages}")

        messages_to_send = []
        is_tool_response_turn = messages and isinstance(messages[-1], ToolMessage)

        if self.system:
            print("Prepending system prompt.")
            messages_to_send = [SystemMessage(content=self.system)] + messages
        else:
            print("No system prompt defined for this agent.")
            messages_to_send = messages

        # --- Add Check for Tool Call / Response Counts ---
        if is_tool_response_turn:
            print("\n--- Verifying Tool Call/Response Counts ---")
            num_calls_requested = 0
            # Find the last AI message that requested tool calls
            ai_message_with_calls = None
            for msg in reversed(messages_to_send):
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    ai_message_with_calls = msg
                    break

            if ai_message_with_calls:
                num_calls_requested = len(ai_message_with_calls.tool_calls)
                print(f"Number of tool calls requested in preceding AIMessage: {num_calls_requested}")
                print(f"Tool Calls: {ai_message_with_calls.tool_calls}") # Optional: print details
            else:
                print("Warning: Could not find preceding AIMessage with tool_calls in history.")

            num_responses_provided = 0
            # Count consecutive ToolMessages at the end of the list
            for msg in reversed(messages_to_send):
                if isinstance(msg, ToolMessage):
                    num_responses_provided += 1
                else:
                    # Stop counting once we hit a non-ToolMessage
                    break
            print(f"Number of ToolMessages being sent as responses: {num_responses_provided}")

            if num_calls_requested != num_responses_provided:
                print(f"!!! MISMATCH DETECTED: Requested Calls ({num_calls_requested}) != Provided Responses ({num_responses_provided}) !!!")
            else:
                print("Counts appear to match.")
            print("--------------------------------------------")
        # --- End Check ---

        # --- Debug Print for final list ---
        print(f"\n--- Final message list being sent to self.model.invoke:\n{messages_to_send}\n-------------------------------------")
        # --- End Debug Print ---

        # Invoke the LLM
        try:
            message = self.model.invoke(messages_to_send)
        except Exception as e:
            print(f"!!! ERROR during self.model.invoke: {e}")
            raise e

        print(f"\nLLM Response Object: {message}")
        print(f"LLM Response Content: {message.content}")

        if hasattr(message, 'tool_calls') and message.tool_calls:
         print(f"LLM Response includes VALID tool_calls: {message.tool_calls}")
        else:
            print("LLM Response does NOT include valid tool_calls.")

        # --- : Check for INVALID tool calls ---
        if hasattr(message, 'invalid_tool_calls') and message.invalid_tool_calls:
            print(f"!!! WARNING: LLM Response includes INVALID tool_calls: {message.invalid_tool_calls}")
        else:
            print("LLM Response does NOT include invalid tool_calls.")
        
        return {'messages': [message]}

    def take_action(self, state: AgentState):
        print("\n--- Taking Action ---")
        # Get the last message from the state
        last_message = state['messages'][-1]
        print(f"Last message type: {type(last_message)}")
        
        # Check if message has tool_calls attribute
        if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
            print("No tool calls found in the message")
            return {'messages': []}
        
        # Process each tool call
        actions = []
        for tool_call in last_message.tool_calls:
            print(f"Tool call structure: {tool_call}")
            
            # Extract tool name and ID based on the structure
            if isinstance(tool_call, dict):
                # Check for different formats of tool_call
                if "function" in tool_call:
                    # Format: {'function': {'name': '...', 'arguments': '{...}'}, 'id': '...'}
                    tool_name = tool_call["function"]["name"]
                    tool_args = tool_call["function"]["arguments"]
                else:
                    # Format: {'name': '...', 'args': {...}, 'id': '...'}
                    tool_name = tool_call["name"]
                    tool_args = json.dumps(tool_call["args"]) if isinstance(tool_call["args"], dict) else tool_call["args"]
                
                tool_id = tool_call["id"]
            else:
                # Try attribute access
                try:
                    if hasattr(tool_call, 'function'):
                        tool_name = tool_call.function.name
                        tool_args = tool_call.function.arguments
                    else:
                        tool_name = tool_call.name
                        tool_args = json.dumps(tool_call.args) if hasattr(tool_call, 'args') else "{}"
                    
                    tool_id = tool_call.id
                except AttributeError as e:
                    print(f"Error: Unexpected tool_call format: {e}")
                    continue
                
            print(f"Processing tool call: {tool_name} (ID: {tool_id})")
            
            # Handle tavily search tool
            if tool_name == "tavily_search_results_json":
                try:
                    # Parse arguments
                    try:
                        arguments = json.loads(tool_args) if isinstance(tool_args, str) else tool_args
                    except json.JSONDecodeError:
                        print(f"Warning: Could not parse arguments as JSON: {tool_args}")
                        arguments = {"query": tool_args}
                    
                    query = arguments.get("query", "")
                    print(f"Tavily Searching: {query}")
                    
                    # Find and invoke the tool
                    tool = self.tools.get(tool_name)
                    if not tool:
                        result = [{"ERROR": f"Tool '{tool_name}' not found"}]
                        print(f"Error: Tool '{tool_name}' not found")
                    else:
                        result = tool.invoke({"query": query})
                        
                        # Check if the query contains "image" and process accordingly
                        if "image" in query.lower():
                            print(f"Image search detected in query: {query}")
                            # Extract URLs from the search results
                            urls = []
                            for item in result:
                                if "url" in item and item["url"]:
                                    urls.append(item["url"])
                            
                            if urls:
                                # Call TavilyExtract with the URLs
                                extract_tool = self.tools.get("tavily_extract")
                                if extract_tool:
                                    print(f"Calling TavilyExtract with {len(urls)} URLs")
                                    extracted_images = []
                                    
                                    for url in urls:
                                        try:
                                            print(f"Extracting images from URL: {url}")
                                            # Create a properly formatted tool call for TavilyExtract
                                            extract_tool_call = {
                                                "args": {"urls": [url]},
                                                "id": tool_id,
                                                "name": "tavily_extract",
                                                "type": "tool_call",
                                            }
                                            print(f"TavilyExtract tool call: {extract_tool_call}")
                                            extract_result = extract_tool.invoke(extract_tool_call)
                                            print(f"TavilyExtract response type: {type(extract_result)}")
                                            
                                            # The response will be a ToolMessage object with content as a string
                                            if hasattr(extract_result, 'content'):
                                                print(f"Response has content attribute: {extract_result.content}...")
                                                try:
                                                    # Parse the content as JSON
                                                    extract_data = json.loads(extract_result.content)
                                                    print(f"Parsed JSON data type: {type(extract_data)}")
                                                    
                                                    # Check for the correct nested structure
                                                    if isinstance(extract_data, dict):
                                                        # Most common structure: {"results": [{...}]}
                                                        if "results" in extract_data and isinstance(extract_data["results"], list):
                                                            for result in extract_data["results"]:
                                                                if isinstance(result, dict) and "images" in result:
                                                                    print(f"Found {len(result['images'])} images in result")
                                                                    extracted_images.extend(result["images"])
                                                        # Direct images array
                                                        elif "images" in extract_data:
                                                            print(f"Found {len(extract_data['images'])} images in dict")
                                                            extracted_images.extend(extract_data["images"])
                                                    # If it's a list, check each item
                                                    elif isinstance(extract_data, list):
                                                        for item in extract_data:
                                                            if isinstance(item, dict):
                                                                if "images" in item:
                                                                    print(f"Found {len(item['images'])} images in list item")
                                                                    extracted_images.extend(item["images"])
                                                                elif "results" in item and isinstance(item["results"], list):
                                                                    for result in item["results"]:
                                                                        if isinstance(result, dict) and "images" in result:
                                                                            print(f"Found {len(result['images'])} images in nested result")
                                                                            extracted_images.extend(result["images"])
                                                except json.JSONDecodeError:
                                                    print(f"Error parsing TavilyExtract response as JSON")
                                            # Traditional format handling
                                            elif isinstance(extract_result, dict) and "images" in extract_result:
                                                print(f"Found {len(extract_result['images'])} images in extract_result dict")
                                                extracted_images.extend(extract_result["images"])
                                            else:
                                                print(f"No images found in extract_result, format: {type(extract_result)}")
                                        except Exception as e:
                                            print(f"Error extracting from URL {url}: {e}")
                                    
                                    # Add the extracted images to the result
                                    if extracted_images:
                                        print(f"Found {len(extracted_images)} images")
                            
                                        # Create a combined result with both search results and images
                                        image_entry = {"title": "Extracted Images", 
                                                     "content": "The following images were extracted from the search results", 
                                                     "images": extracted_images}
                                        
                                        # Handle different result formats
                                        if isinstance(result, list):
                                            # If result is a list, simply append the image entry
                                            combined_result = result + [image_entry]
                                        elif isinstance(result, dict):
                                            # If result is a dict, convert to a list with the dict as first element
                                            combined_result = [result, image_entry]
                                        else:
                                            # Fallback - wrap result in a list
                                            combined_result = [{"content": str(result)}, image_entry]
                                            
                                        result = combined_result
                except Exception as e:
                    print(f"Error processing tool call: {e}")
                    result = [{"ERROR": str(e)}]
            # Handle other tools
            else:
                try:
                    # Find the tool in the tools dictionary
                    tool = self.tools.get(tool_name)
                    
                    if tool:
                        # Parse arguments
                        try:
                            arguments = json.loads(tool_args) if isinstance(tool_args, str) else tool_args
                        except json.JSONDecodeError:
                            print(f"Warning: Could not parse arguments as JSON: {tool_args}")
                            arguments = {}
                            
                        print(f"Tool arguments: {arguments}")
                        
                        # Invoke the tool
                        result = tool.invoke(arguments)
                        print(f"Tool result: {result}")
                    else:
                        result = {"ERROR": f"Tool '{tool_name}' not found"}
                        print(f"Error: Tool '{tool_name}' not found")
                except Exception as e:
                    result = {"ERROR": str(e)}
                    print(f"Error executing tool '{tool_name}': {e}")
            
            # Create a proper ToolMessage object instead of a dictionary
            if isinstance(result, list) or isinstance(result, dict):
                result_str = json.dumps(result)
            else:
                result_str = str(result)
                
            # Create a proper ToolMessage with required content field
            tool_message = ToolMessage(
                content=result_str,
                tool_call_id=tool_id
            )
            
            actions.append(tool_message)
        
        print(f"Tool execution results (as ToolMessages): {actions}")
        return {'messages': actions}

    def run(self, inputData):
        print(f"\n--- Running Agent with Input ---")
        print(f"Input Data: {inputData}")
        messages = [HumanMessage(content=inputData)]
        
        # Invoke the graph
        result_state = self.graph.invoke({"messages": messages}, {"recursion_limit": 50})
        print(f"\n--- Graph Execution Finished ---")
        print(f"Final Graph State: {result_state}")

        # Process the final message
        if result_state and 'messages' in result_state and result_state['messages']:
            final_message_content = result_state['messages'][-1].content
            print(f"Final message content (raw): {final_message_content}")
            self.last_message = self.cleanJsonContent(final_message_content) # Or cleanHtmlContent if needed
            print(f"Final message content (cleaned): {self.last_message}")
        else:
            print("Error: Graph did not return messages in final state.")
            self.last_message = "// Error: No final message content from agent."

        return result_state # Return the full state as before

    def cleanJsonContent(self, content):
        # Existing cleaning logic
        if not isinstance(content, str): # Handle potential non-string content
             print(f"Warning: cleanJsonContent received non-string type: {type(content)}")
             content = str(content)
        content = content.strip().strip("`").replace("json", "").strip().replace("\n", "").replace("  ", "")
        return content

    def cleanHtmlContent(self, content):
        # Existing cleaning logic
        if not isinstance(content, str):
             print(f"Warning: cleanHtmlContent received non-string type: {type(content)}")
             content = str(content)
        content = content.strip().strip("`").replace("html", "").strip().replace("\n", "").replace("  ", "")
        return content