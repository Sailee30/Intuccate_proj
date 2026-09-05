import os       
import asyncio  
from flask import Flask, request, jsonify, render_template
from motor.motor_asyncio import AsyncIOMotorClient
from google import genai
from dotenv import load_dotenv

# Application Initialization
load_dotenv()

# Create the Flask application instance.
# __name__ tells Flask where to find templates/ and static/ folders
app = Flask(__name__)

def get_db():
      return AsyncIOMotorClient(os.getenv("MONGO_URI"))["ai_project"]

def get_ai():
        return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def process_logic(user_input, template, index=0):
    #Step 1
    # Each concurrent task waits (index * 1.5) seconds before
    # calling Gemini. This spreads requests over time to stay
    # within the model's rate limits.
    await asyncio.sleep(index * 1.5)

    #Step 2
    # Combine the reusable prompt template (from MongoDB) with
    # the specific user question. The "Answer in 1 sentence"
    # instruction keeps responses concise.
    final_prompt = f"{template} Answer in 1 sentence: {user_input}"

    #Step 3
    client = get_ai()

    try:
        # Use the async interface (client.aio) to generate content
        # without blocking the event loop. The 'gemini-3.1-flash-lite'
        # model is optimized for fast, low-cost responses.
        response = await client.aio.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=final_prompt
        )
        # Extract and clean up the generated text
        ai_answer = response.text.strip()
    except Exception as e:
        # Capture any API errors (auth failures, quota exceeded,
        # network issues) and return a human-readable message.
        ai_answer = f"Gemini Error: {str(e)}"

    # Step 4
    # Insert the question-answer pair into the 'history' collection
    # for future reference, analytics, and audit trails.
    db = get_db()
    await db.history.insert_one({
        "request": user_input,
        "response": ai_answer
    })

    return ai_answer

# Flask Route Handlers
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask-bulk', methods=['POST'])
async def ask_bulk():
      # Parse the JSON body from the incoming POST request
    data = request.json

    # Extract the list of questions from the payload
    inputs = data.get("userInput")

    # Input Validation
    # Ensure the client sent a non-empty list of strings.
    if not inputs or not isinstance(inputs, list):
        return jsonify({"error": "Provide a list of strings"}), 400

    # Fetch Prompt Template
    # The prompt template is stored in MongoDB under the 'prompts'
    # collection.
    db = get_db()

    prompt_doc = await db.prompts.find_one({"_id": "Education_Prompt"})

   if prompt_doc is None:
          template = "You are an expert in given domain. Answer the following: {{userInput}}"
          await db.prompts.insert_one({
              "_id": "Education_Prompt",
              "template": template
          })
   else:
          template = prompt_doc["template"]

    # Trigger Parallel AI Tasks
    # Build a list of coroutines, one per question. Each coroutine
    # receives a stagger index (i) to space out Gemini API calls.
    tasks = [process_logic(text, template, i) for i, text in enumerate(inputs)]

    # asyncio.gather() runs all tasks concurrently and waits for
    # all of them to complete. Results are returned in the same
    # order as the input list.
    results = await asyncio.gather(*tasks)

    # Return the list of AI-generated answers as JSON
    return jsonify({"responses": results})

if __name__ == '__main__':
    app.run(debug=True, threaded=False)
