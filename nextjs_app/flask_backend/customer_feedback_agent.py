from agent import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
import json5
import os

input_format = {"customer_persona": [{"name":"","demographics":{"age":0,"gender":"","occupation":""},"description":"Brief background and lifestyle information."}],
  "app": "Implementation of the application as React code"} #if there's another css file, you should add that here

response_format = {
  "overview": "Summary of the application's feedback.",
  "usability": "Feedback about the useability and interactivity of the application.",
  "content": "Feedback about the informational value of the content presented in the app.",
  "appearance": "Feedback about the app's appearance, aesthetics, color scheme, text layout and font size, and visual media such as images and graphs.",
  "improvements": [ "List of specific and actionable improvements the customer wants to the app."]
}
class CustomerFeedbackAgent(Agent):
    #change prompt if we decide to use a css file
    prompt = f"""Imagine you are a customer for a Next.js MVP application. You will receive:  
        1. A JSON object containing the application as React code. 
        2. A JSON object containing details about the customer you are embodying.  
        The JSON objects you receive will follow the following format:
        {input_format}

        Take time to understand the customer's characteristics, thoughts, and needs. Then, review the React code and corresponding css sheet from their perspective and provide feedback on the product’s usability, content, and appearance. 
        Go in depth and be specific about the feedback needed, mentioning specific parts of the applciation that need improvements.
        Return your response as a single-line JSON object with double quotes, ensuring all fields are fully populated:
        {response_format}
        """


    #you get the feedback and then you send the feedback through an api route that goes to the software agent and has it update the original generated mvp and replace the file that its on

    def __init__(self, model, tools):
        self.product_idea = ""
        super().__init__(model, tools, self.prompt)

    def run(self, inputData):
        self.product_idea = inputData
        result = super().run(inputData)
        return result

# example usage
# os.environ['GOOGLE_API_KEY'] = "AIzaSyCmUDbVAOGcRZcOKP4q6mmeZ7Gx1WgE3vE"
# gemini_api_key = os.getenv("GOOGLE_API_KEY")
# os.environ['TAVILY_API_KEY'] = "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" #set tavily api key here
# tavily_api_key= os.getenv("TAVILY_API_KEY")

# tools = [TavilySearchResults(max_results = 1, api_key = tavily_api_key)]
# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
# customer = CustomerFeedbackAgent(model, tools)
# swe_data = """
# "use client";
# import { useState } from 'react';
# import { useRouter } from 'next/navigation';

# const LandingPage = () => {
#   return (
#     <div className="container-fluid">
#       <Header />
#       <HeroSection />
#       <FeaturesSection />
#       <LearningPathsSection />
#       <CoachDirectorySection />
#       <CommunitySection />
#       <Footer />
#     </div>
#   );
# };

# const Header = () => {
#   return (
#     <nav className="navbar navbar-expand-lg navbar-light bg-light">
#       <a className="navbar-brand" href="#">
#         Badminton Beginner's Companion
#       </a>
#       <button
#         className="navbar-toggler"
#         type="button"
#         data-toggle="collapse"
#         data-target="#navbarNav"
#         aria-controls="navbarNav"
#         aria-expanded="false"
#         aria-label="Toggle navigation"
#       >
#         <span className="navbar-toggler-icon"></span>
#       </button>
#       <div className="collapse navbar-collapse" id="navbarNav">
#         <ul className="navbar-nav ml-auto">
#           <li className="nav-item">
#             <a className="nav-link" href="#">
#               Learning Resources
#             </a>
#           </li>
#           <li className="nav-item">
#             <a className="nav-link" href="#">
#               Coach Directory
#             </a>
#           </li>
#           <li className="nav-item">
#             <a className="nav-link" href="#">
#               Learning Paths
#             </a>
#           </li>
#           <li className="nav-item">
#             <a className="nav-link" href="#">
#               Community
#             </a>
#           </li>
#           <li className="nav-item">
#             <a className="nav-link" href="#">
#               Sign Up
#             </a>
#           </li>
#           <li className="nav-item">
#             <a className="nav-link" href="#">
#               Log In
#             </a>
#           </li>
#         </ul>
#       </div>
#     </nav>
#   );
# };

# const HeroSection = () => {
#   return (
#     <div className="jumbotron text-center bg-info text-white">
#       <h1 className="display-4">Welcome to the Badminton Beginner's Companion</h1>
#       <p className="lead">Your guide to mastering badminton, one step at a time.</p>
#       <hr className="my-4" />
#       <p>
#         Explore our resources, connect with coaches, and start your badminton
#         journey today!
#       </p>
#       <a className="btn btn-primary btn-lg" href="#" role="button">
#         Get Started
#       </a>
#     </div>
#   );
# };

# const FeaturesSection = () => {
#   return (
#     <div className="container mt-5">
#       <div className="row">
#         <div className="col-md-4">
#           <div className="card">
#             <div className="card-body">
#               <h5 className="card-title">Curated Resources</h5>
#               <p className="card-text">
#                 Access a library of articles, videos, and tutorials covering basic
#                 skills, rules, and strategies.
#               </p>
#               <a href="#" className="btn btn-success">
#                 Learn More
#               </a>
#             </div>
#           </div>
#         </div>
#         <div className="col-md-4">
#           <div className="card">
#             <div className="card-body">
#               <h5 className="card-title">Coach Directory</h5>
#               <p className="card-text">
#                 Find certified badminton coaches with profiles, ratings, and
#                 contact information.
#               </p>
#               <a href="#" className="btn btn-warning">
#                 Find a Coach
#               </a>
#             </div>
#           </div>
#         </div>
#         <div className="col-md-4">
#           <div className="card">
#             <div className="card-body">
#               <h5 className="card-title">Structured Paths</h5>
#               <p className="card-text">
#                 Follow pre-defined learning paths for different skill levels with
#                 recommended resources and exercises.
#               </p>
#               <a href="#" className="btn btn-danger">
#                 Explore Paths
#               </a>
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   );
# };

# const LearningPathsSection = () => {
#   const router = useRouter();
#   const [formData, setFormData] = useState({
#     buttonName: 'Beginner Learning Path',
#   });

#   const handleButtonClick = async (buttonName: string) => {
#     setFormData({ ...formData, buttonName: buttonName });
#     try {
#       const res = await fetch('/api/swe_model', {
#         method: 'POST',
#         headers: {
#           'Content-Type': 'application/json',
#         },
#         body: JSON.stringify({ ...formData, buttonName: buttonName }),
#       });

#       if (!res.ok) {
#         throw new Error('Failed to navigate to learning path');
#       }
#       router.push('/swe_model');
#     } catch (error) {
#       console.error('Error navigating to learning path:', error);
#       alert('There was an error. Please try again.');
#     }
#   };
#   return (
#     <div className="container mt-5">
#       <h2>Learning Paths</h2>
#       <p>Choose a learning path that suits your skill level:</p>
#       <div className="list-group">
#         <button
#           type="button"
#           className="list-group-item list-group-item-action"
#           onClick={() => handleButtonClick('Beginner Learning Path')}
#         >
#           Beginner Learning Path
#         </button>
#         <button
#           type="button"
#           className="list-group-item list-group-item-action"
#           onClick={() => handleButtonClick('Intermediate Learning Path')}
#         >
#           Intermediate Learning Path
#         </button>
#         <button
#           type="button"
#           className="list-group-item list-group-item-action"
#           onClick={() => handleButtonClick('Advanced Learning Path')}
#         >
#           Advanced Learning Path
#         </button>
#       </div>
#     </div>
#   );
# };

# const CoachDirectorySection = () => {
#   const router = useRouter();
#   const [formData, setFormData] = useState({
#     buttonName: 'Find a Coach',
#   });

#   const handleButtonClick = async (buttonName: string) => {
#     setFormData({ ...formData, buttonName: buttonName });
#     try {
#       const res = await fetch('/api/swe_model', {
#         method: 'POST',
#         headers: {
#           'Content-Type': 'application/json',
#         },
#         body: JSON.stringify({ ...formData, buttonName: buttonName }),
#       });

#       if (!res.ok) {
#         throw new Error('Failed to navigate to coach directory');
#       }
#       router.push('/swe_model');
#     } catch (error) {
#       console.error('Error navigating to coach directory:', error);
#       alert('There was an error. Please try again.');
#     }
#   };
#   return (
#     <div className="container mt-5">
#       <h2>Coach Directory</h2>
#       <p>
#         Connect with experienced badminton coaches to improve your skills:
#       </p>
#       <button
#         type="button"
#         className="btn btn-primary"
#         onClick={() => handleButtonClick('Find a Coach')}
#       >
#         Find a Coach
#       </button>
#     </div>
#   );
# };

# const CommunitySection = () => {
#   const router = useRouter();
#   const [formData, setFormData] = useState({
#     buttonName: 'Join the Community',
#   });

#   const handleButtonClick = async (buttonName: string) => {
#     setFormData({ ...formData, buttonName: buttonName });
#     try {
#       const res = await fetch('/api/swe_model', {
#         method: 'POST',
#         headers: {
#           'Content-Type': 'application/json',
#         },
#         body: JSON.stringify({ ...formData, buttonName: buttonName }),
#       });

#       if (!res.ok) {
#         throw new Error('Failed to navigate to community forum');
#       }
#       router.push('/swe_model');
#     } catch (error) {
#       console.error('Error navigating to community forum:', error);
#       alert('There was an error. Please try again.');
#     }
#   };
#   return (
#     <div className="container mt-5">
#       <h2>Community Forum</h2>
#       <p>
#         Connect with other badminton beginners, ask questions, and share your
#         experiences:
#       </p>
#       <button
#         type="button"
#         className="btn btn-info text-white"
#         onClick={() => handleButtonClick('Join the Community')}
#       >
#         Join the Community
#       </button>
#     </div>
#   );
# };

# const Footer = () => {
#   return (
#     <footer className="footer mt-5 bg-dark text-white text-center py-3">
#       <div className="container">
#         <span className="text-muted">
#           Badminton Beginner's Companion &copy; 2024
#         </span>
#       </div>
#       {/* Back to SWE Agent button */}
#       <button 
#             className="btn btn-secondary mt-4" 
#             onClick={() => router.push("/swe")}
#         >
#             Back to SWE Agent
#         </button>
#     </footer>
#   );
# };

# export default LandingPage;

# customer persona: 
# [
#   {
#     "name": "Alex Chen",
#     "demographics": {
#       "age": 25,
#       "gender": "Male",
#       "occupation": "Software Engineer"
#     },
#     "description": "Alex is a tech-savvy professional who enjoys playing sports in his free time. He recently developed an interest in badminton and is looking for structured learning resources to improve his skills. Alex values efficiency and prefers well-organized guides, coaching directories, and community engagement to enhance his learning experience."
#   }
# ]"""
# design_data = "{'customer_persona': [{'name': 'Flora, the Budding Biologist', 'demographics': {'age': 16, 'gender': 'Female', 'occupation': 'High School Student'}, 'description': 'Flora is a bright and curious high school student with a passion for biology and wildlife. She is particularly fascinated by amphibians, especially frogs, and dreams of becoming a herpetologist. She is active on social media, loves nature photography, and is always looking for opportunities to learn more about the natural world. She is also involved in her school\\'s science club and environmental awareness programs.'}], 'empathy_map': {'says': ['\"I wish I knew more about different frog species.\"', '\"It\\'s hard to find reliable information about frog care.\"', '\"I want to share my love for frogs with others.\"', '\"Are there any frogs local to my area?\"'], 'thinks': ['\"Frogs are so interesting, but often misunderstood.\"', '\"I wonder what the best way to protect frog habitats is.\"', '\"I hope I can make a difference in frog conservation.\"', '\"I need a good source of information to learn about frogs.\"'], 'does': ['Reads articles and books about frogs.', 'Watches documentaries about amphibians.', 'Visits local ponds and wetlands to observe frogs.', 'Participates in citizen science projects related to frog monitoring.', 'Shares frog photos and facts on social media.'], 'feels': ['Excited about discovering new frog species.', 'Frustrated by the lack of accessible information about frogs.', 'Concerned about the threats to frog populations.', 'Inspired to take action to protect frogs and their habitats.']}, 'customer_journey_map': {'awareness': 'Sees an ad for the frog app on social media or a science blog.', 'comparison': 'Compares the app to other nature apps and online resources about frogs, looking at features, reviews, and price (if applicable).', 'purchase': 'Downloads the app because it offers a comprehensive database of frog species, interactive identification tools, and community features for sharing observations.', 'installation': \"Easily downloads and installs the app, creates a profile, and starts exploring frog species and local frog sightings. Finds the app intuitive and engaging.\"}, 'problem_statement': 'Young biology enthusiasts lack a centralized, engaging, and reliable mobile resource for learning about frog species, identification, conservation, and community engagement.'}"
# design_data = json5.loads(design_data) #getting the last message from the design thinking agent
# persona = design_data["customer_persona"]
# result = customer.run(str({"customer_persona": persona, "app": swe_data}))
# print(customer.last_message) #last message's content
# jsonify(customer.last_message)
