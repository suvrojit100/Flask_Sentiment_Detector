import flask
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib
import preprocess
import keras.preprocessing.text  # Ensure this is imported

# Flask utils
from flask import Flask, session, redirect, url_for, render_template, request
from werkzeug.utils import secure_filename

# Custom unpickler
import pickle

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'keras.src.preprocessing':
            module = 'keras.preprocessing'
        return super().find_class(module, name)

# Load tokenizer
with open('tokenizer.joblib', 'rb') as f:
    tokenizer = CustomUnpickler(f).load()

# Load max_length
with open('max_length.joblib', 'rb') as f:
    max_length = joblib.load(f)

# Load model
model = tf.keras.models.model_from_json(open('model.json', 'r').read())

app = Flask(__name__)

max_length = 100  # Set the max length for padding

@app.route('/process_comments', methods=['POST'])
def predict_custom_input():
    input_text = request.json['input_text']
    cleaned_text = preprocess(input_text)
    sequence = tokenizer.texts_to_sequences([cleaned_text])
    padded_sequence = pad_sequences(sequence, maxlen=max_length)
    prediction = model.predict(padded_sequence)[0][0]
    sentiment = "Positive" if prediction >= 0.5 else "Negative"
    print("Predicted Sentiment:", sentiment)
    return sentiment

def process_comments():
    url = 'https://www.youtube.com/watch?v=7n8EzY2GeZU' 
    
    # Scrape comments and translate them
    df = scrapfyt(url)
    df['translated_comments'] = df['comments'].apply(translate_comments)
    
    # Filter negative comments using the model
    negative_comments = []
    for _, row in df.iterrows():
        sentiment = predict_custom_input(row['translated_comments'])
        if sentiment == 'Negative':
            negative_comments.append({'username': row['username'], 'comment': row['comments']})
    
    # Create a dataframe with negative comments and usernames
    negative_df = pd.DataFrame(negative_comments)
    
    return negative_df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)



# import flask
# import pandas as pd
# import tensorflow as tf
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# import joblib
# import preprocess
# import scrapfyt_module

# # Flask utils
# from flask import Flask, session, redirect, url_for, render_template, request
# from werkzeug.utils import secure_filename

# # Load tokenizer
# tokenizer = joblib.load('tokenizer.joblib')

# # Load max_length
# max_length = joblib.load('max_length.joblib')

# # Load model
# model = tf.keras.models.model_from_json(open('model.json', 'r').read())

# app = Flask(__name__)

# max_length = 100  # Set the max length for padding

# @app.route('/process_comments', methods=['POST'])
# def predict_custom_input():
#     input_text = request.json['input_text']
#     cleaned_text = preprocess(input_text)
#     sequence = tokenizer.texts_to_sequences([cleaned_text])
#     padded_sequence = pad_sequences(sequence, maxlen=max_length)
#     prediction = model.predict(padded_sequence)[0][0]
#     sentiment = "Positive" if prediction >= 0.5 else "Negative"
#     print("Predicted Sentiment:", sentiment)
#     return sentiment

# def process_comments():
#     url = 'https://www.youtube.com/watch?v=7n8EzY2GeZU' 
    
#     # Scrape comments and translate them
#     df = scrapfyt(url)
#     df['translated_comments'] = df['comments'].apply(translate_comments)
    
#     # Filter negative comments using the model
#     negative_comments = []
#     for _, row in df.iterrows():
#         sentiment = predict_custom_input(row['translated_comments'])
#         if sentiment == 'Negative':
#             negative_comments.append({'username': row['username'], 'comment': row['comments']})
    
#     # Create a dataframe with negative comments and usernames
#     negative_df = pd.DataFrame(negative_comments)
    
#     return negative_df.to_json(orient='records')

# if __name__ == '__main__':
#     app.run(debug=True)
