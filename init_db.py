

import asyncio  
import os   
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def init_database():
    
    # Step 1: Read the MongoDB connection string 
    uri = os.getenv("MONGO_URI")

    # Step 2: Create the async MongoDB client 
    mongo_client = AsyncIOMotorClient(uri)

    # Step 3: Select the database and collection 
    db = mongo_client["ai_project"]
    collection = db["prompts"]

    # Step 4: Define the prompt template document 
    prompt_template = {
        "_id": "Prompt",
        "template": "You are an expert in given domain. Answer the following: {{userInput}}"
    }

    print("Connected to mongodb")

    # Step 5: Upsert the prompt into MongoDB 
    try:
        await collection.update_one(
            {"_id": "Education_Prompt"},
            {"$set": prompt_template},
            upsert=True
        )
        print("Success: 'Education_Prompt' stored in Atlas!")

    except Exception as e:
        # Log any database errors (auth failure, network issues, etc.)
        print(f" Error: {e}")

    finally:
        # Always close the MongoDB connection to free resources,
        # regardless of whether the operation succeeded or failed.
        mongo_client.close()



# Script Entry Point
if __name__ == "__main__":
    # asyncio.run() creates a new event loop, runs the coroutine
    # to completion, and then closes the loop. This is the standard
    # way to execute an async function from a synchronous context.
    asyncio.run(init_database())