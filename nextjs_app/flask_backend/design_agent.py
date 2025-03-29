from agent import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
import json
import os

class DesignThinkingAgent(Agent):
    json_format = {"customer_persona":[{"name":"","demographics":{"age":0,"gender":"","occupation":""},"description":"Brief background and lifestyle information."}],"empathy_map":{"says":["What the persona verbally expresses about the problem."],"thinks":["What the persona is thinking internally."],"does":["Actions the persona takes to address the problem."],"feels":["Emotions experienced by the persona."]},"customer_journey_map":{"awareness":"How the persona becomes aware of the product or problem.","comparison":"How the persona evaluates different options.","purchase":"Factors influencing the purchase decision.","installation":"Persona's experience with setting up or using the product."},"problem_statement":"A clear, concise statement that defines the issue the product is trying to solve."}

    prompt = f""" You are a smart researcher who must utilize design thinking to generate customer personas, given a product description. 
    Use Tavilly to do research on the product description and use the information gained to create a customer persona that would benefit from the specified product. 
    You are allowed to make multiple calls (either together or in sequence).
    Only look up information when you are sure of what you want.
    1. Describe the customer persona.
    2. Create an empathy map for this user - what does the user say, think, do , and feel?
    3. Create a customer journey map for this user that consists of awareness, comparison, purchase, and installation.
    4. Create a clear problem statement for the described product.
    Give output in the following JSON format on one line, making sure to use double quotes and making sure to fill out all parts of the JSON:
    {json_format}
    """

    def __init__(self, model, tools):
        self.product_idea = ""
        super().__init__(model, tools, self.prompt)

    def run(self, inputData):
        self.product_idea = inputData
        result = super().run(inputData)
        return result
# example usage of this class
os.environ['GOOGLE_API_KEY'] = "AIzaSyCmUDbVAOGcRZcOKP4q6mmeZ7Gx1WgE3vE"
gemini_api_key = os.getenv("GOOGLE_API_KEY")
os.environ['TAVILY_API_KEY'] = "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" #set tavily api key here
tavily_api_key= os.getenv("TAVILY_API_KEY")

tools = [TavilySearchResults(max_results = 1, api_key = tavily_api_key)]
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
design = DesignThinkingAgent(model, tools)
result = design.run("web app about caligraphy")
print(result['messages'][-1].content) #last message's content

