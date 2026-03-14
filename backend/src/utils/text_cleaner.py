import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
from pathlib import Path



#Downloading reqquired NKTK resources
nltk.download('stopwords')
nltk.download('wordnet')

#Initialize lemmatizer and stop words
tokenizer = TreebankWordTokenizer()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

#function to clean the text in txt files
def clean_text(text):
    """
    Cleans text files for ML processing by:
    1. Lowercasing all text
    2. Removing punctuation and special characters
    3. removing stop words
    4. Lemmatizing words to their base form

    Returns a cleaned version of the input text.

    """
    #1. Lowercasing text
    text = text.lower()

    #2. Removing punctuation and special characters
    text = re.sub(r'[^a-z0-9\s]','', text)

    #3. Tokenize words
    words = tokenizer.tokenize(text)

    #4. Removing stop words
    words = [word for word in words if word not in stop_words]

    #Lemmatizing words
    words = [lemmatizer.lemmatize(word, pos='n') for word in words]

    #returns cleaned text as a single string
    return ' '.join(words)


