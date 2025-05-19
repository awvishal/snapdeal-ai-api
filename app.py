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

@app.route('/generate-bullets', methods=['POST'])
def generate_bullets():
    data = request.json

    product = data.get('product', {})
    user = data.get('user', {})
    user_query = data.get('user_query', '')

    # Final formatted prompt
    prompt = f"""
You are Smart Assist, a Snapdeal shopping assistant.

Your job is to answer the user's question clearly, based on the product and user details provided.

Respond with exactly 3 short, persuasive bullet points (each under 100 characters) that help the user make a confident decision about buying the product.

If the user query asks for suggestions or recommendations, then add a 4th line exactly like this:
"Reco_API_Hit"
Do not include this line unless recommendation is explicitly asked.

Respond in this format only:
{{"bullets": ["...", "...", "...", "Reco_API_Hit" (if needed)]}}

---

Product Details:
{json.dumps(product, indent=2)}

User Details:
{json.dumps(user, indent=2)}

User Query:
{user_query}
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
