from flask import Flask, request, jsonify
from design_agent import DesignThinkingAgent
from viability_agent import ProductViabilityAgent
from swe_agent import SWESystemAgent
from business_model_agent import BusinessModelAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
import json5
import json
import os
import socket
import re

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

@app.route('/design_input', methods=['POST'])
def run_agent():
    #resetting all the agents' last message
    design.last_message = ""
    viability.last_message = ""
    swe.last_message = "" # UNCOMMENTED
    data = request.json
    query = data['query']
    print("query: " + query)
    result = design.run(query) 
    result = design.cleanJsonContent(result['messages'][-1].content) #getting the last message and formatting that output
    print(result)
    response = {"message": "Query received", "result": result}
    return jsonify(response), 200

@app.route('/viability', methods=['GET'])
def get_viability_data():
    #just for testing purposes
    # design.last_message = """{"customer_persona":[{"name":"Professor Annelise","demographics":{"age":45,"gender":"Female","occupation":"Biology Professor"},"description":"Annelise is a dedicated biology professor with a passion for herpetology, seeking engaging and reliable resources for her classes and research, valuing accuracy, up-to-date information, and user-friendly interfaces."}],"empathy_map":{"says":["I need a reliable source of information on frog species.","My students need engaging learning materials.","It's difficult to find all the information I need in one place."],"thinks":["This web app could save me a lot of time.","I hope the information is accurate and up-to-date.","Will this app be engaging enough for my students?"],"does":["Searches online for frog information.","Looks through textbooks and journals.","Prepares lectures and assignments using various resources."],"feels":["Frustrated by the lack of a comprehensive resource.","Overwhelmed by the amount of information to sift through.","Excited about the potential of a user-friendly web app."]},"customer_journey_map":{"awareness":"Annelise hears about the web app from a colleague at a conference.","comparison":"She compares the web app to other online resources, checking for accuracy, comprehensiveness, and user-friendliness.","purchase":"She decides to use the web app for its comprehensive information and engaging features, free of charge.","installation":"She easily accesses the web app through her browser and finds the interface intuitive and easy to navigate."},"problem_statement":"Biology professors and students lack a comprehensive, accurate, and engaging online resource for learning about frog species, leading to frustration, time wasted on searching multiple sources, and a suboptimal learning experience."}"""
    data = json5.loads(design.last_message) #getting the last message from the design thinking agent
    print("problem statement: " + data["problem_statement"])
    if (viability.last_message == ""):
        viability_result = viability.run(data["problem_statement"]) #run the viability agent on the problem statement
        viability_result = viability.cleanJsonContent(viability_result['messages'][-1].content) #getting cleaned content
    else:
        print("API not called, previous PRD loaded")
        viability_result = viability.last_message
    #just for testing purposes
    # viability_result = """{"introduction":["This product is a web application designed to provide biology professors and students with a comprehensive, accurate, and engaging online resource for learning about frog species. It addresses the current lack of a centralized, reliable source of information, saving users time and enhancing the learning experience."],"goals":["To create a one-stop online resource for all things related to frog species.","To provide accurate, up-to-date, and reliable information for both educational and research purposes.","To offer an engaging and user-friendly interface that caters to both professors and students.","To improve the efficiency of information gathering for biology educators and students.","To enhance the learning and research experience related to herpetology."],"target_audience":["Biology professors teaching courses related to herpetology or ecology.","University students studying biology, zoology, or related fields.","Researchers conducting studies on frog species.","Anyone with a general interest in learning about frog species."],"product_features":["A comprehensive database of frog species information, including taxonomy, morphology, habitat, behavior, and conservation status.","High-quality images and videos of various frog species.","Interactive maps showing the geographic distribution of different frog species.","Engaging learning modules and quizzes to enhance knowledge retention.","A search function to easily find specific information.","Downloadable resources such as fact sheets and presentations.","A user-friendly interface accessible on various devices."],"functional_requirements":["The application should allow users to search for information on specific frog species using keywords or scientific names.","The application should display detailed information about each frog species, including images, videos, and geographic distribution maps.","The application should provide interactive learning modules and quizzes.","The application should allow users to download resources such as fact sheets and presentations.","The application should be responsive and accessible across different devices and browsers.","The application should be integrated with a reliable and up-to-date source of information on frog species."],"nonfunctional_requirements":["The application should be user-friendly and intuitive.","The information presented should be accurate, reliable, and up-to-date.","The application should be accessible to users with disabilities.","The application should be secure and protect user data.","The application should be scalable to handle a large number of users and data.","The application should be performant and load quickly."]}"""
    print(viability_result)

    ##business agent call
    if business.last_message == "":
        business_result = business.run(data["problem_statement"])  # Generate Business Model Canvas
        business_result = business.cleanJsonContent(business_result['messages'][-1].content)  # Clean and return
    else:
        print("API not called, previous Business Model loaded")
        business_result = business.last_message

    response = {
        "message": "Success",
        "viability_result": viability_result,
        "business_result": business_result
    }
    return jsonify(response), 200

@app.route('/design_backtracking', methods=['GET'])
def get_design_output(): #can be any name you want, wont use this name again
    print("in design backtracking")
    result = design.last_message
    response = ""
    if result == "":
        response = {"message": "Error, design agent has no last message data saved"}
    else:
        response = {"message": "Success", "result": result}
    print(response)
    return jsonify(response), 200

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
    data = json5.loads(viability.last_message)
    
    if (swe.last_message == ""):
        result = swe.run(json.dumps(data))
        result = result['messages'][-1].content
        swe.last_message = result

        cleanedResult = re.sub(r'`(?:jsx|css|javascript)?\n?', '', result) # Remove `jsx, `css, `javascript, and ``` (with optional newline after)
        cleanedResult = re.sub(r'`', '', cleanedResult) # Remove any remaining `
        # cleanedResult = re.sub(r'//.*', '', cleanedResult) # Remove single-line JavaScript comments (// ...)
        cleanedResult = cleanedResult.strip() # Trim whitespace

        swe.last_message = cleanedResult
        result = cleanedResult
    else:
        result = swe.last_message
        
    response = {"message": "MVP generated successfully", "result": result}
    print(response)
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