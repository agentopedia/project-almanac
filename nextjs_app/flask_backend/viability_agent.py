import os
import json

from agent import Agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
# from pydrive2.auth import GoogleAuth
# from pydrive2.drive import GoogleDrive

# secret_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# settings = {
#     "client_config_backend": "service",
#     "service_config": {
#         "client_json_file_path": secret_file,
#     }
# }

# gauth = GoogleAuth(settings = settings)
# gauth.ServiceAuth()
# drive = GoogleDrive(gauth)

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

# os.environ['TAVILY_API_KEY'] = "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" #set tavily api key here
# tavily_api_key= os.getenv("TAVILY_API_KEY")
# os.environ['GOOGLE_API_KEY'] = "AIzaSyCmUDbVAOGcRZcOKP4q6mmeZ7Gx1WgE3vE"
# gemini_api_key = os.getenv("GOOGLE_API_KEY")

# tools = [TavilySearchResults(max_results = 1, api_key = tavily_api_key)]
# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
# viability = ProductViabilityAgent(model=model, tools=tools)
# data = "Biology professors and students lack a comprehensive, accurate, and engaging online resource for learning about frog species, leading to frustration, time wasted on searching multiple sources, and a suboptimal learning experience."
# result = viability.run(data) #data from design thinking agent
# print(viability.cleanJsonContent(viability.last_message))

#     def format_document_headers(self, document_url):

#         document_id = document_url.split('/d/')[1].split('/')[0]
#         print(document_id)

#         doc = self.service.documents().get(documentId = document_id).execute()
#         print(doc)
#         body = doc.get('body')

#         requests = []

#         for content in body.get('content', []):
#             paragraph = content.get('paragraph')
#             if not paragraph:
#                 continue

#             for element in paragraph.get('elements', []):
#                 text_run = element.get('textRun')
#                 if not text_run:
#                     continue

#                 text = text_run.get('content', '')

#                 # Identify markdown headers and update the style
#                 if text.startswith('# '):
#                     # Heading 1
#                     requests.append({
#                         'updateParagraphStyle': {
#                             'range': {
#                                 'startIndex': element['startIndex'],
#                                 'endIndex': element['endIndex']
#                             },
#                             'paragraphStyle': {'namedStyleType': 'HEADING_1'},
#                             'fields': 'namedStyleType',
#                         }
#                     })
#                     # Remove the '#' and space
#                     requests.append({
#                         'replaceAllText': {
#                             'containsText': {'text': '# '},
#                             'replaceText': '',
#                         }
#                     })
#                 elif text.startswith('## '):
#                     # Heading 2
#                     requests.append({
#                         'updateParagraphStyle': {
#                             'range': {
#                                 'startIndex': element['startIndex'],
#                                 'endIndex': element['endIndex']
#                             },
#                             'paragraphStyle': {'namedStyleType': 'HEADING_2'},
#                             'fields': 'namedStyleType',
#                         }
#                     })
#                     # Remove the '##' and space
#                     requests.append({
#                         'replaceAllText': {
#                             'containsText': {'text': '## '},
#                             'replaceText': '',
#                         }
#                     })
#                 elif text.startswith('### '):
#                     # Heading 3
#                     requests.append({
#                         'updateParagraphStyle': {
#                             'range': {
#                                 'startIndex': element['startIndex'],
#                                 'endIndex': element['endIndex']
#                             },
#                             'paragraphStyle': {'namedStyleType': 'HEADING_3'},
#                             'fields': 'namedStyleType',
#                         }
#                     })
#                     # Remove the '###' and space
#                     requests.append({
#                         'replaceAllText': {
#                             'containsText': {'text': '### '},
#                             'replaceText': '',
#                         }
#                     })

#         # Apply the formatting requests to the document
#         if requests:
#             self.service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
#             print('Document headers formatted successfully.')
#         else:
#             print('No headers to format.')
