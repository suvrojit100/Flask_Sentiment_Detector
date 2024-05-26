from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_instagram_comments', methods=['POST'])
def get_instagram_comments():
    post_link = request.form['post_link']
    choice = request.form['choice']

    # Call your functions based on the user's choice
    if choice == '1':
        # Get actual comments of the post and download
        pass
    elif choice == '2':
        # Get the translated version of the comments
        pass
    elif choice == '3':
        # Get positive/negative/both comments
        pass

    # Return a response to the user
    return 'Functionality not implemented yet'

if __name__ == '__main__':
    app.run(debug=True)
