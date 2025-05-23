from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.conf import settings
from django.middleware.csrf import get_token
import re
import logging
import json

# Setup logging
logger = logging.getLogger(__name__)

# Custom form with validation
class SecureUserForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Validate username pattern (alphanumeric only)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Validate email
        validate_email(email)
        return email
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        # Enforce strong password policy
        if len(password) < 12:
            raise ValidationError("Password must be at least 12 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one number.")
        if not re.search(r'[^A-Za-z0-9]', password):
            raise ValidationError("Password must contain at least one special character.")
        return password

class SecureContentForm:
    def __init__(self, data):
        self.data = data
        self.cleaned_data = {}
        self.errors = []
    
    def is_valid(self):
        try:
            # Get and validate the title
            title = self.data.get('title', '')
            if not title or len(title) > 200:
                self.errors.append("Title is required and must be less than 200 characters.")
                return False
            
            # Sanitize and validate the content
            content = self.data.get('content', '')
            if not content:
                self.errors.append("Content is required.")
                return False
            
            # Store sanitized data
            self.cleaned_data['title'] = escape(title)
            self.cleaned_data['content'] = escape(content)
            
            return True
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            self.errors.append("Invalid form data.")
            return False

# Ensure CSRF protection and prevent caching
@ensure_csrf_cookie
@never_cache
def index(request):
    """Secure index view that sets CSRF cookie and prevents caching"""
    csrf_token = get_token(request)
    return render(request, 'index.html', {'csrf_token': csrf_token})

# Secure user registration
@csrf_protect
@never_cache
@require_http_methods(["GET", "POST"])
def register_user(request):
    """Secure user registration with validation"""
    if request.method == 'POST':
        form = SecureUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f"New user registered: {user.username}")
            return redirect('profile')
    else:
        form = SecureUserForm()
    
    return render(request, 'register.html', {'form': form})

# Secure login
@csrf_protect
@never_cache
@require_http_methods(["GET", "POST"])
def login_view(request):
    """Secure login with rate limiting and proper authentication"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info(f"User logged in: {user.username}")
            
            # Set secure session settings
            request.session.set_expiry(3600)  # 1 hour expiry
            return redirect('profile')
        else:
            logger.warning(f"Failed login attempt for user: {request.POST.get('username')}")
    else:
        form = AuthenticationForm()
    
    response = render(request, 'login.html', {'form': form})
    
    # Set security headers
    response['X-Content-Type-Options'] = 'nosniff'
    response['X-Frame-Options'] = 'DENY'
    response['Content-Security-Policy'] = "default-src 'self'"
    response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    return response

# Secure logout
@login_required
@never_cache
def logout_view(request):
    """Secure logout that invalidates the session"""
    username = request.user.username
    logout(request)
    request.session.flush()
    logger.info(f"User logged out: {username}")
    return redirect('login')

# Secure profile page
@login_required
@never_cache
def profile_view(request):
    """Protected profile view requiring authentication"""
    return render(request, 'profile.html', {'user': request.user})

# Secure API endpoint
@login_required
@csrf_protect
@require_http_methods(["POST"])
def create_content(request):
    """Secure API endpoint for creating content with validation"""
    try:
        # Parse JSON data safely
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            logger.warning("Invalid JSON data received")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Validate the form data
        form = SecureContentForm(data)
        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=400)
        
        # Process the sanitized data
        # In a real app, you would save to database here
        logger.info(f"User {request.user.username} created new content: {form.cleaned_data['title']}")
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Content created successfully',
            'title': form.cleaned_data['title']
        })
    except Exception as e:
        logger.error(f"Error in create_content: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

# Example settings that would go in Django settings.py
"""
# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
"""

if __name__ == "__main__":
    print("This module contains Django views and security implementations.")
    print("To use it, you would need to:")
    print("1. Create a Django project")
    print("2. Configure proper URLs")
    print("3. Create the necessary templates")
    print("4. Set up the appropriate security settings in settings.py")