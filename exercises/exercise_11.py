import graphene
from graphene import ObjectType, String, Schema, Field, Mutation, List
import uuid

# Mock database
users_db = [
    {"id": "1", "name": "Alice", "email": "alice@example.com"},
    {"id": "2", "name": "Bob", "email": "bob@example.com"},
    {"id": "3", "name": "Charlie", "email": "charlie@example.com"}
]

# GraphQL Type
class User(ObjectType):
    id = String(required=True)
    name = String(required=True)
    email = String(required=True)

# Query
class Query(ObjectType):
    # Get a single user by ID
    user = Field(User, id=String(required=True))
    # Get all users
    users = List(User)
    
    def resolve_user(self, info, id):
        for user in users_db:
            if user["id"] == id:
                return user
        return None
    
    def resolve_users(self, info):
        return users_db

# Mutation to update a user's name
class UpdateUserName(Mutation):
    class Arguments:
        id = String(required=True)
        name = String(required=True)
    
    # Output fields
    user = Field(User)
    
    def mutate(self, info, id, name):
        for user in users_db:
            if user["id"] == id:
                user["name"] = name
                return UpdateUserName(user=user)
        return None

# Mutation to create a new user
class CreateUser(Mutation):
    class Arguments:
        name = String(required=True)
        email = String(required=True)
    
    # Output fields
    user = Field(User)
    
    def mutate(self, info, name, email):
        # Generate a new ID
        new_id = str(uuid.uuid4())[:8]
        
        # Create new user
        new_user = {
            "id": new_id,
            "name": name,
            "email": email
        }
        
        # Add to database
        users_db.append(new_user)
        return CreateUser(user=new_user)

# Root mutation
class Mutation(ObjectType):
    update_user_name = UpdateUserName.Field()
    create_user = CreateUser.Field()

# Create schema
schema = Schema(query=Query, mutation=Mutation)

# Example query and mutations
if __name__ == "__main__":
    # Example query to get all users
    query_string = """
    {
        users {
            id
            name
            email
        }
    }
    """
    
    # Execute the query
    result = schema.execute(query_string)
    print("Query Result (All Users):")
    for user in result.data["users"]:
        print(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}")
    
    # Example mutation to update a user's name
    mutation_string = """
    mutation {
        updateUserName(id: "2", name: "Robert") {
            user {
                id
                name
            }
        }
    }
    """
    
    # Execute the mutation
    result = schema.execute(mutation_string)
    print("\nMutation Result (Update User):")
    print(f"Updated User: ID: {result.data['updateUserName']['user']['id']}, " + 
          f"New Name: {result.data['updateUserName']['user']['name']}")
    
    # Example mutation to create a new user
    mutation_string = """
    mutation {
        createUser(name: "David", email: "david@example.com") {
            user {
                id
                name
                email
            }
        }
    }
    """
    
    # Execute the mutation
    result = schema.execute(mutation_string)
    print("\nMutation Result (Create User):")
    new_user = result.data['createUser']['user']
    print(f"New User: ID: {new_user['id']}, Name: {new_user['name']}, Email: {new_user['email']}")
    
    # Verify the updated database
    print("\nUpdated User List:")
    result = schema.execute(query_string)
    for user in result.data["users"]:
        print(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}")