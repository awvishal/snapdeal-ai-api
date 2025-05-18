from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import json

# ✅ FIXED: Hardcoded key for demo/testing
genai.configure(api_key="AIzaSyBWpPkPeCAqX_ua_AOgHiDUmuBmhvkvbLk")

model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

app = Flask(__name__)

@app.route('/generate-bullets', methods=['POST'])
def generate_bullets():
    data = request.json
    product = data.get('product', {})
    user = data.get('user', {})

    prompt = f"""
You are a Snapdeal shopping assistant.

Product: {product}
User: {user}

Give 3 friendly, persuasive bullet points in JSON format: {{"bullets": ["...", "...", "..."]}}
"""

    response = model.generate_content(prompt)

    try:
        text = response.text.strip("```json\n").strip("```").strip()
        bullets_json = json.loads(text)
    except:
        bullets_json = {"raw_output": response.text}

    return jsonify(bullets_json)

@app.route('/')
def health():
    return "✅ Snapdeal AI API is live!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
