import joblib
from preprocess import preprocess_text

# Load trained model and vectorizer
model = joblib.load("models/phishing_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

def predict_email(text):
    processed_text = preprocess_text(text)
    text_tfidf = vectorizer.transform([processed_text])
    prediction = model.predict(text_tfidf)
    return "🚨 Phishing Email Detected!" if prediction[0] else "✅ Safe Email"

# Example test
if __name__ == "__main__":
    email = input("Enter an email message: ")
    print(predict_email(email))
