import re
import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
def preprocess(text):
    # Removing URLS
    text = re.sub(r"https?://\S+|www\.\S+"," ",text)

    # Removing html tags
    text = re.sub(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});"," ",text)

    # Removing the Punctuation
    text = re.sub(r"[^\w\s]", " ", text)

    # Removing words that have numbers
    text = re.sub(r"\w*\d\w*", " ", text)

    # Removing Digits
    text = re.sub(r"[0-9]+", " ", text)

    # Cleaning white spaces
    text = re.sub(r"\s+", " ", text).strip()

    text = text.lower()
    # Check stop words
    tokens = []
    for token in text.split():
        if token not in stop_words and len(token) > 3:
            tokens.append(token)
    return " ".join(tokens)