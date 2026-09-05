import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()


async def init_database():
    uri = os.getenv("MONGO_URI")

    mongo_client = AsyncIOMotorClient(uri)
    db = mongo_client["ai_project"]
    collection = db["prompts"]

    prompt_template = {
        "template": "You are an expert in given domain. Answer the following: {{userInput}}"
    }

    print("Connected to mongodb")

    try:
        await collection.update_one(
            {"_id": "Education_Prompt"},
            {"$set": prompt_template},
            upsert=True
        )

        print("Success: 'Education_Prompt' stored in Atlas!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        mongo_client.close()


if __name__ == "__main__":
    asyncio.run(init_database())
