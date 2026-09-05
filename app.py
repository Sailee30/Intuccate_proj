import os
import asyncio
from flask import Flask, request, jsonify, render_template
from motor.motor_asyncio import AsyncIOMotorClient
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def get_db():
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))["ai_project"]


def get_ai():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


async def process_logic(user_input, template, index=0):
    await asyncio.sleep(index * 1.5)

    final_prompt = f"{template} Answer in 1 sentence: {user_input}"

    client = get_ai()

    try:
        response = await client.aio.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=final_prompt
        )
        ai_answer = response.text.strip()
    except Exception as e:
        ai_answer = f"Gemini Error: {str(e)}"

    db = get_db()

    await db.history.insert_one({
        "request": user_input,
        "response": ai_answer
    })

    return ai_answer


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask-bulk", methods=["POST"])
async def ask_bulk():
    data = request.json

    if not data:
        return jsonify({"error": "No data received"}), 400

    inputs = data.get("userInput")

    if not inputs or not isinstance(inputs, list):
        return jsonify({"error": "Provide a list of strings"}), 400

    db = get_db()

    prompt_doc = await db.prompts.find_one(
        {"_id": "Education_Prompt"}
    )

    if prompt_doc is None:
        template = (
            "You are an expert in given domain. "
            "Answer the following: {{userInput}}"
        )

        await db.prompts.insert_one({
            "_id": "Education_Prompt",
            "template": template
        })
    else:
        template = prompt_doc["template"]

    tasks = [
        process_logic(text, template, i)
        for i, text in enumerate(inputs)
    ]

    results = await asyncio.gather(*tasks)

    return jsonify({"responses": results})


if __name__ == "__main__":
    app.run(debug=True, threaded=False)
