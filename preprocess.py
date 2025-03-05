import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources (only once)
nltk.download("stopwords")
nltk.download("wordnet")

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

def load_dataset(filename="dataset/emails.csv"):
    """
    Loads the dataset and ensures only required columns are used.
    Expects columns: 'text' and 'target'.
    """
    df = pd.read_csv(filename)
    df = df[['text', 'target']]  # Keep only relevant columns
    return df

def preprocess_text(text):
    """
    Cleans and preprocesses email text for model training.
    Steps:
    1. Convert to lowercase
    2. Remove special characters & punctuation
    3. Remove stopwords
    4. Lemmatize words
    """
    stop_words = set(stopwords.words("english"))
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters, numbers, and punctuation
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    
    # Remove stopwords & apply lemmatization
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    
    return " ".join(words)

# Example test
if __name__ == "__main__":
    sample_text = "Congratulations! You've won $1000. Click here to claim your prize now!"
    print("Original:", sample_text)
    print("Processed:", preprocess_text(sample_text))
