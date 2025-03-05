import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from preprocess import load_dataset, preprocess_text

# Load dataset
df = load_dataset()
df["text"] = df["text"].apply(preprocess_text)

# Split data
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["target"], test_size=0.2, random_state=42)

# Convert text to numerical features
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train Naïve Bayes model
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Evaluate performance
y_pred = model.predict(X_test_tfidf)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model & vectorizer
joblib.dump(model, "models/phishing_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")
