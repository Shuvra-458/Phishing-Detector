import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()

def load_dataset(filename="dataset/emails.csv"):
    df = pd.read_csv(filename)
    df = df[['text', 'target']] 
    return df

def preprocess_text(text):
   
    stop_words = set(stopwords.words("english"))
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters, numbers, and punctuation
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    
    return " ".join(words)

if __name__ == "__main__":
    sample_text = "Congratulations! You've won $1000. Click here to claim your prize now!"
    print("Original:", sample_text)
    print("Processed:", preprocess_text(sample_text))
