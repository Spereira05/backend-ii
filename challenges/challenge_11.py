import graphene
from graphene import ObjectType, String, Int, List, Field, Mutation, Boolean, Enum, Interface
from graphql import GraphQLError
import uuid
import datetime
import jwt
import os
from functools import wraps

# Secret key for JWT tokens
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'development-secret-key')

# Mock database
users_db = [
    {"id": "1", "username": "alice", "email": "alice@example.com", "password": "password123", "role": "ADMIN"},
    {"id": "2", "username": "bob", "email": "bob@example.com", "password": "password456", "role": "USER"},
]

posts_db = [
    {"id": "1", "title": "First Post", "content": "This is Alice's first post", "author_id": "1", "published": True, "created_at": "2023-01-15T12:00:00Z"},
    {"id": "2", "title": "GraphQL Tutorial", "content": "Learn about GraphQL", "author_id": "1", "published": True, "created_at": "2023-02-20T14:30:00Z"},
    {"id": "3", "title": "My Experience", "content": "Bob's experience with programming", "author_id": "2", "published": True, "created_at": "2023-03-05T09:15:00Z"},
    {"id": "4", "title": "Draft Post", "content": "This is not published yet", "author_id": "2", "published": False, "created_at": "2023-04-10T16:45:00Z"},
]

comments_db = [
    {"id": "1", "content": "Great post!", "post_id": "1", "user_id": "2", "created_at": "2023-01-16T10:30:00Z"},
    {"id": "2", "content": "Very informative", "post_id": "2", "user_id": "2", "created_at": "2023-02-21T08:45:00Z"},
    {"id": "3", "content": "Thanks for sharing", "post_id": "2", "user_id": "1", "created_at": "2023-02-22T15:20:00Z"},
    {"id": "4", "content": "I learned a lot", "post_id": "3", "user_id": "1", "created_at": "2023-03-06T11:10:00Z"},
]

# Role enum for user roles
class UserRole(Enum):
    ADMIN = "ADMIN"
    USER = "USER"

# JWT Authentication
def get_token_from_info(info):
    """Extract JWT token from the request context"""
    auth_header = info.context.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    return auth_header[7:]  # Remove 'Bearer ' prefix

def authenticate(f):
    """Decorator to check if user is authenticated"""
    @wraps(f)
    def wrapper(self, info, *args, **kwargs):
        token = get_token_from_info(info)
        if not token:
            raise GraphQLError("Authentication required")
        
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            info.context['user_id'] = decoded['user_id']
            info.context['role'] = decoded['role']
        except jwt.InvalidTokenError:
            raise GraphQLError("Invalid token")
            
        return f(self, info, *args, **kwargs)
    return wrapper

def admin_required(f):
    """Decorator to check if user is an admin"""
    @wraps(f)
    def wrapper(self, info, *args, **kwargs):
        if info.context.get('role') != 'ADMIN':
            raise GraphQLError("Admin privileges required")
        return f(self, info, *args, **kwargs)
    return wrapper

# Interface for timestamps
class TimestampInterface(Interface):
    created_at = String()

# GraphQL Types
class User(ObjectType):
    id = String(required=True)
    username = String(required=True)
    email = String(required=True)
    role = String()
    posts = List(lambda: Post)
    comments = List(lambda: Comment)
    
    def resolve_posts(self, info):
        # Only return published posts for non-authors
        user_id = info.context.get('user_id')
        if user_id == self.id or info.context.get('role') == 'ADMIN':
            return [post for post in posts_db if post["author_id"] == self.id]
        else:
            return [post for post in posts_db if post["author_id"] == self.id and post["published"]]
    
    def resolve_comments(self, info):
        return [comment for comment in comments_db if comment["user_id"] == self.id]

class Post(ObjectType):
    class Meta:
        interfaces = (TimestampInterface,)
        
    id = String(required=True)
    title = String(required=True)
    content = String(required=True)
    published = Boolean(required=True)
    author = Field(User)
    comments = List(lambda: Comment)
    
    def resolve_author(self, info):
        for user in users_db:
            if user["id"] == self["author_id"]:
                return user
        return None
    
    def resolve_comments(self, info):
        return [comment for comment in comments_db if comment["post_id"] == self.id]

class Comment(ObjectType):
    class Meta:
        interfaces = (TimestampInterface,)
        
    id = String(required=True)
    content = String(required=True)
    post = Field(Post)
    user = Field(User)
    
    def resolve_post(self, info):
        for post in posts_db:
            if post["id"] == self["post_id"]:
                return post
        return None
    
    def resolve_user(self, info):
        for user in users_db:
            if user["id"] == self["user_id"]:
                return user
        return None

# Login mutation
class LoginUser(Mutation):
    class Arguments:
        username = String(required=True)
        password = String(required=True)
    
    token = String()
    user = Field(User)
    
    def mutate(self, info, username, password):
        for user in users_db:
            if user["username"] == username and user["password"] == password:
                # Generate JWT token
                token_payload = {
                    'user_id': user['id'],
                    'role': user['role'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
                }
                token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
                return LoginUser(token=token, user=user)
        
        raise GraphQLError("Invalid username or password")

# Create post mutation
class CreatePost(Mutation):
    class Arguments:
        title = String(required=True)
        content = String(required=True)
        published = Boolean(default_value=False)
    
    post = Field(Post)
    
    @authenticate
    def mutate(self, info, title, content, published):
        user_id = info.context.get('user_id')
        
        new_post = {
            "id": str(uuid.uuid4())[:8],
            "title": title,
            "content": content,
            "author_id": user_id,
            "published": published,
            "created_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
        
        posts_db.append(new_post)
        return CreatePost(post=new_post)

# Update post mutation
class UpdatePost(Mutation):
    class Arguments:
        id = String(required=True)
        title = String()
        content = String()
        published = Boolean()
    
    post = Field(Post)
    
    @authenticate
    def mutate(self, info, id, **kwargs):
        user_id = info.context.get('user_id')
        user_role = info.context.get('role')
        
        for post in posts_db:
            if post["id"] == id:
                # Check if user is author or admin
                if post["author_id"] != user_id and user_role != "ADMIN":
                    raise GraphQLError("Not authorized to update this post")
                
                # Update fields
                if 'title' in kwargs:
                    post["title"] = kwargs['title']
                if 'content' in kwargs:
                    post["content"] = kwargs['content']
                if 'published' in kwargs:
                    post["published"] = kwargs['published']
                
                return UpdatePost(post=post)
        
        raise GraphQLError("Post not found")

# Delete post mutation
class DeletePost(Mutation):
    class Arguments:
        id = String(required=True)
    
    success = Boolean()
    
    @authenticate
    def mutate(self, info, id):
        user_id = info.context.get('user_id')
        user_role = info.context.get('role')
        
        for i, post in enumerate(posts_db):
            if post["id"] == id:
                # Check if user is author or admin
                if post["author_id"] != user_id and user_role != "ADMIN":
                    raise GraphQLError("Not authorized to delete this post")
                
                # Delete post
                del posts_db[i]
                
                # Also delete related comments
                comments_db[:] = [c for c in comments_db if c["post_id"] != id]
                
                return DeletePost(success=True)
        
        raise GraphQLError("Post not found")

# Add comment mutation
class AddComment(Mutation):
    class Arguments:
        post_id = String(required=True)
        content = String(required=True)
    
    comment = Field(Comment)
    
    @authenticate
    def mutate(self, info, post_id, content):
        user_id = info.context.get('user_id')
        
        # Check if post exists and is published
        post = next((p for p in posts_db if p["id"] == post_id), None)
        if not post:
            raise GraphQLError("Post not found")
        
        if not post["published"] and post["author_id"] != user_id and info.context.get('role') != "ADMIN":
            raise GraphQLError("Cannot comment on unpublished post")
        
        new_comment = {
            "id": str(uuid.uuid4())[:8],
            "content": content,
            "post_id": post_id,
            "user_id": user_id,
            "created_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
        
        comments_db.append(new_comment)
        return AddComment(comment=new_comment)

# Delete user mutation (admin only)
class DeleteUser(Mutation):
    class Arguments:
        id = String(required=True)
    
    success = Boolean()
    
    @authenticate
    @admin_required
    def mutate(self, info, id):
        for i, user in enumerate(users_db):
            if user["id"] == id:
                del users_db[i]
                
                # Delete related posts and comments
                posts_db[:] = [p for p in posts_db if p["author_id"] != id]
                comments_db[:] = [c for c in comments_db if c["user_id"] != id]
                
                return DeleteUser(success=True)
        
        raise GraphQLError("User not found")

# Query
class Query(ObjectType):
    # User queries
    user = Field(User, id=String())
    users = List(User)
    me = Field(User)
    
    # Post queries
    post = Field(Post, id=String(required=True))
    posts = List(Post, published=Boolean())
    
    # Comment queries
    comment = Field(Comment, id=String(required=True))
    comments = List(Comment, post_id=String())
    
    def resolve_user(self, info, id=None):
        if id:
            for user in users_db:
                if user["id"] == id:
                    return user
            return None
        return None
    
    def resolve_users(self, info):
        return users_db
    
    @authenticate
    def resolve_me(self, info):
        user_id = info.context.get('user_id')
        for user in users_db:
            if user["id"] == user_id:
                return user
        return None
    
    def resolve_post(self, info, id):
        user_id = info.context.get('user_id')
        user_role = info.context.get('role')
        
        for post in posts_db:
            if post["id"] == id:
                # Check if post is published or user is author/admin
                if post["published"] or user_id == post["author_id"] or user_role == "ADMIN":
                    return post
                else:
                    raise GraphQLError("Not authorized to view this post")
        return None
    
    def resolve_posts(self, info, published=None):
        user_id = info.context.get('user_id')
        user_role = info.context.get('role')
        
        if published is not None:
            filtered_posts = [p for p in posts_db if p["published"] == published]
        else:
            # If not admin or logged in, only show published posts
            if not user_id or user_role != "ADMIN":
                filtered_posts = [p for p in posts_db if p["published"]]
            else:
                filtered_posts = posts_db
                
        return filtered_posts
    
    def resolve_comment(self, info, id):
        for comment in comments_db:
            if comment["id"] == id:
                return comment
        return None
    
    def resolve_comments(self, info, post_id=None):
        if post_id:
            return [c for c in comments_db if c["post_id"] == post_id]
        return comments_db

# Mutation
class Mutation(ObjectType):
    login = LoginUser.Field()
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    add_comment = AddComment.Field()
    delete_user = DeleteUser.Field()

# Schema
schema = Schema(query=Query, mutation=Mutation)

if __name__ == "__main__":
    print("Advanced GraphQL API with Authentication")
    print("This module implements a GraphQL API with the following features:")
    print("- User authentication with JWT")
    print("- Role-based authorization (Admin/User)")
    print("- Nested queries for users, posts, and comments")
    print("- Interface for timestamp fields")
    print("- CRUD operations with proper permissions")