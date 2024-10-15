import openai
import os
from dotenv import load_dotenv
from openai import OpenAI


_ = load_dotenv() #loading environment

# create a .env file that has OPENAI_API_KEY=(your key here)
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key
print(api_key)
client = OpenAI()

# testing the api key out
# response = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Hello!",
#         }
#     ],
#     model="gpt-3.5-turbo",
# )

# print(response.choices[0].message["content"])

design_profiling = """"
Imagine you are a product manager who must utilize design thinking to generate customer personas, create empathy maps, and expand the problem definition. 
Design thinking emphasizes human thinking design and focuses on the solution to the problem rather than the problem itself. 
Given a description of a product, create three customer personas to give insight into the type of users that could potentially benefit from the specified product. 
Describe each customer person and list out their needs and pain points.
Then, gather and list out the information necessary to create empathy maps for each of these users by researching to understand the users’ emotions and challenges. An empathy map consists of what a user says, thinks, does, and feels.
Also, gather and list out the information necessary to create a customer journey map. A customer journey map consists of 4 stages: awareness, comparison, purchase, and installation
Utilize this information gained to create a clear problem statement for the issue that the product attempts to solve.
"""
#could include an example of what the desired output should look like

class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute() #calling the execute method defined below to run the request
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = client.chat.completions.create(
                        model="gpt-3.5-turbo", 
                        temperature=0,
                        messages=self.messages)
        return completion.choices[0].message.content

design_agent = Agent(design_profiling)

result = design_agent("a web application that analyzes movements in modern art") #calling the agent
print(result)
