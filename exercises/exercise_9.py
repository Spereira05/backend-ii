# Exercise 9: Django model testing with pytest

from django.db import models
from django.utils import timezone
import datetime

class BlogPost(models.Model):
    """
    A simple Django model representing a blog post.
    
    This model demonstrates basic Django model functionality
    with custom methods that can be tested with pytest.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def publish(self):
        """Publish the blog post by setting published date and status"""
        self.published_at = timezone.now()
        self.is_published = True
        self.save()
    
    def unpublish(self):
        """Unpublish the blog post"""
        self.is_published = False
        self.save()
    
    def increment_views(self):
        """Increment the view count"""
        self.view_count += 1
        self.save()
    
    def is_recently_published(self):
        """Check if the post was published within the last 7 days"""
        if not self.published_at:
            return False
        return self.published_at >= timezone.now() - datetime.timedelta(days=7)
    
    def get_summary(self, chars=100):
        """Return a summary of the post content"""
        if len(self.content) <= chars:
            return self.content
        return self.content[:chars] + "..."

"""
To test this model, create a file named 'test_exercise_9.py' with the following content:

import pytest
from django.utils import timezone
import datetime
from unittest.mock import patch

# You'll need to install pytest-django and configure it properly
pytestmark = pytest.mark.django_db

# Import the model
from exercise_9 import BlogPost

class TestBlogPost:
    def test_create_blog_post(self):
        # Create a blog post
        post = BlogPost.objects.create(
            title="Test Post",
            content="This is a test post content.",
            author="Test Author"
        )
        # Check that it was created properly
        assert post.title == "Test Post"
        assert post.content == "This is a test post content."
        assert post.author == "Test Author"
        assert post.is_published is False
        assert post.view_count == 0
        assert post.published_at is None
    
    def test_publish_blog_post(self):
        # Create a blog post
        post = BlogPost.objects.create(
            title="Test Post",
            content="Content",
            author="Author"
        )
        # Publish it
        post.publish()
        
        # Check that it was published
        assert post.is_published is True
        assert post.published_at is not None
    
    def test_unpublish_blog_post(self):
        # Create a published blog post
        post = BlogPost.objects.create(
            title="Test Post",
            content="Content",
            author="Author",
            is_published=True,
            published_at=timezone.now()
        )
        
        # Unpublish it
        post.unpublish()
        
        # Check that it was unpublished
        assert post.is_published is False
    
    def test_increment_views(self):
        # Create a blog post
        post = BlogPost.objects.create(
            title="Test Post",
            content="Content",
            author="Author"
        )
        
        # Increment views multiple times
        initial_views = post.view_count
        post.increment_views()
        post.increment_views()
        post.increment_views()
        
        # Check that view count was incremented
        assert post.view_count == initial_views + 3
    
    def test_is_recently_published(self):
        # Create a blog post published now
        recent_post = BlogPost.objects.create(
            title="Recent Post",
            content="Content",
            author="Author",
            is_published=True,
            published_at=timezone.now()
        )
        
        # Create a blog post published 10 days ago
        old_post = BlogPost.objects.create(
            title="Old Post",
            content="Content",
            author="Author",
            is_published=True,
            published_at=timezone.now() - datetime.timedelta(days=10)
        )
        
        # Create an unpublished post
        unpublished_post = BlogPost.objects.create(
            title="Unpublished Post",
            content="Content",
            author="Author"
        )
        
        # Check the results
        assert recent_post.is_recently_published() is True
        assert old_post.is_recently_published() is False
        assert unpublished_post.is_recently_published() is False
    
    def test_get_summary(self):
        # Create a blog post with long content
        long_content = "This is a very long content that needs to be summarized properly for display in list views or previews."
        post = BlogPost.objects.create(
            title="Test Post",
            content=long_content,
            author="Author"
        )
        
        # Test with default length
        default_summary = post.get_summary()
        assert len(default_summary) <= 103  # 100 chars + "..."
        assert default_summary.endswith("...")
        
        # Test with custom length
        custom_summary = post.get_summary(chars=20)
        assert len(custom_summary) <= 23  # 20 chars + "..."
        assert custom_summary.endswith("...")
        
        # Test with content shorter than summary length
        short_post = BlogPost.objects.create(
            title="Short Post",
            content="Short content",
            author="Author"
        )
        short_summary = short_post.get_summary(chars=50)
        assert short_summary == "Short content"
        assert not short_summary.endswith("...")
"""

if __name__ == "__main__":
    print("This is a Django model that would normally be used within a Django project.")
    print("To test this model, you would need to:")
    print("1. Create a Django project")
    print("2. Add this model to an app's models.py")
    print("3. Run migrations")
    print("4. Use pytest with pytest-django to run the tests")