from django.contrib import admin

from .models import Blog, BlogPost, BlogPostCategory, BlogPostCollaborator

admin.site.register(Blog)
admin.site.register(BlogPost)
admin.site.register(BlogPostCategory)
admin.site.register(BlogPostCollaborator)
