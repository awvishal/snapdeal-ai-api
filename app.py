@app.route('/generate-bullets', methods=['POST'])
def generate_bullets():
    data = request.json
    product = data.get('product', {})
    user = data.get('user', {})
    custom_prompt = data.get('prompt', None)

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
        bullets_json = {"error": str(e), "raw_output": response.text}

    return jsonify(bullets_json)
