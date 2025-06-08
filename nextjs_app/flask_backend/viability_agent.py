import os
import json

from agent import Agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


class ProductViabilityAgent(Agent):

    jsonFormat = {"introduction": [], "goals": [], "target_audience": [], "product_features": [], "functional_requirements": [], "nonfunctional_requirements": []}

    prompt = f"""You are a strategic product manager tasked with creating a comprehensive product requirement document for a product. 
    Based on a provided problem statement, create the following entries for product requirement document:
    1. Introduction: What is the high-level overview of the product?
    2. Goals: What are the product's objectives?
    3. Target Audience: What are the product's intended users?
    4. Product Features: What are the product's core functionalities and capabilities?
    5. Functional Requirements: What are the product's technical and functional capabilities?
    6. Nonfunctional Requirements: What are the product's quality attributes, constraints, or standards?
    Return the output in JSON using the following JSON format, remembering to use double quotes.
    {json.dumps(jsonFormat, indent = 4)}
    """

    def __init__(self, model, tools):
        self.documentUrl = ""
        super().__init__(model, tools, self.prompt)
    
    def run(self, inputData):
        def createDocument(content):
            gdoc = drive.CreateFile({'title': 'Business Model Canvas'})
            gdoc.SetContentString(content)
            gdoc.Upload()
            gdoc.InsertPermission({"type": "anyone", "value": "anyone", "role": "writer"})
            return gdoc["alternateLink"]
        result = super().run(inputData)

        # cleaned_content = self.cleanJsonContent(result['messages'][-1].content)
        # markdownContent = self.convertToMarkdown(cleaned_content)
        # self.documentUrl = createDocument(markdownContent)
        # print(f"\n\nBusiness Model Canvas document created. You can view it at: {self.documentUrl}")
        return result

    def convertToMarkdown(self, content):
        # Convert the Product Requirments Document JSON content to markdown format
        sections = [
            ("# Introduction", "introduction"),
            ("# Goals", "goals"),
            ("# Target Audience", "target_audience"),
            ("# Product Features", "product_features"),
            ("# Functional Requirements", "functional_requirements"),
            ("# Nonfunctional Requirements", "nonfunctional_requirements")
        ]
        markdown = "## Product Requirments Document\n\n"
        data = json.loads(content)
        for title, key in sections:
            markdown += f"{title}\n"
            items = data.get(key, [])
            if items:
                markdown += "\n".join(f"- {item}" for item in items)
            markdown += "\n\n"
        return markdown
