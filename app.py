from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import json

# ✅ Hardcoded API key for now (move to env variable for prod)
genai.configure(api_key="AIzaSyBWpPkPeCAqX_ua_AOgHiDUmuBmhvkvbLk")

# ✅ Use Gemini 1.5 Flash model
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# ✅ Initialize Flask app
app = Flask(__name__)

# ✅ Main API route
@app.route('/generate-bullets', methods=['POST'])
def generate_bullets():
    data = request.json
    product = data.get('product', {})
    user = data.get('user', {})
    custom_prompt = data.get('prompt', None)

    # Use custom prompt if provided, else default
    if custom_prompt:
        prompt = custom_prompt
    else:
        prompt = f"""
You are a Snapdeal shopping assistant.

Product: {product}
User: {user}

Give 3 friendly, persuasive bullet points in JSON format: {{"bullets": ["...", "...", "..."]}}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip("```json\n").strip("```").strip()
        bullets_json = json.loads(text)
    except Exception as e:
        bullets_json = {
            "error": str(e),
            "raw_output": "No response generated due to an exception."
        }

    return jsonify(bullets_json)

# ✅ Health check
@app.route('/')
def health():
    return "✅ Snapdeal AI API is live!"

# ✅ Bind to 0.0.0.0 for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
