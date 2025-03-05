import os
import json

from agent import Agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


class BusinessModelAgent(Agent):
    jsonFormat = {
        "customer_segments": [],
        "value_propositions": [],
        "channels": [],
        "customer_relationships": [],
        "revenue_streams": [],
        "key_resources": [],
        "key_activities": [],
        "key_partnerships": [],
        "cost_structure": []
    }

    prompt = f"""You are a strategic business analyst tasked with creating a comprehensive business model canvas for a product. 
    Based on a provided problem statement, describe the following components of a business model canvas:
    1. Customer Segments: Who are the customers?
    2. Value Propositions: What value does the product provide?
    3. Channels: How does the product reach customers?
    4. Customer Relationships: How does the product interact with customers?
    5. Revenue Streams: How does the product make money?
    6. Key Resources: What resources are essential?
    7. Key Activities: What activities are crucial for the business?
    8. Key Partnerships: Who are the partners?
    9. Cost Structure: What are the main costs?

    Return the output in JSON using the following JSON format:
    {json.dumps(jsonFormat, indent = 4)}
    """

    def __init__(self, model, tools):
        super().__init__(model, tools, self.prompt)
    
    def run(self, inputData):
        result = super().run(inputData)
        return result

    def cleanJsonContent(self, content):
        # Remove the Markdown code block delimiters (```json and ```
        content = content.strip()
        if content.startswith('```json'):
            content = content[len('```json'):].strip() 
        if content.endswith('```'):
            content = content[:-3].strip() 
        return content

    def convertToMarkdown(self, content):
        # Convert the business model canvas JSON content to markdown format
        sections = [
            ("# Customer Segments", "customer_segments"),
            ("# Value Propositions", "value_propositions"),
            ("# Channels", "channels"),
            ("# Customer Relationships", "customer_relationships"),
            ("# Revenue Streams", "revenue_streams"),
            ("# Key Resources", "key_resources"),
            ("# Key Activities", "key_activities"),
            ("# Key Partnerships", "key_partnerships"),
            ("# Cost Structure", "cost_structure")
        ]
        markdown = "## Business Model Canvas\n\n"
        data = json.loads(content)
        for title, key in sections:
            markdown += f"{title}\n"
            items = data.get(key, [])
            if items:
                markdown += "\n".join(f"- {item}" for item in items)
            markdown += "\n\n"
        return markdown

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

