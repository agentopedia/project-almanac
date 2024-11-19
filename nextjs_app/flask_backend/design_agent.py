# from langchain_openai import ChatOpenAI #langchain wrapper for openAI
from langchain_google_genai import ChatGoogleGenerativeAI
from agent import Agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
import os

os.environ['GOOGLE_API_KEY'] = "AIzaSyCmUDbVAOGcRZcOKP4q6mmeZ7Gx1WgE3vE"
gemini_api_key = os.getenv("GOOGLE_API_KEY")

os.environ['TAVILY_API_KEY'] = "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" #set tavily api key here
tavily_api_key= os.getenv("TAVILY_API_KEY")

class DesignThinkingAgent:
    tool = TavilySearchResults(max_results=1, api_key=tavily_api_key)
    #NEED TO HAVE THIS AS A SINGLE LINE
    json_format = {"customer_persona":[{"name":"Persona 1","demographics":{"age":0,"gender":"","occupation":""},"description":"Brief background and lifestyle information."}],"empathy_map":{"says":["What the persona verbally expresses about the problem."],"thinks":["What the persona is thinking internally."],"does":["Actions the persona takes to address the problem."],"feels":["Emotions experienced by the persona."]},"customer_journey_map":{"awareness":"How the persona becomes aware of the product or problem.","comparison":"How the persona evaluates different options.","purchase":"Factors influencing the purchase decision.","installation":"Persona's experience with setting up or using the product."},"problem_statement":"A clear, concise statement that defines the issue the product is trying to solve."}

    prompt = f""" You are a smart researcher who must utilize design thinking to generate customer personas, given a product description. 
    Use Tavilly to do research on the product description and use the information gained to create a customer persona that would benefit from the specified product. 
    You are allowed to make multiple calls (either together or in sequence).
    Only look up information when you are sure of what you want.
    Describe the customer persona and list their pain points.
    Then, create an empathy map for a this user that consists of what the user says, thinks, does, and feels.
    Also, create a customer journey map for this typical user that consists of 4 stages: awareness, comparison, purchase, and installation.
    Utilize the information gained to create a clear problem statement for the described product.

    Give output in the following json format on one line, making sure to use double quotes:
    {json_format}
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    
    def __init__(self):
        self.agent = Agent(self.model, [self.tool], system = self.prompt) #all the functionality is stored in the agent attribute

# example usage of this class
# design = DesignThinkingAgent()
# result = design.agent.run("web app about caligraphy")
# print(result['messages'][-1].content) #last message's content

