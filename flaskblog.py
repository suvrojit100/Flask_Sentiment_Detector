from flask import Flask, render_template
app = Flask(__name__)

fform = 'form.html'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')

@app.route("/features")
def features():
    return render_template('features.html', title='Features')

@app.route("/form/yt")
def yt_form():
    return render_template('form.html', link='yt')   

@app.route("/form/insta")
def insta_form():
    return render_template(fform, link='insta') 

@app.route("/form/twtr")
def twtr_form():
    return render_template(fform , link='twtr')   

@app.route("/form/fb")
def fb_form():
    return render_template(fform , link='fb')

@app.route("/form/lnkdn")
def lnkdn_form():
    return render_template(fform , link='lnkdn')

if __name__ == '__main__':
    app.run(debug=True)
