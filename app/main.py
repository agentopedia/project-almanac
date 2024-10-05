import os
from flask import Flask, jsonify,render_template, request, redirect, url_for, session
import requests
import json
import time
import sqlite3
import os
from flask_cors import CORS
from tavily import TavilyClient
from replit import db
#from langchain.retrievers.tavily_search_api import TavilySearchAPIRetriever
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'

import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = ''
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

os.environ["TAVILY_API_KEY"] = ""

def tavily_search(query):
    tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
# For basic search:
    results = tavily.search(query=query)
    return results
# For advanced search:
    
# Function to create a table
def add_record(table_name, record_id, description, url, html_content):
    if table_name in db:
        table = db[table_name]
        record = {
            "description": description,
            "url": url,
            "html_content": html_content
        }
        table[record_id] = record
        db[table_name] = table
        print(f"Record '{record_id}' added to table '{table_name}'.")
    else:
        print(f"Table '{table_name}' does not exist.")

# Function to retrieve a record from the table
def get_record(table_name, record_id):
    if table_name in db and record_id in db[table_name]:
        return db[table_name][record_id]
    else:
        print(f"Record '{record_id}' not found in table '{table_name}'.")

# Function to update a record in the table
def update_record(table_name, record_id, description=None, url=None, html_content=None):
    if table_name in db and record_id in db[table_name]:
        table = db[table_name]
        record = table[record_id]
        if description:
            record["description"] = description
        if url:
            record["url"] = url
        if html_content:
            record["html_content"] = html_content
        table[record_id] = record
        db[table_name] = table
        print(f"Record '{record_id}' in table '{table_name}' updated successfully.")
    else:
        print(f"Record '{record_id}' not found in table '{table_name}'.")


# Optional, add tracing in LangSmith
import string
os.environ["LANGCHAIN_API_KEY"] = "ls__92a67c6930624f93aa427f1c1ad3f59b"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "almanac"
generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

system_instruction = "You are a full stack developer who is going to help build real-world LLM-first applications. You will be given a user's request and you will generate a full stack application that meets the user's needs."


model_gen = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
      generation_config=generation_config,
      system_instruction=system_instruction,
      safety_settings=safety_settings)

def model_response(text):
   response = model_gen.generate_content(text)
   return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_almanac():
    if request.method == 'POST':
        name = request.form['name']
        session['name'] = name
        
        description = request.form['description']
        
        session['description'] = description
        session['url'] = "https://agentville-almanac.replit.app/almanac/"+name
        return redirect(url_for('almanac', name=name))
        #new_artifact = Artifact(name=name, description=description)
    return render_template('add_almanac.html')
@app.route('/update', methods=['GET', 'POST'])
def update_almanac():
    url = session['url']
    description = session['description']
    html_code = session['html_code']
    name = session['name']
    prd = model_response(f'''You are an expert in generating PRDs with CUJs by analyzing a website. Given the below details, generate a prd for the website outlining all the CUJs served by it. The Prd content should be rendered in markdown syntax in a html page.:
    Name of the app: {name}
    Description: {description}
    HTML code of the website: {html_code}
    
    Output:
    PRD''')
    print ("PRD", prd)
    prd_final = remove_html_and_backticks(prd)
    return render_template('almanac_update.html', almanac=name, url = url, prd=prd_final)

@app.route('/new_almanac',methods=['GET','POST'])
def new_almanac():
    if request.method == 'POST':
        new_desc = request.form['new_requirements']
        print ("New description",new_desc)
        
        content = model_response(f'''Imagine you are a front-end engineer expert in bootstrap. Generate bootstrap html code based on the description:{new_desc}. Use the context from search results pertaining to the description for populating the landing page. 

        Come up with a PRD to build a multi-page web application that includes all the different CUJs that are possible.  The primary objective is to make sure that clicking any button on the home page as part of the CUJ redirects the user to the /model endpoint.
        Constraints:
        1.Do not generate a description of the code
        2.Do not generate html codeticks
        3.Ensure that all the buttons in the page are making a call to the route named '/model'. Clicking on this button should pass the arguments as input to the route. 
        4.Do not add javascript code to handle form submission to the /model end point. It should be handled directly by the generated html form element, so that request comes directly to the Flask route without involvement from Javascript. 
        5.Do not output the plan or the PRD

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
        Submit Button: The submit button is created with the class btn btn-primary to apply Bootstrap button styling. The form tag has an action attribute set to /model, and the method is set to POST.
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
            <button type="submit" class="btn btn-primary">Book Appointment</button>
        </form>
        </div>

        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </body>
        </html>
        These examples cover various types of forms, each designed to capture different types of user input and make POST requests to the /model route. This should provide a clear template for generating similar Bootstrap forms for other use cases.


        ''')
        content_final = remove_html_and_backticks(content)
        session['html_code'] = content_final
        url = session['url']
        name = session['name']
        #add_record("almanac",name,description,session['url'],content_final)
        print (content_final)
        update_record("almanac", name, description=new_desc, url=url, html_content=session['html_code'])
        return render_template('almanac_app.html',name=content_final,almanac=name,url=url)
        
@app.route('/almanac/<name>')
def almanac(name):
    #artifact = Artifact.query.filter_by(name=name).first_or_404()
    record = get_record("almanac", name)
    if record:
        print ("Inside the if block")
        print (record)
        description = record.get("description")
        url = record.get("url")
        session['url'] = url
        session['description'] = description
        content_final = record.get("html_content")
        session['html_code'] = content_final
        session['name'] = name
    else:
        description = session['description']
        session['name'] = name
        url = session['url']
        
            #search_content = generate_search(description)
            
        
           # search_content = model_response(f'''Imagine you are a search engine capable of extracting relevant content from your knowledge base based on the topics mentioned in the description: {description}. This extracted content will then be used to build a web application.''')
        search_content = '''Imagine yourself to be a search engine capable of extracting relevant content from your knowledgebase based on the topics mentioned in the description: {description}. This extracted content will then be used to build a web application '''
        content = model_response(f'''Imagine you are a front-end engineer expert in bootstrap. Generate bootstrap html code based on the description:{description}. Use the context from search results: {search_content} pertaining to the description for populating the landing page. 

Come up with a PRD to build a multi-page web application that includes all the different CUJs that are possible.  The primary objective is to make sure that clicking any button on the home page as part of the CUJ redirects the user to the /model endpoint. You also need to generate hidden input elements with the name 'button_name' in every form to capture the names of the buttons in the form. These names will also be sent to the /model end point when the user clicks on the buttons.
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

''')
        content_final = remove_html_and_backticks(content)
        session['html_code'] = content_final
        add_record("almanac",name,description,session['url'],content_final)
    return render_template('almanac_app.html',name=content_final,almanac=name,url=url)

def generate_search(description):
    search_queries = model_response(f'''Given the description: {description} for a web application, generate a search query that would retrieve the relevant content. 
    Output:
    query''')
    search_results = tavily_search(search_queries)
    print ("Search results",search_results)
    return search_results

@app.route('/model', methods=['POST','GET'])
def model():
    inputs = {}
    form_data = ''
    query_data = ''
    if request.method == 'POST':
        # Retrieve form data from POST request
        form_data = request.form
        inputs = {key: form_data[key] for key in form_data.keys()}
    elif request.method == 'GET':
        # Retrieve query parameters from GET request
        query_data = request.args
        inputs = {key: query_data[key] for key in query_data.keys()}

    # Print the inputs (for demonstration purposes)
    print("Received inputs:")
    for key, value in inputs.items():
        print(f"{key}: {value}")

    # You can process the inputs here as needed

   


    html_code = session['html_code']
    problem = session['description']
    input_problem = model_response(f'''Imagine you are an expert in generating Bootstrap HTML code. User has clicked a button and submitted input to you. Analyze why the user clicked on this button and estimate the output he might be expecting. Your job is to process the input as a large language model and generate the html code that contains the output.  You are supposed to just generate the html code - nothing else. Do not generate explanations of the code. Here are the steps to follow along with sample query and answers. The generated html code should also contain buttons that will help the user interact with the generated content.

    Avoid using placeholder text like 'here is the sample question.' Instead, make realistic assumptions about real-world scenarios and provide genuine queries as examples.
    
    Step 1: Extract Input Data:

    Parse the input data: {form_data} {query_data} to retrieve the input values submitted by the user.
    Parse the html code: {html_code} to identify the button clicked by the user and determine its intended action based on the overall problem: {problem}.button_name contains the name of the button clicked by the user.
    Step 2: Identify Button Intention:

    From the parsed html_code, locate the specific button clicked by matching it with the data or event that triggered the submission.
    Determine the action or purpose associated with the clicked button (e.g., form submission, data retrieval, etc.).
    Step 3: Generate the query in the form of a question which would be input to a large language model. The question should contain the form_data and query_data included.Do not generate code.
    Step 4: Based on the query, come up with an answer
    Step 5: Based on the query and the answer, regenerate the html page which would be seen as a logical next screen to the page from which the user submitted the input: {html_code}
 Step 6: 
All buttons and hyperlinks on the page should redirect to the /model endpoint, which opens the page in a new tab with the user's intention passed as input.
Step 7:
Never use placeholder texts as examples. Always approximate the real-world scenarios as examples based on the context of the webpage.

Constraint: As much as possible, ensure that the content user is requesting is available on the webpage. Do not expect that the user is going to click on a button that will take them to a specific page. It is your responsibility to ensure that the number of clicks are minimized for the user so that he quickly gets all the information he needs. Use your knowledge of the webpage to approximate real-world examples and present the content.

Examples of Final Queries Generated at the End of Step 3
Example 1: Contact Form Submission
form_data: ['name': 'Alice', 'email': 'alice@example.com', 'message': 'I would like more information.']
html_code:

<form action="/model" method="POST">
    <input type="text" name="name" value="Alice">
    <input type="email" name="email" value="alice@example.com">
    <textarea name="message">I would like more information.</textarea>
    <button type="submit" name="button_name" value="submitBtn" data-intention="submitForm">Submit</button>
</form>
problem: "User wants to submit a contact form to request more information."
Generated Query:
"Given the form data 'name': 'Alice', 'email': 'alice@example.com', 'message': 'I would like more information.' and the HTML code of the contact form, how should the system respond to the user who clicked the 'Submit' button to request more information?"

Answer:
"Dear Alice,

Thank you for reaching out to us! We have received your request for more information. Our team will review your message and get back to you shortly at the email address you provided: alice@example.com. If you have any urgent questions, please feel free to contact our support team directly.

Best regards,
[Your Company Name]"

Example 2: Feedback Form Submission
form_data: 'fullname': 'Bob', 'email': 'bob@example.com', 'feedback': 'Great service!'

html_code:

<form action="/model" method="POST">
    <input type="text" name="fullname" value="Bob">
    <input type="email" name="email" value="bob@example.com">
    <textarea name="feedback">Great service!</textarea>
    <button type="submit" name="button_name" value="feedbackBtn" data-intention="submitFeedback">Submit Feedback</button>
</form>
problem: "User wants to submit feedback about the service."
Generated Query:
"Given the form data 'fullname': 'Bob', 'email': 'bob@example.com', 'feedback': 'Great service!' and the HTML code of the feedback form, how should the system respond to the user who clicked the 'Submit Feedback' button to provide feedback about the service?"
Answer:
"Hi Bob,

Thank you for your wonderful feedback! We are delighted to hear that you had a great experience with our service. Your feedback is very important to us and helps us to continuously improve. We appreciate you taking the time to share your thoughts.

Kind regards,
[Your Company Name]"

Example 3: Survey Form Submission
form_data: 'age': '30', 'gender': 'male', 'rating': '5'
html_code:

<form action="/model" method="POST">
    <input type="number" name="age" value="30">
    <select name="gender">
        <option value="male" selected>Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
    </select>
    <select name="rating">
        <option value="5" selected>5 - Excellent</option>
        <option value="4">4 - Very Good</option>
        <option value="3">3 - Good</option>
        <option value="2">2 - Fair</option>
        <option value="1">1 - Poor</option>
    </select>
    <button type="submit" name="button_name" value="surveyBtn" data-intention="submitSurvey">Submit Survey</button>
</form>
problem: "User wants to submit a survey with their demographic details and service rating."
Generated Query:
"Given the form data 'age': '30', 'gender': 'male', 'rating': '5' and the HTML code of the survey form, answer to the user who clicked the 'Submit Survey' button to provide their demographic details and service rating?"
Answer: 
"Thank you for participating in our survey!

We appreciate your time and feedback. Your responses have been recorded as follows:

Age: 30
Gender: Male
Service Rating: 5 - Excellent
Your input is valuable to us as we strive to provide the best possible service. If you have any additional comments or suggestions, please do not hesitate to reach out.

Best regards,
[Your Company Name]"

Given the generated query, provide the answer. Based on the answer and the {html_code}, regenerate the html code for the page that would contain the answer to the generated query. Ensure that the html generated is in line with the html code: {html_code} of the page where the user entered the query. Verify that the output just contains html code.
     ''')
    #print ("Input problem is",input_problem)
    #output = model_response(f'''Given the problem {input_problem}, generate an answer.''')

    # You can process the inputs here as needed
    name = session['name']
    content = remove_html_and_backticks(input_problem)
    session['html_code'] = content
    return render_template('almanac.html',name=content,almanac=name,url=session['url'])

def remove_html_and_backticks(input_text):
  # Remove "```html"
  cleaned_text = input_text.replace("```html", "")

  # Remove "```"
  cleaned_text = cleaned_text.replace("```", "")

  return cleaned_text

def detectiva_response(problem):
    url = 'https://dataville-427614.uc.r.appspot.com/detectiva'
    print ("Problem:",problem)
    data = {'problem': problem}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    ki_dict = json.loads(response.text)

# Extract the "output" value
    output_value = ki_dict['output']
    return output_value

@app.route('/detectiva', methods=['POST'])
def detectiva():
    data = request.get_json()
    message = data['message']
    raw_context = data['context']
    context = model_response(f'''Summarize the functionality of the web page: {raw_context}. Use this summary to answer the question posted by the user: {message}. Here is an example:
    
    Raw context summary:
"Introducing the latest in home automation: the SmartThermostat X. Our cutting-edge thermostat learns your schedule, adjusts temperatures automatically, and can be controlled remotely via our mobile app. Features include energy-saving modes, integration with smart home systems like Alexa and Google Home, and detailed usage reports. Easy installation and compatibility with most HVAC systems make SmartThermostat X a convenient choice for any household."

User's message:
"What are the main features of the SmartThermostat X?"

Example output:
The SmartThermostat X offers several advanced features including learning your schedule to adjust temperatures automatically, remote control via a mobile app, energy-saving modes, and integration with smart home systems like Alexa and Google Home. It also provides detailed usage reports and is easy to install, compatible with most HVAC systems.

Constraints:

1.Just output the answer
2.Do not provide the summary of the webpage
3.Answer the question by assuming the personality of the webpage you are provided as context. For example, if a webpage is around Smart Thermostat X, you need to answer as if you are Smart Thermostat X. If a web page is about Da Vinci, you need to answer questions as Leonardo Da Vinci.

''')
    #print (data)
    #print (message)
    #print (context)
    # Process the message and context, generate a response
    #detectiva_output = detectiva_response("Answer the question:"+message)
    # Process the message and context, generate a response
    #detectiva_output = detectiva_response(f'''You are an expert of building complex web applications. Analyze the given code for a webpage:{context}, and provide a response to the question asked by the user:{message}''')
    #print(detectiva_output)

    response = {"reply": context}
    return jsonify(response)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)

