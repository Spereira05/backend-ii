from fastapi import FastAPI, HTTPException, Depends, status
import uvicorn
import os
from typing import List, Optional
from pydantic import BaseModel, Field
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Sample API for CI/CD Demo",
    description="A simple API to demonstrate CI/CD pipelines with GitHub Actions",
    version="1.0.0"
)

# Pydantic models
class Item(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Sample Item",
                "description": "This is a sample item description",
                "price": 29.99,
                "quantity": 10
            }
        }

# In-memory database
items_db = [
    {
        "id": 1,
        "name": "Laptop",
        "description": "High performance laptop with 16GB RAM",
        "price": 999.99,
        "quantity": 10
    },
    {
        "id": 2,
        "name": "Smartphone",
        "description": "Latest smartphone with advanced camera",
        "price": 699.99,
        "quantity": 15
    },
    {
        "id": 3,
        "name": "Headphones",
        "description": "Wireless noise-cancelling headphones",
        "price": 199.99,
        "quantity": 20
    }
]

# Helper functions
def get_next_id():
    return max([item["id"] for item in items_db]) + 1 if items_db else 1

# Routes
@app.get("/")
async def root():
    """Root endpoint that returns a welcome message and API status"""
    return {
        "message": "Welcome to the Sample API",
        "status": "online",
        "version": app.version,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/items", response_model=List[Item])
async def get_items():
    """Get all items"""
    logger.info("Fetching all items")
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a specific item by ID"""
    logger.info(f"Fetching item with ID: {item_id}")
    
    for item in items_db:
        if item["id"] == item_id:
            return item
    
    logger.warning(f"Item with ID {item_id} not found")
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    """Create a new item"""
    logger.info("Creating new item")
    
    # Create new item with auto-generated ID
    new_item = item.dict()
    new_item["id"] = get_next_id()
    
    # Add to database
    items_db.append(new_item)
    logger.info(f"Created item with ID: {new_item['id']}")
    
    return new_item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    """Update an existing item"""
    logger.info(f"Updating item with ID: {item_id}")
    
    for i, existing_item in enumerate(items_db):
        if existing_item["id"] == item_id:
            # Update the item while preserving its ID
            updated_item = item.dict()
            updated_item["id"] = item_id
            items_db[i] = updated_item
            
            logger.info(f"Updated item with ID: {item_id}")
            return updated_item
    
    logger.warning(f"Item with ID {item_id} not found for update")
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """Delete an item"""
    logger.info(f"Deleting item with ID: {item_id}")
    
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            # Remove the item
            del items_db[i]
            logger.info(f"Deleted item with ID: {item_id}")
            return
    
    logger.warning(f"Item with ID {item_id} not found for deletion")
    raise HTTPException(status_code=404, detail="Item not found")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# Run the application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)