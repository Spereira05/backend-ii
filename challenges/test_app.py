import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns correct structure"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert data["status"] == "online"
    assert "version" in data
    assert "timestamp" in data

def test_get_all_items():
    """Test getting all items"""
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3  # We start with 3 items in our DB
    
    # Check structure of first item
    assert "id" in data[0]
    assert "name" in data[0]
    assert "price" in data[0]
    assert "quantity" in data[0]

def test_get_item_by_id():
    """Test getting a specific item by ID"""
    # Test with valid ID
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    
    # Test with invalid ID
    response = client.get("/items/999")
    assert response.status_code == 404
    
def test_create_item():
    """Test creating a new item"""
    new_item = {
        "name": "Test Item",
        "description": "This is a test item",
        "price": 99.99,
        "quantity": 5
    }
    
    response = client.post("/items", json=new_item)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == new_item["name"]
    assert data["price"] == new_item["price"]
    assert data["quantity"] == new_item["quantity"]
    assert "id" in data  # Ensure ID was assigned
    
    # Verify item was actually added
    get_response = client.get(f"/items/{data['id']}")
    assert get_response.status_code == 200

def test_update_item():
    """Test updating an existing item"""
    # First create an item
    new_item = {
        "name": "Update Test Item",
        "description": "This item will be updated",
        "price": 50.0,
        "quantity": 10
    }
    create_response = client.post("/items", json=new_item)
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # Now update it
    updated_data = {
        "name": "Updated Item",
        "description": "This item has been updated",
        "price": 75.0,
        "quantity": 5
    }
    update_response = client.put(f"/items/{item_id}", json=updated_data)
    assert update_response.status_code == 200
    updated_item = update_response.json()
    assert updated_item["id"] == item_id
    assert updated_item["name"] == updated_data["name"]
    assert updated_item["price"] == updated_data["price"]
    
    # Verify item was actually updated
    get_response = client.get(f"/items/{item_id}")
    assert get_response.json()["name"] == updated_data["name"]

def test_delete_item():
    """Test deleting an item"""
    # First create an item
    new_item = {
        "name": "Delete Test Item",
        "description": "This item will be deleted",
        "price": 25.0,
        "quantity": 3
    }
    create_response = client.post("/items", json=new_item)
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # Now delete it
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 204
    
    # Verify item was actually deleted
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_create_item_validation():
    """Test validation when creating items"""
    # Test with missing required fields
    response = client.post("/items", json={"name": "Invalid Item"})
    assert response.status_code == 422
    
    # Test with invalid price (must be > 0)
    response = client.post("/items", json={
        "name": "Invalid Item",
        "price": -10.0,
        "quantity": 5
    })
    assert response.status_code == 422
    
    # Test with invalid quantity (must be >= 0)
    response = client.post("/items", json={
        "name": "Invalid Item",
        "price": 10.0,
        "quantity": -5
    })
    assert response.status_code == 422