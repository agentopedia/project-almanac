import os

from agent import Agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI

class SWESystemAgent(Agent):

    def __init__(self, model, tools):
        self.prd_content = ""
        prompt = f"""Imagine you are a front-end engineer expert in bootstrap. Generate bootstrap html code based on the requirements outlined in the prd:{self.prd_content}. 

        The multi-page web application should include all the different CUJs that are possible.  The primary objective is to make sure that clicking any button on the home page as part of the CUJ redirects the user to the /model endpoint. You also need to generate hidden input elements with the name 'button_name' in every form to capture the names of the buttons in the form. These names will also be sent to the /model end point when the user clicks on the buttons.
        Constraints:
        1.Do not generate a description of the code
        2.Do not generate html codeticks
        3.Ensure that all the buttons in the page are making a call to the route named '/model'. Clicking on this button should pass the arguments as input to the route. 
        4.Do not add javascript code to handle form submission to the /model end point. It should be handled directly by the generated html form element, so that request comes directly to the Flask route without involvement from Javascript. 
        5.Do not output the plan or the PRD
        6.Ensure that the html page provides a gateway to multiple pathways that users can explore. The landing page should open up a great deal of possibilities that the users can explore - their user experience should be enhanced by the use of the html page. Design the HTML landing page to function as a central hub, where users can easily navigate to different sections such as tutorials, product features, and support resources. The page should offer clear pathways with intuitive design elements, encouraging users to explore various options, thereby enhancing their overall experience 
        7.Never use placeholder texts as examples. Always approximate the real-world scenarios as examples based on the context of the webpage.
        8. Do not generate images. If needed generate ascii art that approximate the images

        Let's assume the description is for a contact form with fields for name, email, and message, along with a submit button that makes a call to the /model route. Here is the code:

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Contact Form</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container">
                <h2 class="mt-5">Contact Us</h2>
                <form action="/model" method="POST" id="contactForm">
                    <div class="form-group">
                        <label for="name">Name</label>
                        <input type="text" class="form-control" id="name" name="name" placeholder="Enter your name" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" class="form-control" id="email" name="email" placeholder="Enter your email" required>
                    </div>
                    <div class="form-group">
                        <label for="message">Message</label>
                        <textarea class="form-control" id="message" name="message" rows="4" placeholder="Enter your message" required></textarea>
                    </div>
                    <input type="hidden" name="button_name" value="Submit Feedback">
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>

            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </body>
        </html>
        Explanation:
        HTML Structure: The HTML document starts with the <!DOCTYPE html> declaration and includes the necessary metadata, such as the character set and viewport settings.
        Bootstrap Integration: Bootstrap CSS and JS are integrated using the CDN links.
        Form Structure: The form contains three input fields for name, email, and message. Each field is wrapped in a div with the class form-group to apply Bootstrap styling.
        Submit Button: The submit button is created with the class btn btn-primary to apply Bootstrap button styling. The form tag has an action attribute set to /model, and the method is set to POST. It will also send the hidden input field that contains the button name.
        JavaScript Integration: Bootstrap's JavaScript dependencies are included at the end of the body for better page load performance.
        Example for LLM to generate similar code:
        To ensure the LLM generates the correct code for buttons, here are a few additional examples with different form fields and buttons making calls to the /model route.

        Do not generate login form code.

        Example 3: Feedback Form
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Feedback Form</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container">
                <h2 class="mt-5">Feedback</h2>
                <form action="/model" method="POST" id="feedbackForm">
                    <div class="form-group">
                        <label for="fullname">Full Name</label>
                        <input type="text" class="form-control" id="fullname" name="fullname" placeholder="Enter your full name" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" class="form-control" id="email" name="email" placeholder="Enter your email" required>
                    </div>
                    <div class="form-group">
                        <label for="feedback">Feedback</label>
                        <textarea class="form-control" id="feedback" name="feedback" rows="4" placeholder="Enter your feedback" required></textarea>
                    </div>
                    <input type="hidden" name="button_name" value="Submit Feedback">
                    <button type="submit" class="btn btn-primary">Submit Feedback</button>
                </form>
            </div>

            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </body>
        </html>
        Example 4: Survey Form
        html
        Copy code
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Survey Form</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container">
                <h2 class="mt-5">Survey</h2>
                <form action="/model" method="POST" id="surveyForm">
                    <div class="form-group">
                        <label for="age">Age</label>
                        <input type="number" class="form-control" id="age" name="age" placeholder="Enter your age" required>
                    </div>
                    <div class="form-group">
                        <label for="gender">Gender</label>
                        <select class="form-control" id="gender" name="gender" required>
                            <option value="">Select your gender</option>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="rating">Rate our service</label>
                        <select class="form-control" id="rating" name="rating" required>
                            <option value="">Select rating</option>
                            <option value="1">1 - Poor</option>
                            <option value="2">2 - Fair</option>
                            <option value="3">3 - Good</option>
                            <option value="4">4 - Very Good</option>
                            <option value="5">5 - Excellent</option>
                        </select>
                    </div>
                    <input type="hidden" name="button_name" value="Submit Survey">
                    <button type="submit" class="btn btn-primary">Submit Survey</button>
                </form>
            </div>

            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </body>
        </html>
        Example 5: Appointment Booking Form
        html
        Copy code
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Appointment Booking</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container">
                <h2 class="mt-5">Book an Appointment</h2>
                <form action="/model" method="POST" id="appointmentForm">
                    <div class="form-group">
                        <label for="fullname">Full Name</label>
                        <input type="text" class="form-control" id="fullname" name="fullname" placeholder="Enter your full name" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" class="form-control" id="email" name="email" placeholder="Enter your email" required>
                    </div>
                    <div class="form-group">
                        <label for="date">Preferred Date</label>
                        <input type="date" class="form-control" id="date" name="date" required>
                    </div>
                    <div class="form-group">
                        <label for="time">Preferred Time</label>
                        <input type="time" class="form-control" id="time" name="time" required>
                    </div>
                    <input type="hidden" name="button_name" value="Book Appointment">
                    <button type="submit" class="btn btn-primary">Book Appointment</button>
                </form>
            </div>

            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </body>
        </html>

        These examples cover various types of forms, each designed to capture different types of user input and make POST requests to the /model route. This should provide a clear template for generating similar Bootstrap forms for other use cases.

        Augment the final generated html code with the below guidelines:

        Here are the instructions for generating the html code:

        Design a dynamic, responsive web application using Bootstrap that incorporates a variety of layouts, components, and design patterns available in the framework. Do not use the default blue color to render the buttons. Use different colors based on the theme of the application that is getting built. This application should:

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
        """
        super().__init__(model, tools, prompt)

    def run(self, inputData):
        self.prd_content = inputData
        result = super().run(inputData)
        return result
    
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