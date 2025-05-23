import asyncio
from fastapi import FastAPI
import uvicorn
import time
from typing import Dict

app = FastAPI()

async def fetch_user_data(user_id: int) -> Dict:
    # Simulating a database query with a delay
    await asyncio.sleep(2)  # Simulates database access latency
    return {
        "id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com"
    }

async def fetch_order_history(user_id: int) -> Dict:
    # Simulating an API call with a delay
    await asyncio.sleep(1.5)  # Simulates API access latency
    return {
        "user_id": user_id,
        "orders": [
            {"id": 1, "item": "Product A", "amount": 50.0},
            {"id": 2, "item": "Product B", "amount": 30.0},
            {"id": 3, "item": "Product C", "amount": 25.0}
        ]
    }

@app.get("/user/{user_id}")
async def get_user_profile(user_id: int):
    start_time = time.time()
    
    # Fetch data concurrently using asyncio.gather
    user_data, order_history = await asyncio.gather(
        fetch_user_data(user_id),
        fetch_order_history(user_id)
    )
    
    # Combine the results
    profile = {
        "user": user_data,
        "orders": order_history["orders"],
        "fetch_time": f"{time.time() - start_time:.2f} seconds"
    }
    
    return profile

if __name__ == "__main__":
    print("Starting FastAPI server...")
    print("To test: Open http://127.0.0.1:8000/user/123 in your browser")
    uvicorn.run(app, host="127.0.0.1", port=8000)