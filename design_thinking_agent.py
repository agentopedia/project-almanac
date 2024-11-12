from agent import Agent
import json

class DesignThinkingAgent(Agent):
    jsonFormat = {
        "customer_personas": [
            {
                "name": "Persona 1",
                "demographics": {"age": 0, "gender": "", "occupation": ""},
                "description": "Brief background and lifestyle information.",
                "needs": ["Need 1", "Need 2", "Need 3"],
                "pain_points": ["Pain Point 1", "Pain Point 2", "Pain Point 3"]
            },
            {
                "name": "Persona 2",
                "demographics": {"age": 0, "gender": "", "occupation": ""},
                "description": "Brief background and lifestyle information.",
                "needs": ["Need 1", "Need 2", "Need 3"],
                "pain_points": ["Pain Point 1", "Pain Point 2", "Pain Point 3"]
            },
            {
                "name": "Persona 3",
                "demographics": {"age": 0, "gender": "", "occupation": ""},
                "description": "Brief background and lifestyle information.",
                "needs": ["Need 1", "Need 2", "Need 3"],
                "pain_points": ["Pain Point 1", "Pain Point 2", "Pain Point 3"]
            }
        ],
        "empathy_map": {
            "says": ["What the persona verbally expresses about the problem."],
            "thinks": ["What the persona is thinking internally."],
            "does": ["Actions the persona takes to address the problem."],
            "feels": ["Emotions experienced by the persona."]
        },
        "customer_journey_map": {
            "awareness": "How the persona becomes aware of the product or problem.",
            "comparison": "How the persona evaluates different options.",
            "purchase": "Factors influencing the purchase decision.",
            "installation": "Persona's experience with setting up or using the product."
        },
        "problem_statement": "A clear, concise statement that defines the issue the product is trying to solve."
    }

    prompt = f"""You are a smart researcher who must utilize design thinking to generate customer personas, create empathy maps, and expand the problem definition, given a problem statement or product description. 
    You are allowed to make multiple calls (either together or in sequence).
    Only look up information when you are sure of what you want.
    If you need to look up some information before asking a follow up question, you are allowed to do that!
    Use Tavilly to do research on the problem statement and use the information gained to create 3 customer personas that give insight into the type of users that could benefit from the specified product. 
    Describe each customer persona and list out their needs and pain points.
    Then, create an empathy map for a typical user by researching to understand the users’ emotions and challenges. An empathy map consists of what a user says, thinks, does, and feels.
    Also, create a customer journey map for a typical user. A customer journey map consists of 4 stages: awareness, comparison, purchase, and installation.
    Utilize this information gained to create a clear problem statement for the issue that the product attempts to solve.

    Give output in plaintext and in JSON, using the following JSON format:
    {json.dumps(jsonFormat, indent = 4)}
    """

    def __init__(self, model, tools):
        super().__init__(model, tools, self.prompt)
