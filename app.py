from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import json

genai.configure(api_key="YOUR_GEMINI_API_KEY")  # Replace with your actual key

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

if __name__ == '__main__':
    app.run(debug=True)
