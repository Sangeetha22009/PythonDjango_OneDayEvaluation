from django.contrib import admin
from .models import Blog, BlogPost, Comment, Share

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'created_by','created_at']

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'blog', 'created_by','created_at']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'post', 'created_by','created_at']

class ShareAdmin(admin.ModelAdmin):
    list_display = ['social_media', 'post', 'created_by','created_at']

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Share, ShareAdmin)