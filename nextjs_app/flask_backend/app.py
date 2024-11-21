from flask import Flask, request, jsonify
from design_agent import DesignThinkingAgent
from viability_agent import ProductViabilityAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
import json
import os

os.environ['GOOGLE_API_KEY'] = "AIzaSyCmUDbVAOGcRZcOKP4q6mmeZ7Gx1WgE3vE"
gemini_api_key = os.getenv("GOOGLE_API_KEY")

os.environ['TAVILY_API_KEY'] = "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" #set tavily api key here
tavily_api_key= os.getenv("TAVILY_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
tools = [TavilySearchResults(max_results = 1, api_key = tavily_api_key)]

app = Flask(__name__)
design = DesignThinkingAgent(model, tools)
viability = ProductViabilityAgent(model, tools)

@app.route('/design_input', methods=['POST'])
def run_agent():
    data = request.json
    query = data['query']
    print("python " + query)
    result = design.run(query) #getting the last message
    # result = design.last_message #formatting the output properly
    result = design.cleanJsonContent(result['messages'][-1].content)
    print(result)
    response = {"message": "Query received", "result": result}
    return jsonify(response), 200

@app.route('/viability', methods=['GET'])
def get_viability_data():
    #just for testing purposes
    # design.last_message = """{"customer_persona":[{"name":"Professor Annelise","demographics":{"age":45,"gender":"Female","occupation":"Biology Professor"},"description":"Annelise is a dedicated biology professor with a passion for herpetology, seeking engaging and reliable resources for her classes and research, valuing accuracy, up-to-date information, and user-friendly interfaces."}],"empathy_map":{"says":["I need a reliable source of information on frog species.","My students need engaging learning materials.","It's difficult to find all the information I need in one place."],"thinks":["This web app could save me a lot of time.","I hope the information is accurate and up-to-date.","Will this app be engaging enough for my students?"],"does":["Searches online for frog information.","Looks through textbooks and journals.","Prepares lectures and assignments using various resources."],"feels":["Frustrated by the lack of a comprehensive resource.","Overwhelmed by the amount of information to sift through.","Excited about the potential of a user-friendly web app."]},"customer_journey_map":{"awareness":"Annelise hears about the web app from a colleague at a conference.","comparison":"She compares the web app to other online resources, checking for accuracy, comprehensiveness, and user-friendliness.","purchase":"She decides to use the web app for its comprehensive information and engaging features, free of charge.","installation":"She easily accesses the web app through her browser and finds the interface intuitive and easy to navigate."},"problem_statement":"Biology professors and students lack a comprehensive, accurate, and engaging online resource for learning about frog species, leading to frustration, time wasted on searching multiple sources, and a suboptimal learning experience."}"""
    data = json.loads(design.last_message) #getting the last message from the design thinking agent
    print(data["problem_statement"])
    result = viability.run(data["problem_statement"]) #run the viability agent on the problem statement
    result = viability.cleanJsonContent(result['messages'][-1].content) #getting cleaned content
    #just for testing purposes
    # result = """{"introduction":["This product is a web application designed to provide biology professors and students with a comprehensive, accurate, and engaging online resource for learning about frog species. It addresses the current lack of a centralized, reliable source of information, saving users time and enhancing the learning experience."],"goals":["To create a one-stop online resource for all things related to frog species.","To provide accurate, up-to-date, and reliable information for both educational and research purposes.","To offer an engaging and user-friendly interface that caters to both professors and students.","To improve the efficiency of information gathering for biology educators and students.","To enhance the learning and research experience related to herpetology."],"target_audience":["Biology professors teaching courses related to herpetology or ecology.","University students studying biology, zoology, or related fields.","Researchers conducting studies on frog species.","Anyone with a general interest in learning about frog species."],"product_features":["A comprehensive database of frog species information, including taxonomy, morphology, habitat, behavior, and conservation status.","High-quality images and videos of various frog species.","Interactive maps showing the geographic distribution of different frog species.","Engaging learning modules and quizzes to enhance knowledge retention.","A search function to easily find specific information.","Downloadable resources such as fact sheets and presentations.","A user-friendly interface accessible on various devices."],"functional_requirements":["The application should allow users to search for information on specific frog species using keywords or scientific names.","The application should display detailed information about each frog species, including images, videos, and geographic distribution maps.","The application should provide interactive learning modules and quizzes.","The application should allow users to download resources such as fact sheets and presentations.","The application should be responsive and accessible across different devices and browsers.","The application should be integrated with a reliable and up-to-date source of information on frog species."],"nonfunctional_requirements":["The application should be user-friendly and intuitive.","The information presented should be accurate, reliable, and up-to-date.","The application should be accessible to users with disabilities.","The application should be secure and protect user data.","The application should be scalable to handle a large number of users and data.","The application should be performant and load quickly."]}"""
    print(result)
    response = {"message": "Success", "data": result}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

