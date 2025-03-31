from flask import Flask, request, jsonify

from design_agent import DesignThinkingAgent
from business_model_agent import BusinessModelAgent
from viability_agent import ProductViabilityAgent
from swe_agent import SWESystemAgent
from swe_verifier_agent import SWEVerifierAgent
from customer_feedback_agent import CustomerFeedbackAgent

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults

import json5
import json
import os
import socket
import re
import traceback

os.environ['GOOGLE_API_KEY'] = "AIzaSyCcN7Yo1ONOFYn5wCzPcBxTXfk7wyUFlko"
gemini_api_key = os.getenv("GOOGLE_API_KEY")

os.environ['TAVILY_API_KEY'] = "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" #set tavily api key here
tavily_api_key= os.getenv("TAVILY_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
tools = [TavilySearchResults(max_results = 1, api_key = tavily_api_key)]

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
    swe.last_message = "" # UNCOMMENTED
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
    if design.last_message == "": #THIS IS FOR TESTING PURPOSES if the design last message is empty - which it shouldnt be if you started from the beginning
        design.last_message = "{'customer_persona': [{'name': 'Flora, the Budding Biologist', 'demographics': {'age': 16, 'gender': 'Female', 'occupation': 'High School Student'}, 'description': 'Flora is a bright and curious high school student with a passion for biology and wildlife. She is particularly fascinated by amphibians, especially frogs, and dreams of becoming a herpetologist. She is active on social media, loves nature photography, and is always looking for opportunities to learn more about the natural world. She is also involved in her school\\'s science club and environmental awareness programs.'}], 'empathy_map': {'says': ['\"I wish I knew more about different frog species.\"', '\"It\\'s hard to find reliable information about frog care.\"', '\"I want to share my love for frogs with others.\"', '\"Are there any frogs local to my area?\"'], 'thinks': ['\"Frogs are so interesting, but often misunderstood.\"', '\"I wonder what the best way to protect frog habitats is.\"', '\"I hope I can make a difference in frog conservation.\"', '\"I need a good source of information to learn about frogs.\"'], 'does': ['Reads articles and books about frogs.', 'Watches documentaries about amphibians.', 'Visits local ponds and wetlands to observe frogs.', 'Participates in citizen science projects related to frog monitoring.', 'Shares frog photos and facts on social media.'], 'feels': ['Excited about discovering new frog species.', 'Frustrated by the lack of accessible information about frogs.', 'Concerned about the threats to frog populations.', 'Inspired to take action to protect frogs and their habitats.']}, 'customer_journey_map': {'awareness': 'Sees an ad for the frog app on social media or a science blog.', 'comparison': 'Compares the app to other nature apps and online resources about frogs, looking at features, reviews, and price (if applicable).', 'purchase': 'Downloads the app because it offers a comprehensive database of frog species, interactive identification tools, and community features for sharing observations.', 'installation': \"Easily downloads and installs the app, creates a profile, and starts exploring frog species and local frog sightings. Finds the app intuitive and engaging.\"}, 'problem_statement': 'Young biology enthusiasts lack a centralized, engaging, and reliable mobile resource for learning about frog species, identification, conservation, and community engagement.'}"
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
        result = "{'customer_persona': [{'name': 'Flora, the Budding Biologist', 'demographics': {'age': 16, 'gender': 'Female', 'occupation': 'High School Student'}, 'description': 'Flora is a bright and curious high school student with a passion for biology and wildlife. She is particularly fascinated by amphibians, especially frogs, and dreams of becoming a herpetologist. She is active on social media, loves nature photography, and is always looking for opportunities to learn more about the natural world. She is also involved in her school\\'s science club and environmental awareness programs.'}], 'empathy_map': {'says': ['\"I wish I knew more about different frog species.\"', '\"It\\'s hard to find reliable information about frog care.\"', '\"I want to share my love for frogs with others.\"', '\"Are there any frogs local to my area?\"'], 'thinks': ['\"Frogs are so interesting, but often misunderstood.\"', '\"I wonder what the best way to protect frog habitats is.\"', '\"I hope I can make a difference in frog conservation.\"', '\"I need a good source of information to learn about frogs.\"'], 'does': ['Reads articles and books about frogs.', 'Watches documentaries about amphibians.', 'Visits local ponds and wetlands to observe frogs.', 'Participates in citizen science projects related to frog monitoring.', 'Shares frog photos and facts on social media.'], 'feels': ['Excited about discovering new frog species.', 'Frustrated by the lack of accessible information about frogs.', 'Concerned about the threats to frog populations.', 'Inspired to take action to protect frogs and their habitats.']}, 'customer_journey_map': {'awareness': 'Sees an ad for the frog app on social media or a science blog.', 'comparison': 'Compares the app to other nature apps and online resources about frogs, looking at features, reviews, and price (if applicable).', 'purchase': 'Downloads the app because it offers a comprehensive database of frog species, interactive identification tools, and community features for sharing observations.', 'installation': \"Easily downloads and installs the app, creates a profile, and starts exploring frog species and local frog sightings. Finds the app intuitive and engaging.\"}, 'problem_statement': 'Young biology enthusiasts lack a centralized, engaging, and reliable mobile resource for learning about frog species, identification, conservation, and community engagement.'}"
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
        filePath = os.path.join(cwd, '..', 'app', 'generatedmvp', 'page.tsx')

        # Ensure the directory exists
        os.makedirs(os.path.dirname(filePath), exist_ok = True)
    
        with open(filePath, 'w') as f:
            f.write(result)

        response = {
            "message": "MVP generated, verified, and saved successfully.", 
            "result": result
        }
        return jsonify(response), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/generate_context_page', methods=['POST'])
def generate_context_page():
    try:
        data = request.json
        contextResult = swe.run(data)

        verifiedCode = verifier.run(contextResult['pageContent'])
        swe.last_message = verifiedCode
        contextResult = verifiedCode

        cwd = os.getcwd() 
        filePath = os.path.join(cwd, '..', 'app', 'generatedmvp', 'page.tsx')

        # Ensure the directory exists
        os.makedirs(os.path.dirname(filePath), exist_ok = True)
    
        with open(filePath, 'w') as f:
            f.write(contextResult)

        response = {
            "message": "Context page generated, verified, and saved successfully.", 
            "result": contextResult
        }
        return jsonify(response), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/customer_feedback', methods=['GET'])
def get_feedback():
    result = ""
    if design.last_message == "" or swe.last_message == "": #TESTING PURPOSES ONLY
        result = """{"overview": "The Cosmic Companion app is a promising start for budding biologists like Flora. It offers features like real-time sky data based on location, information on astronomical events, and personalization options. However, the app's usability, content, and appearance need improvements to make it more engaging and informative for a young user.", "usability": "The app's location detection is a great feature, but the loading times for fetching sky data should be optimized. The navigation to other sections (object database, astronomical events, SWE Agent) isn't clear and needs better visual cues. The form for personalizing the experience is functional, but it lacks immediate feedback upon saving preferences.", "content": "While the app mentions providing real-time data and a comprehensive database, there's no actual sky data displayed in the provided code (only a placeholder for JSON). The description of the astronomical events calendar is vague. The link to NASA is helpful, but the app could benefit from integrating more educational content directly.", "appearance": "The dark background with light text is readable but lacks visual appeal for a younger audience. The night sky image is generic, and the overall design feels a bit outdated. The font size is adequate, but the layout could be more dynamic and engaging.", "improvements": ["Implement actual sky data visualization (e.g., using a sky map or constellation diagrams).", "Add interactive elements to the sky data display, allowing users to click on celestial objects for more information.", "Improve the visual design with a more modern and engaging color scheme, fonts, and graphics (consider incorporating space-themed illustrations or animations).", "Provide clear navigation cues and visual feedback for button clicks and form submissions.", "Incorporate educational content directly into the app, such as short descriptions of constellations, planets, and other celestial objects.", "Optimize loading times for fetching sky data.", "Add a confirmation message or visual cue after saving personalization preferences.", "Make the 'Explore Now' button navigate to an actual object database with relevant information.", "Implement the astronomical events calendar with specific dates and details."]}"""
    else:
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
    app.run(host='0.0.0.0', port = port)  # Use dynamic port