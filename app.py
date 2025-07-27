from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from urllib.parse import urlparse
import re

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load("pickle/model.pkl")

# Enhanced Feature Extraction - ensures exactly 30 features
def extract_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    features = []

    # Basic URL structure
    features.append(len(url))                          # 1. URL length
    features.append(url.count('.'))                    # 2. Number of dots
    features.append(url.count('/'))                    # 3. Number of slashes
    features.append(url.count('-'))                    # 4. Hyphen count
    features.append(url.count('@'))                    # 5. @ character
    features.append(url.count('='))                    # 6. Equal sign count
    features.append(url.count('?'))                    # 7. Question marks
    features.append(url.count('&'))                    # 8. Ampersand count
    features.append(url.count('%'))                    # 9. Percentage signs
    features.append(int('https' in url.lower()))       # 10. Uses HTTPS

    # Domain and path properties
    features.append(len(domain))                       # 11. Domain length
    features.append(len(path))                         # 12. Path length
    features.append(int(domain.count('.') >= 3))       # 13. Subdomain depth
    features.append(int(bool(re.search(r'\d', domain)))) # 14. Digits in domain
    features.append(int('ip' in url.lower()))          # 15. Contains 'ip'
    features.append(int('login' in url.lower()))       # 16. Contains 'login'
    features.append(int('secure' in url.lower()))      # 17. Contains 'secure'
    features.append(int('account' in url.lower()))     # 18. Contains 'account'
    features.append(int(bool(re.search(r'^https?:\/\/\d+\.\d+\.\d+\.\d+', url)))) # 19. Starts with IP
    features.append(int('//' in url[8:]))              # 20. Multiple //

    # Boolean indicators
    features.append(int(bool(re.search(r'[^\w\-]', url))))  # 21. Special characters
    features.append(int('bank' in url.lower()))        # 22. Contains 'bank'
    features.append(int('confirm' in url.lower()))     # 23. Contains 'confirm'
    features.append(int('update' in url.lower()))      # 24. Contains 'update'
    features.append(int('ebay' in url.lower()))        # 25. Contains 'ebay'
    features.append(int('paypal' in url.lower()))      # 26. Contains 'paypal'

    # Extra: heuristic patterns
    features.append(int(url.lower().startswith('http://'))) # 27. HTTP only
    features.append(int(domain.endswith('.zip')))      # 28. Ends with .zip
    features.append(int(domain.endswith('.exe')))      # 29. Ends with .exe
    features.append(int('free' in url.lower()))        # 30. Contains 'free'

    return features

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        features = extract_features(url)

        # Predict using model (should have 30 features)
        prediction = model.predict([features])[0]

        label = "phishing" if prediction == 1 else "legitimate"
        return jsonify({"result": label})

    except Exception as e:
        print("Error during prediction:", str(e))
        return jsonify({"error": "Error during prediction"}), 500

@app.route("/")
def home():
    return "Phishing Detection API is running."

if __name__ == "__main__":
    app.run(debug=True, port=5000)
