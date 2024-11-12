from design_thinking_agent import DesignThinkingAgent
from business_model_agent import BusinessModelAgent

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults

import os
import json

# export GOOGLE_API_KEY=AIzaSyCmUDbVAOGcRZcOKP4q6mmeZ7Gx1WgE3vE
# export TAVILY_API_KEY=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
# export GOOGLE_APPLICATION_CREDENTIALS="/Users/Neo/Coding/CSE 485/Sprint Retrospective 4/almanac/agents/almanac-439923-8bcc2d95a76e.json"

gemini_api_key = os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")


model = ChatGoogleGenerativeAI(model = "gemini-1.5-flash")
tool = TavilySearchResults(max_results = 1, api_key = tavily_api_key)

designThinkingAgent = DesignThinkingAgent(model, [tool])
businessModelAgent = BusinessModelAgent(model, [tool])

def cleanJsonContent(content):
    # Remove the Markdown code block delimiters (```json and ```
    content = content.strip()
    if content.startswith('```json'):
        content = content[len('```json'):].strip() 
    if content.endswith('```'):
        content = content[:-3].strip() 
    return content

def cleanDTAOutput(parsedOutput):
    try:
        output_data = json.loads(parsedOutput)
        cleaned_output = []

        # Customer Personas
        cleaned_output.append("############ Customer Personas ############")
        for persona in output_data.get("customer_personas", []):
            cleaned_output.append(f"Persona Name: {persona.get('name')}")
            cleaned_output.append("Demographics:")
            for key, value in persona.get('demographics', {}).items():
                cleaned_output.append(f"  {key.capitalize()}: {value}")
            cleaned_output.append(f"Description: {persona.get('description')}")
            cleaned_output.append("Needs:")
            for need in persona.get('needs', []):
                cleaned_output.append(f"  - {need}")
            cleaned_output.append("Pain Points:")
            for pain_point in persona.get('pain_points', []):
                cleaned_output.append(f"  - {pain_point}")
            cleaned_output.append("")

        # Empathy Map
        cleaned_output.append("############ Empathy Map ############")
        empathy_map = output_data.get("empathy_map", {})
        for section in ['says', 'thinks', 'does', 'feels']:
            cleaned_output.append(f"{section.capitalize()}:")
            for item in empathy_map.get(section, []):
                cleaned_output.append(f"  - {item}")
            cleaned_output.append("")

        # Customer Journey Map
        cleaned_output.append("############ Customer Journey Map ############")
        journey_map = output_data.get("customer_journey_map", {})
        for stage, description in journey_map.items():
            cleaned_output.append(f"{stage.capitalize()}: {description}")
        cleaned_output.append("")

        # Problem Statement
        cleaned_output.append("############ Problem Statement ############")
        cleaned_output.append(f"{output_data.get('problem_statement', 'No problem statement provided.')}")

        return "\n".join(cleaned_output)
    
    except Exception as e:
        return f"Error parsing output: {str(e)}"

def cleanBMAOutput(parsedOutput):
    try:
        output_data = json.loads(parsedOutput)
        cleaned_output = []

        # Customer Segments
        cleaned_output.append("############ Customer Segments ############")
        for segment in output_data.get("customer_segments", []):
            cleaned_output.append(f"  - {segment}")
        cleaned_output.append("")

        # Value Propositions
        cleaned_output.append("############ Value Propositions ############")
        for proposition in output_data.get("value_propositions", []):
            cleaned_output.append(f"  - {proposition}")
        cleaned_output.append("")

        # Channels
        cleaned_output.append("############ Channels ############")
        for channel in output_data.get("channels", []):
            cleaned_output.append(f"  - {channel}")
        cleaned_output.append("")

        # Customer Relationships
        cleaned_output.append("############ Customer Relationships ############")
        for relationship in output_data.get("customer_relationships", []):
            cleaned_output.append(f"  - {relationship}")
        cleaned_output.append("")

        # Revenue Streams
        cleaned_output.append("############ Revenue Streams ############")
        for revenue in output_data.get("revenue_streams", []):
            cleaned_output.append(f"  - {revenue}")
        cleaned_output.append("")

        # Key Resources
        cleaned_output.append("############ Key Resources ############")
        for resource in output_data.get("key_resources", []):
            cleaned_output.append(f"  - {resource}")
        cleaned_output.append("")

        # Key Activities
        cleaned_output.append("############ Key Activities ############")
        for activity in output_data.get("key_activities", []):
            cleaned_output.append(f"  - {activity}")
        cleaned_output.append("")

        # Key Partnerships
        cleaned_output.append("############ Key Partnerships ############")
        for partnership in output_data.get("key_partnerships", []):
            cleaned_output.append(f"  - {partnership}")
        cleaned_output.append("")

        # Cost Structure
        cleaned_output.append("############ Cost Structure ############")
        for cost in output_data.get("cost_structure", []):
            cleaned_output.append(f"  - {cost}")
        cleaned_output.append("")

        return "\n".join(cleaned_output)

    except Exception as e:
        return f"Error parsing output: {str(e)}"

query = input("Enter your problem statement or product description here: ")

print("\n\n############ Running Design Thinking Agent... ############")
designOutput = designThinkingAgent.run(query)

if designOutput is None or 'messages' not in designOutput:
    print("Error: Design output is None or does not contain messages.")
else:
    output = designOutput['messages'][-1].content
    validJSONOutput = cleanJsonContent(content = output)
    cleanedOutput = cleanDTAOutput(parsedOutput = validJSONOutput)
    
    print("\n\n############ Parsed Output from Design Thinking Agent ############")
    print(f"\n\n{cleanedOutput}")

    print("\n\n############ Running Business Model Agent... ############")
    businessModelResult = businessModelAgent.run(cleanedOutput)

    if businessModelResult is None:
        print("Error: Business Model result is None.")
    elif 'messages' not in businessModelResult:
        print("Error: Business Model result does not contain messages.")
    else:
        output = businessModelResult['messages'][-1].content
        validJSONOutput = cleanJsonContent(content = output)
        cleanedOutput = cleanBMAOutput(parsedOutput = validJSONOutput)

        print("\n\n############ Business Model Canvas ############")
        print("\n\n" + cleanedOutput)
