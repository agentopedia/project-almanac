from flask import Flask, request, jsonify
from design_agent import Agent, ChatOpenAI, TavilySearchResults, HumanMessage, tool

app = Flask(__name__)

json_format = {"customer_persona":[{"name":"Persona 1","demographics":{"age":0,"gender":"","occupation":""},"description":"Brief background and lifestyle information.","pain_points":["Pain Point 1","Pain Point 2","Pain Point 3"]}],"empathy_map":{"says":["What the persona verbally expresses about the problem."],"thinks":["What the persona is thinking internally."],"does":["Actions the persona takes to address the problem."],"feels":["Emotions experienced by the persona."]},"customer_journey_map":{"awareness":"How the persona becomes aware of the product or problem.","comparison":"How the persona evaluates different options.","purchase":"Factors influencing the purchase decision.","installation":"Persona's experience with setting up or using the product."},"problem_statement":"A clear, concise statement that defines the issue the product is trying to solve."}

prompt = f""" You are a smart researcher who must utilize design thinking to generate customer personas, given a product description. 
Use Tavilly to do research on the product description and use the information gained to create a customer persona that would benefit from the specified product. 
You are allowed to make multiple calls (either together or in sequence).
Only look up information when you are sure of what you want.
Describe the customer persona and list their pain points.
Then, create an empathy map for a this user that consists of what the user says, thinks, does, and feels.
Also, create a customer journey map for this typical user that consists of 4 stages: awareness, comparison, purchase, and installation.
Utilize the information gained to create a clear problem statement for the described product.

Give output in json, using the following json format:
{json_format}
"""

# Initialize the model and agent
model = ChatOpenAI(model="gpt-3.5-turbo")
agent = Agent(model, [tool], system=prompt)

@app.route('/design_input', methods=['POST'])
def run_agent():
    data = request.json
    query = data['query']
    print(query)
    messages = [HumanMessage(content=query)]
    # Call your agent with the provided query
    result = agent.graph.invoke({"messages": messages})

    print(result['messages'][-1].content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
