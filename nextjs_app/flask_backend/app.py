from flask import Flask, request, jsonify
from design_agent import DesignThinkingAgent

app = Flask(__name__)
design = DesignThinkingAgent()


@app.route('/design_input', methods=['POST'])
def run_agent():
    data = request.json
    query = data['query']
    print("python " + query)
    result = design.agent.run(query)['messages'][-1].content #getting the last message
    result = result.strip().strip("`").replace("json", "").strip().replace("\n", "").replace("  ", "") #formatting the output properly
    print(result)
    response = {"message": "Query received", "result": result}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

