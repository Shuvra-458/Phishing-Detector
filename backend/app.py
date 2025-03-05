from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import googleapiclient.discovery
from gmail_auth import authenticate_gmail
from preprocess import preprocess_text

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load trained model and vectorizer
model = joblib.load("../models/phishing_model.pkl")
vectorizer = joblib.load("../models/vectorizer.pkl")

def predict_email(text):
    """Classifies the given email text as phishing or safe."""
    processed_text = preprocess_text(text)
    text_tfidf = vectorizer.transform([processed_text])
    prediction = model.predict(text_tfidf)
    return "Phishing" if prediction[0] else "Safe"

@app.route("/fetch_emails", methods=["GET"])
def fetch_emails():
    """Fetch unread Gmail messages using OAuth authentication and classify them."""
    creds = authenticate_gmail()
    service = googleapiclient.discovery.build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
    messages = results.get("messages", [])

    if not messages:
        return jsonify({"message": "✅ No unread emails found."})

    email_results = []
    for msg in messages[:5]:  # Limit to 5 emails
        msg_id = msg["id"]
        msg_data = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
        
        payload = msg_data["payload"]
        headers = payload.get("headers", [])

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")

        # Extract email body
        body = ""
        if "data" in payload.get("body", {}):
            body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
        else:
            for part in payload.get("parts", []):
                if "data" in part.get("body", {}):
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                    break

        # Analyze email with AI model
        result = predict_email(body)
        email_results.append({"subject": subject, "body": body[:100], "prediction": result})

    return jsonify(email_results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
