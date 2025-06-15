from agent import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
import json5
import os

input_format = {"customer_persona": [{"name":"","demographics":{"age":0,"gender":"","occupation":""},"description":"Brief background and lifestyle information."}],
  "app": "Implementation of the application as React code"} #if there's another css file, you should add that here

response_format = {
  "overview": "Summary of the application's feedback.",
  "usability": "Feedback about the useability and interactivity of the application.",
  "content": "Feedback about the informational value of the content presented in the app.",
  "appearance": "Feedback about the app's appearance, aesthetics, color scheme, text layout and font size, and visual media such as images and graphs.",
  "improvements": [ "List of specific and actionable improvements the customer wants to the app."]
}
class CustomerFeedbackAgent(Agent):
    #change prompt if we decide to use a css file
    prompt = f"""Imagine you are a customer for a Next.js MVP application. You will receive:  
        1. A JSON object containing the application as React code. 
        2. A JSON object containing details about the customer you are embodying.  
        The JSON objects you receive will follow the following format:
        {input_format}

        Take time to understand the customer's characteristics, thoughts, and needs. Then, review the React code and corresponding css sheet from their perspective and provide feedback on the product’s usability, content, and appearance. 
        Go in depth and be specific about the feedback needed, mentioning specific parts of the applciation that need improvements.
        Return your response as a single-line JSON object with double quotes, ensuring all fields are fully populated:
        {response_format}
        """


    #you get the feedback and then you send the feedback through an api route that goes to the software agent and has it update the original generated mvp and replace the file that its on

    def __init__(self, model, tools):
        self.product_idea = ""
        super().__init__(model, tools, self.prompt)

    def run(self, inputData):
        self.product_idea = inputData
        result = super().run(inputData)
        return result
