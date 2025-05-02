from flask import Flask, request, jsonify

from design_agent import DesignThinkingAgent
from business_model_agent import BusinessModelAgent
from viability_agent import ProductViabilityAgent
from swe_agent import SWESystemAgent
from swe_verifier_agent import SWEVerifierAgent
from customer_feedback_agent import CustomerFeedbackAgent

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilyExtract

import json5
import json
import os
import socket
import re
import traceback

# os.environ['GOOGLE_API_KEY'] = "AIzaSyCcN7Yo1ONOFYn5wCzPcBxTXfk7wyUFlko"
# os.environ['GOOGLE_API_KEY'] = 'AIzaSyBWkci81KcDP9DGdTt_ur3o12m47gYqXec'
os.environ['GOOGLE_API_KEY'] = 'AIzaSyDS0oliZQP5gmpmoGKURXh4fQSxUZnPMg0'

gemini_api_key = os.getenv("GOOGLE_API_KEY")

os.environ['TAVILY_API_KEY'] = "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" #set tavily api key here
tavily_api_key= os.getenv("TAVILY_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
tools = [TavilySearchResults(
    max_results = 1, 
    api_key = tavily_api_key, 
    exclude_domains = ["istockphoto.com", "shutterstock.com", "gettyimages.com", "stock.adobe.com", "m.media-amazon.com",
                        "static.wikia.nocookie.net", "media.istockphoto.com", "alamy.com"], 
    include_domains=["unsplash.com", "images.unsplash.com", "wallpapercat.com"]
), TavilyExtract(
    extract_depth="advanced", 
    api_key=tavily_api_key, 
    include_images=True
)]

app = Flask(__name__)
design = DesignThinkingAgent(model, tools)
viability = ProductViabilityAgent(model, tools)
business = BusinessModelAgent(model, tools)
swe = SWESystemAgent(model, tools)
verifier = SWEVerifierAgent(model, tools)
feedback = CustomerFeedbackAgent(model, tools)

@app.route('/design_input', methods=['POST'])
def run_agent():
    #resetting all the agents' last message
    design.last_message = ""
    viability.last_message = ""
    swe.last_message = "" 
    feedback.last_message = ""
    data = request.json
    query = data['query']
    print("query: " + query)
    result = design.run(query) 
    result = design.cleanJsonContent(result['messages'][-1].content) #getting the last message and formatting that output
    print(result)
    response = {"message": "Query received", "result": result}
    return jsonify(response), 200

@app.route('/update_persona', methods=['POST'])
def update_customer_info():
    data = request.json
    customer = data['customer']
    # if design.last_message == "": #THIS IS FOR TESTING PURPOSES if the design last message is empty - which it shouldnt be if you started from the beginning
    #     design.last_message = "{'customer_persona': [{'name': 'Flora, the Budding Biologist', 'demographics': {'age': 16, 'gender': 'Female', 'occupation': 'High School Student'}, 'description': 'Flora is a bright and curious high school student with a passion for biology and wildlife. She is particularly fascinated by amphibians, especially frogs, and dreams of becoming a herpetologist. She is active on social media, loves nature photography, and is always looking for opportunities to learn more about the natural world. She is also involved in her school\\'s science club and environmental awareness programs.'}], 'empathy_map': {'says': ['\"I wish I knew more about different frog species.\"', '\"It\\'s hard to find reliable information about frog care.\"', '\"I want to share my love for frogs with others.\"', '\"Are there any frogs local to my area?\"'], 'thinks': ['\"Frogs are so interesting, but often misunderstood.\"', '\"I wonder what the best way to protect frog habitats is.\"', '\"I hope I can make a difference in frog conservation.\"', '\"I need a good source of information to learn about frogs.\"'], 'does': ['Reads articles and books about frogs.', 'Watches documentaries about amphibians.', 'Visits local ponds and wetlands to observe frogs.', 'Participates in citizen science projects related to frog monitoring.', 'Shares frog photos and facts on social media.'], 'feels': ['Excited about discovering new frog species.', 'Frustrated by the lack of accessible information about frogs.', 'Concerned about the threats to frog populations.', 'Inspired to take action to protect frogs and their habitats.']}, 'customer_journey_map': {'awareness': 'Sees an ad for the frog app on social media or a science blog.', 'comparison': 'Compares the app to other nature apps and online resources about frogs, looking at features, reviews, and price (if applicable).', 'purchase': 'Downloads the app because it offers a comprehensive database of frog species, interactive identification tools, and community features for sharing observations.', 'installation': \"Easily downloads and installs the app, creates a profile, and starts exploring frog species and local frog sightings. Finds the app intuitive and engaging.\"}, 'problem_statement': 'Young biology enthusiasts lack a centralized, engaging, and reliable mobile resource for learning about frog species, identification, conservation, and community engagement.'}"
    info = json5.loads(design.last_message)
    info["customer_persona"][0] = customer #changing the customer persona field
    design.last_message = json.dumps(info) #reassigning the last message to the data with the updated customer persona
    result = design.last_message
    # print("updated message: ")
    # print(design.last_message)
    response = {"message": "Update received", "result": result}
    return jsonify(response), 200

@app.route('/viability', methods=['GET'])
def get_viability_data():
    data = json5.loads(design.last_message) #getting the last message from the design thinking agent
    print("problem statement: " + data["problem_statement"])
    if (viability.last_message == ""):
        viability_result = viability.run(data["problem_statement"]) #run the viability agent on the problem statement
        viability_result = viability.cleanJsonContent(viability_result['messages'][-1].content) #getting cleaned content
    else:
        print("API not called, previous PRD loaded")
        viability_result = viability.last_message
    # print(viability_result)

    #business agent call
    if business.last_message == "":
        business_result = business.run(data["problem_statement"])  # Generate Business Model Canvas
        business_result = business.cleanJsonContent(business_result['messages'][-1].content)  # Clean and return
    else:
        print("API not called, previous Business Model loaded")
        business_result = business.last_message
    print(business_result)
    response = {
        "message": "Success",
        "viability_result": viability_result,
        "business_result": business_result
    }
    return jsonify(response), 200

@app.route('/design_backtracking', methods=['GET'])
def get_design_output(): #can be any name you want, wont use this name again
    # print("in design backtracking")
    result = design.last_message
    response = ""
    if result == "": #TESTING PURPOSES ONLY
        # result = "{'customer_persona': [{'name': 'Flora, the Budding Biologist', 'demographics': {'age': 16, 'gender': 'Female', 'occupation': 'High School Student'}, 'description': 'Flora is a bright and curious high school student with a passion for biology and wildlife. She is particularly fascinated by amphibians, especially frogs, and dreams of becoming a herpetologist. She is active on social media, loves nature photography, and is always looking for opportunities to learn more about the natural world. She is also involved in her school\\'s science club and environmental awareness programs.'}], 'empathy_map': {'says': ['\"I wish I knew more about different frog species.\"', '\"It\\'s hard to find reliable information about frog care.\"', '\"I want to share my love for frogs with others.\"', '\"Are there any frogs local to my area?\"'], 'thinks': ['\"Frogs are so interesting, but often misunderstood.\"', '\"I wonder what the best way to protect frog habitats is.\"', '\"I hope I can make a difference in frog conservation.\"', '\"I need a good source of information to learn about frogs.\"'], 'does': ['Reads articles and books about frogs.', 'Watches documentaries about amphibians.', 'Visits local ponds and wetlands to observe frogs.', 'Participates in citizen science projects related to frog monitoring.', 'Shares frog photos and facts on social media.'], 'feels': ['Excited about discovering new frog species.', 'Frustrated by the lack of accessible information about frogs.', 'Concerned about the threats to frog populations.', 'Inspired to take action to protect frogs and their habitats.']}, 'customer_journey_map': {'awareness': 'Sees an ad for the frog app on social media or a science blog.', 'comparison': 'Compares the app to other nature apps and online resources about frogs, looking at features, reviews, and price (if applicable).', 'purchase': 'Downloads the app because it offers a comprehensive database of frog species, interactive identification tools, and community features for sharing observations.', 'installation': \"Easily downloads and installs the app, creates a profile, and starts exploring frog species and local frog sightings. Finds the app intuitive and engaging.\"}, 'problem_statement': 'Young biology enthusiasts lack a centralized, engaging, and reliable mobile resource for learning about frog species, identification, conservation, and community engagement.'}"
        response = {"message": "Error, design agent has no last message data saved, loading dummy data", "result": result} 
    else:
        response = {"message": "Success", "result": result}
    # print(response)
    return jsonify(response), 200

# we didnt ever use this i dont think 
@app.route('/ideation_backtracking', methods=['GET'])
def get_product_idea(): 
    print("in product ideation backtracking")
    result = design.product_idea
    print("product idea: " + result)
    response = {"message": "Success", "result": result}
    return jsonify(response), 200

@app.route('/swe_model', methods=['POST'])
def swe_model_endpoint():
    data = request.json
    # Process the data from the frontend
    button_name = data.get('buttonName', '')
    
    response = {
        "status": "success",
        "message": f"Received data for button: {button_name}",
        "data": data
    }
    return jsonify(response), 200

@app.route('/generate_mvp', methods=['GET'])
def generate_mvp():
    # Endpoint to generate the MVP code based on PRD
    try:
        data = json5.loads(viability.last_message)
    
        if (swe.last_message == ""):
            result = swe.run(json.dumps(data))
            result = result['messages'][-1].content

            verifiedCode = verifier.run(result)
            swe.last_message = verifiedCode
            result = verifiedCode
        else:
            result = swe.last_message

        cwd = os.getcwd() 
        
        # Split the result at "--- CSS DIVIDER ---"
        if "--- CSS DIVIDER ---" in result:
            tsxCode, cssCode = result.split("--- CSS DIVIDER ---", 1)
            # Strip any whitespace and ensure the divider is completely removed
            tsxCode = tsxCode.strip()
            cssCode = cssCode.strip()
        else:
            tsxCode = result
            cssCode = "@tailwind base;\n@tailwind components;\n@tailwind utilities;"
        if not cssCode.strip():
            cssCode = "@tailwind base;\n@tailwind components;\n@tailwind utilities;"
        
        # Create and write to page.tsx
        tsxFilePath = os.path.join(cwd, '..', 'app', 'generatedmvp', 'page.tsx')
        os.makedirs(os.path.dirname(tsxFilePath), exist_ok=True)
        with open(tsxFilePath, 'w') as f:
            f.write(tsxCode.strip())
            
        # Create and write to mvp.css
        cssFilePath = os.path.join(cwd, '..', 'app', 'generatedmvp', 'mvp.css')
        os.makedirs(os.path.dirname(cssFilePath), exist_ok=True)
        with open(cssFilePath, 'w') as f:
            f.write(cssCode.strip())

        response = {
            "message": "MVP TSX and CSS generated, verified, and saved as separate files.", 
            "tsx_result": tsxCode.strip(),
            "css_result": cssCode.strip()
        }
        return jsonify(response), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/generate_context_page', methods=['POST'])
def generate_context_page():
    try:
        dataFromClient = request.json
        cwd = os.getcwd()
        tsxFilePath = os.path.join(cwd, '..', 'app', 'generatedmvp', 'page.tsx')
        currentPageContent = ""
        if os.path.exists(tsxFilePath):
            try:
                with open(tsxFilePath, 'r', encoding = 'utf-8') as f:
                    currentPageContent = f.read()
                print(f"Successfully read current page content from {tsxFilePath}")
            except Exception as readError:
                print(f"Error reading {tsxFilePath}: {readError}")
                currentPageContent = f"// Error reading previous page: {readError}"
        dataForAgent = dict(dataFromClient) # Make mutable copy
        dataForAgent['currentPage'] = currentPageContent
        print("Data being passed to swe.run:", dataForAgent)
        contextResult = swe.run(dataForAgent) # Pass augmented data

        lastMessage = contextResult['messages'][-1]
        rawPageContent = lastMessage.content
        print("Raw content received from agent:", rawPageContent)
        
        verifiedCode = verifier.run(rawPageContent)
        swe.last_message = verifiedCode
        
        # Split the result at "--- CSS DIVIDER ---"
        if "--- CSS DIVIDER ---" in verifiedCode:
            tsxCode, cssCode = verifiedCode.split("--- CSS DIVIDER ---", 1)
            # Strip any whitespace and ensure the divider is completely removed
            tsxCode = tsxCode.strip()
            cssCode = cssCode.strip()
        else:
            tsxCode = verifiedCode.strip()
            cssCode = "@tailwind base;\n@tailwind components;\n@tailwind utilities;"

        cwd = os.getcwd() 
        
        # Create and write to page.tsx
        tsxFilePath = os.path.join(cwd, '..', 'app', 'generatedmvp', 'page.tsx')
        os.makedirs(os.path.dirname(tsxFilePath), exist_ok=True)
        with open(tsxFilePath, 'w') as f:
            f.write(tsxCode)
            
        # Create and write to mvp.css
        cssFilePath = os.path.join(cwd, '..', 'app', 'generatedmvp', 'mvp.css')
        os.makedirs(os.path.dirname(cssFilePath), exist_ok=True)
        with open(cssFilePath, 'w') as f:
            f.write(cssCode)

        response = {
            "message": "Context page generated, verified, and saved as separate files.", 
            "tsx_result": tsxCode,
            "css_result": cssCode
        }
        return jsonify(response), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/customer_feedback', methods=['GET'])
def get_feedback():
    result = ""
    design_data = json5.loads(design.last_message) #getting the last message from the design thinking agent
    persona = design_data["customer_persona"]
    feedback.run(str({"customer_persona": persona, "app": swe.last_message}))
    result = feedback.last_message
    print(feedback.last_message)
   
    response = {"message": "Success", "result": str(result)}
    return jsonify(response), 200

@app.route('/update_feedback', methods=['POST'])
def update_customer_feedback():
    data = request.json
    info = data['feedback']
    feedback.last_message = json.dumps(info) #reassigning the last message to the updated customer feedback
    result = feedback.last_message
    response = {"message": "Update received", "result": result}
    print(feedback.last_message)
    return jsonify(response), 200


def findFreePort():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

port = findFreePort()
os.environ["ALMANACPORT"] = str(port)

with open("flask_port.json", "w") as f:
    json.dump({"port": os.environ["ALMANACPORT"]}, f)

if __name__ == '__main__':
    print(f"Running Flask on port {port}")
    app.run(host='0.0.0.0', port = port)  # Use dynamic portasw