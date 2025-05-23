# Challenge 9: Testing Django REST API with pytest

from django.db import models
from django.utils import timezone
from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

# Django Model
class BlogPost(models.Model):
    """Blog post model with basic fields and methods"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.title
    
    def publish(self):
        """Publish the blog post"""
        self.published_at = timezone.now()
        self.is_published = True
        self.save()
    
    def get_tags_as_list(self):
        """Return tags as a list"""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',')]

# REST Framework Serializer
class BlogPostSerializer(serializers.ModelSerializer):
    tag_list = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'created_at', 
                 'updated_at', 'published_at', 'is_published', 'tags', 'tag_list']
    
    def get_tag_list(self, obj):
        return obj.get_tags_as_list()

# REST Framework ViewSet
class BlogPostViewSet(viewsets.ModelViewSet):
    """API viewset for BlogPost model"""
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Allow filtering by published status and author"""
        queryset = BlogPost.objects.all().order_by('-created_at')
        
        # Filter by published status if specified
        is_published = self.request.query_params.get('published', None)
        if is_published is not None:
            is_published = is_published.lower() == 'true'
            queryset = queryset.filter(is_published=is_published)
        
        # Filter by author if specified
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author=author)
            
        # Filter by tag if specified
        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__contains=tag)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Custom action to publish a blog post"""
        post = self.get_object()
        post.publish()
        return Response({'status': 'post published'})

"""
To test this API, create a file named 'test_challenge_9.py' with the following content:

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
import datetime

# Import the model and serializer
from challenge_9 import BlogPost, BlogPostSerializer

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_blog_posts():
    # Create several blog posts for testing
    posts = [
        BlogPost.objects.create(
            title="Published Post 1",
            content="Content for published post 1",
            author="Author1",
            is_published=True,
            published_at=timezone.now() - datetime.timedelta(days=1),
            tags="python,django,testing"
        ),
        BlogPost.objects.create(
            title="Published Post 2",
            content="Content for published post 2",
            author="Author2",
            is_published=True,
            published_at=timezone.now() - datetime.timedelta(days=2),
            tags="python,api"
        ),
        BlogPost.objects.create(
            title="Unpublished Post 1",
            content="Content for unpublished post",
            author="Author1",
            tags="draft,python"
        ),
        BlogPost.objects.create(
            title="Unpublished Post 2",
            content="Another unpublished post",
            author="Author3",
            tags=""
        ),
    ]
    return posts

@pytest.mark.django_db
class TestBlogPostAPI:
    def test_list_all_posts(self, api_client, sample_blog_posts):
        url = reverse('blogpost-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(sample_blog_posts)
    
    @pytest.mark.parametrize('published,expected_count', [
        ('true', 2),   # 2 published posts
        ('false', 2),  # 2 unpublished posts
    ])
    def test_filter_by_published(self, api_client, sample_blog_posts, published, expected_count):
        url = f"{reverse('blogpost-list')}?published={published}"
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == expected_count
    
    @pytest.mark.parametrize('author,expected_count', [
        ('Author1', 2),  # Author1 has 2 posts
        ('Author2', 1),  # Author2 has 1 post
        ('Author3', 1),  # Author3 has 1 post
        ('Unknown', 0),  # Unknown author has 0 posts
    ])
    def test_filter_by_author(self, api_client, sample_blog_posts, author, expected_count):
        url = f"{reverse('blogpost-list')}?author={author}"
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == expected_count
    
    @pytest.mark.parametrize('tag,expected_count', [
        ('python', 3),  # 3 posts with 'python' tag
        ('django', 1),  # 1 post with 'django' tag
        ('api', 1),     # 1 post with 'api' tag
        ('draft', 1),   # 1 post with 'draft' tag
        ('unknown', 0), # 0 posts with 'unknown' tag
    ])
    def test_filter_by_tag(self, api_client, sample_blog_posts, tag, expected_count):
        url = f"{reverse('blogpost-list')}?tag={tag}"
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == expected_count
    
    def test_create_blog_post(self, api_client):
        url = reverse('blogpost-list')
        data = {
            'title': 'New Test Post',
            'content': 'Content for new test post',
            'author': 'Test Author',
            'tags': 'test,new,api'
        }
        
        # Simulate authenticated user (would need proper authentication in real project)
        api_client.force_authenticate(user=None)
        
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == data['title']
        assert response.data['tag_list'] == ['test', 'new', 'api']
    
    def test_retrieve_blog_post(self, api_client, sample_blog_posts):
        post = sample_blog_posts[0]  # Get the first post
        url = reverse('blogpost-detail', kwargs={'pk': post.id})
        
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == post.id
        assert response.data['title'] == post.title
    
    def test_update_blog_post(self, api_client, sample_blog_posts):
        post = sample_blog_posts[0]
        url = reverse('blogpost-detail', kwargs={'pk': post.id})
        data = {
            'title': 'Updated Title',
            'content': post.content,  # Keep the same content
            'author': post.author,    # Keep the same author
            'tags': 'updated,test'
        }
        
        # Simulate authenticated user
        api_client.force_authenticate(user=None)
        
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'
        assert response.data['tag_list'] == ['updated', 'test']
    
    def test_delete_blog_post(self, api_client, sample_blog_posts):
        post = sample_blog_posts[0]
        url = reverse('blogpost-detail', kwargs={'pk': post.id})
        
        # Simulate authenticated user
        api_client.force_authenticate(user=None)
        
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify the post was deleted
        get_response = api_client.get(url)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_publish_action(self, api_client, sample_blog_posts):
        post = sample_blog_posts[2]  # Get an unpublished post
        assert post.is_published is False
        
        url = reverse('blogpost-publish', kwargs={'pk': post.id})
        
        # Simulate authenticated user
        api_client.force_authenticate(user=None)
        
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        
        # Refresh the post from database
        post.refresh_from_db()
        assert post.is_published is True
        assert post.published_at is not None
"""

if __name__ == "__main__":
    print("This module contains Django models, serializers, and viewsets for a REST API.")
    print("To test it, you need a Django project with Django REST Framework installed.")
    print("The tests require pytest and pytest-django configured correctly.")