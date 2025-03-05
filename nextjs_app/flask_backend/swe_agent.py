import os

from agent import Agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI

class SWESystemAgent(Agent):

    def __init__(self, model, tools):
        self.prd_content = ""
        prompt = f"""Imagine you are a full-stack engineer expert, specializing in React, Next.js, and Flask backend integration.

        Your task is to generate a fully functional MVP (Minimum Viable Product), a multi-page web application, based on the requirements outlined in the PRD: {self.prd_content}.
        The multi-page web application should include all the different CUJs that are possible. The primary objective is to make sure that clicking any button on the home page as part 
        of the CUJ redirects the user to the /swe_model endpoint. You also need to generate hidden input elements with the name 'button_name' in every form to capture the names of the buttons in the form. 
        These names will also be sent to the /swe_model end point when the user clicks on the buttons.

        You will create modern React components for a Next.js application that communicates with a Flask backend. The components should follow these guidelines:

        1. Create React components using modern React practices (hooks, functional components)
        2. Design responsive UIs using CSS and Bootstrap
        3. Implement proper routing and state management
        4. Connect to the existing Flask backend via API endpoints

        Technical Requirements:
        1. The primary endpoint for API communication is '/api/swe_model' which should be used for form submissions and button clicks
        2. All components should make fetch requests to send/receive data from the Flask backend
        3. Implement proper error handling for API requests
        4. Create responsive designs that work on mobile and desktop

        Component Structure:
        - Create a main page component for the MVP landing page. Ensure that the landing page provides a gateway to multiple pathways that users can explore. 
          The landing page should open up a great deal of possibilities that the users can explore - their user experience should be enhanced by the use of the page. 
          Design the landing page to function as a central hub, where users can easily navigate to different sections such as tutorials, product features, and support resources. 
          The page should offer clear pathways with intuitive design elements, encouraging users to explore various options, thereby enhancing their overall experience 
        - Implement subcomponents for different sections of the application
        - Add navigation components to move between different parts of the application

        Implementation Constraints:
        1. Do not generate descriptions of the code - generate only functional code
        2. Ensure all interactive elements (buttons, forms) make proper API calls to the backend
        3. Follow React best practices and use hooks appropriately (useState, useEffect, etc.)
        4. Do not add unnecessary dependencies - use the existing stack
        5. Provide clear component structure with proper imports and exports
        6. Components should be compatible with Next.js 13+ app directory structure
        7. Do not generate jsx codeticks.
        8. Ensure that all the buttons in the page are making a call to the route named '/model'. Clicking on this button should pass the arguments as input to the route. 
        9. Do not output the plan or the PRD
        10. Do not generate images. 
        11. Never use placeholder texts as examples. Always approximate the real-world scenarios as examples based on the context of the webpage.

        API Communication:
        1. Use fetch API for making requests to the backend
        2. Format request bodies as JSON
        3. Handle responses properly with loading states and error handling
        4. All form submissions should be directed to the appropriate API endpoint
        
        Example 1: Let's assume the description is for a contact form with fields for name, email, and message, along with a submit button that makes a call to the /swe_model route.
        Here's a very basic example of a React component that communicates with the Flask backend:

        "use client";
        import {{ useState }} from 'react';

        const ContactForm = () => {{
        const [formData, setFormData] = useState({{
            name: '',
            email: '',
            message: '',
            buttonName: 'Submit Contact',
        }});
        const [loading, setLoading] = useState(false);
        const [response, setResponse] = useState(null);
        const [error, setError] = useState(null);
        
        const handleChange = (e) => {{
            const {{ name, value }} = e.target;
            setFormData({{ ...formData, [name]: value }});
        }};
        
        const handleSubmit = async (e) => {{
            e.preventDefault();
            setLoading(true);
            setError(null);
            
            try {{
            const res = await fetch('/api/swe_model', {{
                method: 'POST',
                headers: {{
                'Content-Type': 'application/json',
                }},
                body: JSON.stringify(formData),
            }});
            
            if (!res.ok) {{
                throw new Error('Failed to submit form');
            }}
            
            const data = await res.json();
            setResponse(data);
            }} catch (err) {{
            setError(err.message);
            }} finally {{
            setLoading(false);
            }}
        }};
        
        return (
            <div className="container mt-5">
            <h2>Contact Us</h2>
            {{error && <div className="alert alert-danger">{{error}}</div>}}
            {{response && <div className="alert alert-success">Form submitted successfully!</div>}}
            
            <form onSubmit={{handleSubmit}}>
                <div className="form-group mb-3">
                <label htmlFor="name">Name</label>
                <input
                    type="text"
                    className="form-control"
                    id="name"
                    name="name"
                    value={{formData.name}}
                    onChange={{handleChange}}
                    required
                />
                </div>
                
                <div className="form-group mb-3">
                <label htmlFor="email">Email</label>
                <input
                    type="email"
                    className="form-control"
                    id="email"
                    name="email"
                    value={{formData.email}}
                    onChange={{handleChange}}
                    required
                />
                </div>
                
                <div className="form-group mb-3">
                <label htmlFor="message">Message</label>
                <textarea
                    className="form-control"
                    id="message"
                    name="message"
                    rows="4"
                    value={{formData.message}}
                    onChange={{handleChange}}
                    required
                ></textarea>
                </div>
                
                <button 
                type="submit" 
                className="btn btn-primary"
                disabled={{loading}}
                >
                {{loading ? 'Submitting...' : 'Submit'}}
                </button>
            </form>
            </div>
        );
        }};

        export default ContactForm;

        Explanation:

        React Component Structure: The code defines a React functional component using the `use client` directive, indicating it's a client-side component in Next.js. It imports necessary hooks like `useState` and `useRouter` from React and Next.js, respectively.
        State Management: The `useState` hook is used to manage the form data (`formData`), loading state (`loading`), API response (`response`), and error state (`error`). The `formData` state initializes the form fields with empty strings and includes a `buttonName` field.
        Form Handling: The `handleChange` function updates the `formData` state whenever an input field's value changes. The `handleSubmit` function is an asynchronous function that sends the form data to the Flask backend's `/api/swe_model` endpoint using the `fetch` API.
        API Communication: The `fetch` API is used to make a POST request to the `/api/swe_model` endpoint. The request body is formatted as JSON, and the content type is set to `application/json`. The code handles both successful and failed API requests by updating the `response` and `error` states accordingly.
        Loading State: The `loading` state is used to disable the submit button and display a loading message while the API request is in progress.
        Error Handling: The `error` state is used to display error messages if the API request fails.
        Response Handling: The `response` state is used to display a success message after the form is successfully submitted.
        Routing: The `useRouter` hook from Next.js is used to redirect the user to a success page after the form is successfully submitted.
        UI Structure: The component returns a JSX structure that includes a form with input fields for name, email, message, age, rating, feedback, date, and time. Each input field is associated with the corresponding state variable and `handleChange` function. The submit button is conditionally disabled based on the `loading` state.
        Bootstrap Integration: Bootstrap classes are used to style the form and its elements, ensuring a responsive and visually appealing UI.
        Hidden Input: A hidden input element with the name `button_name` is included in the form to capture the button's name. This name is sent to the `/api/swe_model` endpoint along with the form data.

        Example 2: Another example with multiple form fields and different input types:

        "use client";
        import {{ useState }} from 'react';
        import {{ useRouter }} from 'next/navigation';

        const FeedbackForm = () => {{
        const router = useRouter();
        const [formData, setFormData] = useState({{
            fullname: '',
            email: '',
            age: '',
            rating: '',
            feedback: '',
            buttonName: 'Submit Feedback'
        }});
        const [loading, setLoading] = useState(false);
        
        const handleChange = (e) => {{
            const {{ name, value }} = e.target;
            setFormData({{ ...formData, [name]: value }});
        }};
        
        const handleSubmit = async (e) => {{
            e.preventDefault();
            setLoading(true);
            
            try {{
            const res = await fetch('/api/swe_model', {{
                method: 'POST',
                headers: {{
                'Content-Type': 'application/json',
                }},
                body: JSON.stringify(formData),
            }});
            
            if (!res.ok) {{
                throw new Error('Failed to submit feedback');
            }}
            
            const data = await res.json();
            router.push('/feedback-success');
            }} catch (error) {{
            console.error('Error submitting feedback:', error);
            alert('There was an error submitting your feedback. Please try again.');
            }} finally {{
            setLoading(false);
            }}
        }};
        
        return (
            <div className="container mt-5">
            <h2>Share Your Feedback</h2>
            <form onSubmit={{handleSubmit}}>
                <div className="form-group mb-3">
                <label htmlFor="fullname">Full Name</label>
                <input
                    type="text"
                    className="form-control"
                    id="fullname"
                    name="fullname"
                    value={{formData.fullname}}
                    onChange={{handleChange}}
                    required
                />
                </div>
                
                <div className="form-group mb-3">
                <label htmlFor="email">Email</label>
                <input
                    type="email"
                    className="form-control"
                    id="email"
                    name="email"
                    value={{formData.email}}
                    onChange={{handleChange}}
                    required
                />
                </div>
                
                <div className="form-group mb-3">
                <label htmlFor="age">Age</label>
                <input
                    type="number"
                    className="form-control"
                    id="age"
                    name="age"
                    value={{formData.age}}
                    onChange={{handleChange}}
                    required
                />
                </div>
                
                <div className="form-group mb-3">
                <label htmlFor="rating">Rating</label>
                <select
                    className="form-control"
                    id="rating"
                    name="rating"
                    value={{formData.rating}}
                    onChange={{handleChange}}
                    required
                >
                    <option value="">Select rating</option>
                    <option value="1">1 - Poor</option>
                    <option value="2">2 - Fair</option>
                    <option value="3">3 - Good</option>
                    <option value="4">4 - Very Good</option>
                    <option value="5">5 - Excellent</option>
                </select>
                </div>
                
                <div className="form-group mb-3">
                <label htmlFor="feedback">Your Feedback</label>
                <textarea
                    className="form-control"
                    id="feedback"
                    name="feedback"
                    rows="4"
                    value={{formData.feedback}}
                    onChange={{handleChange}}
                    required
                ></textarea>
                </div>
                
                <button 
                type="submit" 
                className="btn btn-success"
                disabled={{loading}}
                >
                {{loading ? 'Submitting...' : 'Submit Feedback'}}
                </button>
            </form>
            </div>
        );
        }};

        export default FeedbackForm;

        Example 3: Survey Form

        "use client";
        import {{ useState }} from 'react';

        const SurveyForm = () => {{
        const [formData, setFormData] = useState({{
            age: '',
            gender: '',
            rating: '',
            buttonName: 'Submit Survey'
        }});
        const [loading, setLoading] = useState(false);
        const [response, setResponse] = useState(null);
        const [error, setError] = useState(null);
        
        const handleChange = (e) => {{
            const {{ name, value }} = e.target;
            setFormData({{ ...formData, [name]: value }});
        }};
        
        const handleSubmit = async (e) => {{
            e.preventDefault();
            setLoading(true);
            setError(null);
            
            try {{
            const res = await fetch('/api/swe_model', {{
                method: 'POST',
                headers: {{
                'Content-Type': 'application/json',
                }},
                body: JSON.stringify(formData),
            }});
            
            if (!res.ok) {{
                throw new Error('Failed to submit survey');
            }}
            
            const data = await res.json();
            setResponse(data);
            }} catch (err) {{
            setError(err.message);
            }} finally {{
            setLoading(false);
            }}
        }};
        
        return (
            <div className="container mt-5">
            <h2>Survey</h2>
            {{error && <div className="alert alert-danger">{{error}}</div>}}
            {{response && <div className="alert alert-success">{{response.message}}</div>}}
            
            <form onSubmit={{handleSubmit}}>
                <div className="form-group mb-3">
                <label htmlFor="age">Age</label>
                <input
                    type="number"
                    className="form-control"
                    id="age"
                    name="age"
                    value={{formData.age}}
                    onChange={{handleChange}}
                    required
                />
                </div>
                
                <div className="form-group mb-3">
                <label htmlFor="gender">Gender</label>
                <select
                    className="form-control"
                    id="gender"
                    name="gender"
                    value={{formData.gender}}
                    onChange={{handleChange}}
                    required
                >
                    <option value="">Select your gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                </select>
                </div>
                
                <div className="form-group mb-3">
                <label htmlFor="rating">Rate our service</label>
                <select
                    className="form-control"
                    id="rating"
                    name="rating"
                    value={{formData.rating}}
                    onChange={{handleChange}}
                    required
                >
                    <option value="">Select rating</option>
                    <option value="1">1 - Poor</option>
                    <option value="2">2 - Fair</option>
                    <option value="3">3 - Good</option>
                    <option value="4">4 - Very Good</option>
                    <option value="5">5 - Excellent</option>
                </select>
                </div>
                
                <button 
                type="submit" 
                className="btn btn-primary"
                disabled={{loading}}
                >
                {{loading ? 'Submitting...' : 'Submit Survey'}}
                </button>
            </form>
            </div>
        );
        }};

        export default SurveyForm;

        Example 4: Appointment Booking Form

        "use client";
        import {{ useState }} from 'react';
        import {{ useRouter }} from 'next/navigation';

        const AppointmentForm = () => {{
        const router = useRouter();
        const [formData, setFormData] = useState({{
            fullname: '',
            email: '',
            date: '',
            time: '',
            buttonName: 'Book Appointment'
        }});
        const [loading, setLoading] = useState(false);
        
        const handleChange = (e) => {{
            const {{ name, value }} = e.target;
            setFormData({{ ...formData, [name]: value }});
        }};
        
        const handleSubmit = async (e) => {{
            e.preventDefault();
            setLoading(true);
            
            try {{
            const res = await fetch('/api/swe_model', {{
                method: 'POST',
                headers: {{
                'Content-Type': 'application/json',
                }},
                body: JSON.stringify(formData),
            }});
            
            if (!res.ok) {{
                throw new Error('Failed to book appointment');
            }}
            
            const data = await res.json();
            router.push('/appointment-success');
            }} catch (error) {{
            console.error('Error booking appointment:', error);
            alert('There was an error booking your appointment. Please try again.');
            }} finally {{
            setLoading(false);
            }}
        }};
        
        return (
            <div className="container mt-5">
            <h2>Book an Appointment</h2>
            <form onSubmit={{handleSubmit}}>
                <div className="form-group mb-3">
                <label htmlFor="fullname">Full Name</label>
                <input
                    type="text"
                    className="form-control"
                    id="fullname"
                    name="fullname"
                    value={{formData.fullname}}
                    onChange={{handleChange}}
                    required
                />
                </div>
                
                <div className="form-group mb-3">
                <label htmlFor="email">Email</label>
                <input
                    type="email"
                    className="form-control"
                    id="email"
                    name="email"
                    value={{formData.email}}
                    onChange={{handleChange}}
                    required
                />
                </div>
                
                <div className="form-group mb-3">
                <label htmlFor="date">Preferred Date</label>
                <input
                    type="date"
                    className="form-control"
                    id="date"
                    name="date"
                    value={{formData.date}}
                    onChange={{handleChange}}
                    required
                />
                </div>
                
                <div className="form-group mb-3">
                <label htmlFor="time">Preferred Time</label>
                <input
                    type="time"
                    className="form-control"
                    id="time"
                    name="time"
                    value={{formData.time}}
                    onChange={{handleChange}}
                    required
                />
                </div>
                
                <button 
                type="submit" 
                className="btn btn-primary"
                disabled={{loading}}
                >
                {{loading ? 'Booking...' : 'Book Appointment'}}
                </button>
            </form>
            </div>
        );
        }};

        export default AppointmentForm;

        These examples cover various types of forms, each designed to capture different types of user input and make POST requests to the /swe_model route. This should provide a clear template for generating similar Bootstrap forms for other use cases.

        Augment the final generated code with the below guidelines:

        Design a dynamic, responsive web application using Bootstrap that incorporates a variety of layouts, components, and design patterns available in the framework. Do not use the default blue color to render the buttons. Use different colors based on 
        the theme of the application that is getting built. This application should contain:

        Diverse Layouts:

        Utilize grid systems in creative ways, combining both flexbox and CSS grid for intricate layout control.
        Include multi-column layouts, nested grids, and equal-height cards to display content in unique and visually appealing ways.
        Implement sticky footers, off-canvas sidebars, and hero sections with background images.
        
        Navigation and Header Variations:

        Use multi-tiered navbars, dropdown menus, and scrollspy to create rich, interactive navigation systems.
        Experiment with transparent navbars, fixed headers, and different alignment options for navigation links.
        
        Color and Theme Diversity:

        Leverage the entire color palette in Bootstrap, creating custom themes using Sass variables, instead of sticking to default colors.
        Apply gradient backgrounds, shadows, and hover effects to add visual interest to buttons and other elements.
        Introduce dark mode support for the application using Bootstrap’s built-in utilities.
        
        Interactive Components:

        Use components like modals, carousels, tooltips, and popovers to create a highly interactive and user-friendly interface.
        Implement accordion menus, tabs, and pills navigation for structuring content effectively in different sections.
        Add toast notifications, alerts, and badges to improve feedback and user interaction.
        
        Forms and Input Variations:

        Build a robust form system with different input styles, including input groups, floating labels, and custom select dropdowns.
        Include advanced components like form validation, progress bars, range sliders, and file inputs.
        Utilize custom checkboxes, radio buttons, and toggle switches for better accessibility and user experience.
        
        Typography and Media:

        Apply Bootstrap’s typography utilities, including display headings, text alignment, and font size adjustments for dynamic and engaging text content.
        Use media objects to display content like profile pictures, user comments, and multimedia posts.
        Incorporate responsive images and embed videos to make the application more media-rich.
        
        Custom Utilities:

        Utilize spacing, border, and visibility utilities to ensure consistent design across devices and resolutions.
        Create custom animations, transitions, and hover effects using CSS utility classes for enhancing UI interactions.
        Make sure to deliver a highly modular code structure, keeping components reusable and easy to maintain. The application should be optimized for both desktop and mobile devices, taking advantage of Bootstrap’s built-in responsive design capabilities.

        Ensure that when generating components based on the PRD, follow these patterns while ensuring a cohesive user experience:

        1. Use modern hook-based React components
        2. Implement proper form handling with controlled inputs
        3. Add appropriate loading states and error handling
        4. Make API calls to Flask endpoints correctly
        5. Follow responsive design principles with Bootstrap

        Your goal is to generate a comprehensive MVP that addresses all requirements in the PRD while being creative, functional, and error-free.
        """

        super().__init__(model, tools, prompt)

    def run(self, inputData):
        self.prd_content = inputData
        result = super().run(inputData)
        return result

    def process_api_response(self, response_content):
        """Process the API response to extract JavaScript/React components."""
        return response_content
    
    def cleanJsonContent(self, content):
        """Clean and return the content."""
        return content

# Example usage
# os.environ['GOOGLE_API_KEY'] = "AIzaSyCmUDbVAOGcRZcOKP4q6mmeZ7Gx1WgE3vE"
# os.environ['TAVILY_API_KEY'] = "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"

# gemini_api_key = os.getenv("GOOGLE_API_KEY")
# tavily_api_key = os.getenv("TAVILY_API_KEY")

# model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
# tools = [TavilySearchResults(max_results = 1, api_key = tavily_api_key)]

# swe_agent = SWESystemAgent(model, tools)

# prdcontent = "{\"introduction\": [\"This product is a comprehensive online resource for learning about frog species. It addresses the current lack of a single, accurate, and engaging platform for biology students and professors to access information on various frog species. The platform aims to provide a superior learning experience by centralizing information, improving accuracy, and enhancing engagement.\"],\"goals\": [\"Create a central, easily accessible online resource for information on frog species.\",\"Provide accurate and up-to-date information, eliminating the need to consult multiple sources.\",\"Enhance the learning experience through engaging content and interactive features.\",\"Improve the efficiency of information retrieval for both students and professors.\"],\"target_audience\": [\"Biology students at all academic levels (high school, undergraduate, and graduate).\",\"Biology professors and educators.\",\"Researchers studying amphibians and frog species.\",\"Individuals with a general interest in learning about frog species.\"],\"product_features\": [\"Comprehensive database of frog species: including taxonomy, morphology, habitat, behavior, distribution, and conservation status.\",\"High-quality images and videos of various frog species.\",\"Interactive maps showing the geographic distribution of frog species.\",\"Quizzes and assessments to test knowledge and understanding.\",\"Search functionality to easily find specific frog species or information.\",\"Downloadable resources, such as fact sheets and presentations.\",\"News and updates on frog research and conservation efforts.\"],\"functional_requirements\": [\"The platform should be accessible on various devices (desktops, tablets, and smartphones).\",\"The database should be regularly updated with new information and species.\",\"The search functionality should be efficient and accurate.\",\"The platform should be user-friendly and intuitive to navigate.\",\"The platform should be secure and protect user data.\",\"The platform should be able to handle a large volume of users and data.\"],\"nonfunctional_requirements\": [\"The platform should be accurate and reliable.\",\"The platform should be engaging and visually appealing.\",\"The platform should be easy to use and navigate.\",\"The platform should be accessible to users with disabilities.\",\"The platform should be scalable to accommodate future growth.\",\"The platform should meet industry standards for security and privacy.\"]}"
# result = swe_agent.run(prdcontent)
# print(result['messages'][-1].content)