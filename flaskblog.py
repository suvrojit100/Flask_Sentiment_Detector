from flask import Flask, render_template, request
import pandas as pd
from functions.scrapfyt_module import scrapfyt

app = Flask(__name__)

# Route for home page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

# Route for handling form submission
@app.route('/read_form', methods=['POST'])
def read_form():
    data = request.form
    url = data['video_link']
    choice = data['choice']

    result = scrapfyt(url)
    
    tables = None
    titles = None

    # Handle different choices here
    if choice == '1':
        # Convert result (assuming it's a DataFrame) to HTML
        tables = [result.to_html(classes='table table-striped')]
        titles = ['User Comments']
    elif choice == '2':
        return "Receiving translated comment data"
    elif choice == '3':
        return render_template('features.html', title='Features')
    else:
        return "Invalid choice"

    # Pass the tables and titles to form.html
    return render_template('form.html', tables=tables, titles=titles)


# Other routes for navigation
@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')

@app.route("/features")
def features():
    return render_template('features.html', title='Features')

@app.route('/task')
def task():
    return render_template('task.html', title='Task')

if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, render_template, request

# app = Flask(__name__)

# from functions.scrapfyt_module import scrapfyt

# # Route for home page
# @app.route("/")
# @app.route("/home")
# def home():
#     return render_template('home.html')

# # Route for handling form submission
# @app.route('/read_form', methods=['POST'])
# def read_form():
#     data = request.form
#     url = data['video_link']
#     choice = data['choice']

#     result = scrapfyt(url)
    
#     tables = None
#     titles = None

#     # Handle different choices here
#     if choice == '1':
        
#         tables = [result] 
#         titles = ['User Comments']
#     elif choice == '2':
#         return "Receiving translated comment data"
#     elif choice == '3':
#         return render_template('features.html', title='Features')
#     else:
#         return "Invalid choice"

#     return render_template('features.html', tables=tables, titles=titles)

# # Other routes for navigation
# @app.route("/about")
# def about():
#     return render_template('about.html', title='About')

# @app.route("/contact")
# def contact():
#     return render_template('contact.html', title='Contact')

# @app.route("/features")
# def features():
#     return render_template('features.html', title='Features')

# @app.route('/task')
# def task():
#     return render_template('task.html', title='Task')

# # @app.route('/submit_link', methods=['POST'])
# # def submit_link():
# #     link = request.form.get('link')
# #     return render_template('task.html')    

# if __name__ == '__main__':
#     app.run(debug=True)
