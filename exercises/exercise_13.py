# Exercise 13: Web Development Best Practices with Django and FastAPI

"""
This file demonstrates two minimal applications serving a "Hello World" endpoint:
1. A Django application
2. A FastAPI application

Both follow best practices for their respective frameworks.

To run the Django app:
1. Install Django: pip install django
2. Run: python exercise_13.py django

To run the FastAPI app:
1. Install FastAPI and Uvicorn: pip install fastapi uvicorn
2. Run: python exercise_13.py fastapi
"""

import sys
import os
from datetime import datetime

# DJANGO IMPLEMENTATION

def create_django_project():
    """
    Creates a minimal Django project with a "Hello World" endpoint
    following best practices
    """
    
    # Check if Django is installed
    try:
        import django
        from django.conf import settings
        from django.urls import path
        from django.http import JsonResponse
        from django.core.management import execute_from_command_line
        from django.middleware.csrf import CsrfViewMiddleware
        from django.middleware.security import SecurityMiddleware
        from django.middleware.common import CommonMiddleware
    except ImportError:
        print("Django is not installed. Please install with: pip install django")
        return

    # Configure Django settings
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            SECRET_KEY='django-insecure-key-for-development-only',
            ROOT_URLCONF=__name__,
            MIDDLEWARE=[
                'django.middleware.security.SecurityMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.middleware.clickjacking.XFrameOptionsMiddleware',
            ],
            ALLOWED_HOSTS=['*'],  # For development only
            TEMPLATES=[{
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            }],
        )
        django.setup()

    # Define a view
    def hello_world(request):
        """Simple Hello World endpoint with timestamp"""
        return JsonResponse({
            'message': 'Hello, World!',
            'framework': 'Django',
            'timestamp': datetime.now().isoformat(),
            'path': request.path,
        })

    # Define URL patterns
    urlpatterns = [
        path('', hello_world),
        path('hello/', hello_world),
    ]

    # Run the server
    print("Starting Django development server at http://127.0.0.1:8000/")
    print("Press CTRL+C to quit")
    
    # Use Django's management command to run the server
    sys.argv = ['exercise_13.py', 'runserver', '0.0.0.0:8000']
    execute_from_command_line(sys.argv)


# FASTAPI IMPLEMENTATION

def create_fastapi_app():
    """
    Creates a minimal FastAPI application with a "Hello World" endpoint
    following best practices
    """
    
    # Check if FastAPI and Uvicorn are installed
    try:
        import fastapi
        import uvicorn
        from fastapi import FastAPI, Request
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import JSONResponse
    except ImportError:
        print("FastAPI or Uvicorn is not installed.")
        print("Please install with: pip install fastapi uvicorn")
        return

    # Create FastAPI app with documentation
    app = FastAPI(
        title="Hello World API",
        description="A simple API that returns Hello World",
        version="1.0.0",
    )

    # Add middleware for security and CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # For development only
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Define a route
    @app.get("/", response_class=JSONResponse)
    @app.get("/hello/", response_class=JSONResponse)
    async def hello_world(request: Request):
        """
        Returns a Hello World message with timestamp
        """
        return {
            "message": "Hello, World!",
            "framework": "FastAPI",
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path,
        }

    # Run the app
    print("Starting FastAPI server at http://127.0.0.1:8000/")
    print("Documentation available at http://127.0.0.1:8000/docs")
    print("Press CTRL+C to quit")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) < 2 or sys.argv[1] not in ['django', 'fastapi']:
        print("Usage: python exercise_13.py [django|fastapi]")
        print("  django  - Run the Django Hello World app")
        print("  fastapi - Run the FastAPI Hello World app")
        sys.exit(1)
    
    # Run the selected framework
    if sys.argv[1] == 'django':
        create_django_project()
    else:
        create_fastapi_app()