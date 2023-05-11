from django.contrib import admin
from .models import Blog, BlogPost, Comment, Share

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'created_by','created_at']

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'blog', 'created_by','created_at']
    list_filter = ['blog', 'title','created_by']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'post', 'created_by','created_at']

class ShareAdmin(admin.ModelAdmin):
    list_display = ['social_media', 'post', 'created_by','created_at']

# admin.site.site_header = "UMSRA Admin"
# admin.site.site_title = "UMSRA Admin Portal"
# admin.site.index_title = "Welcome to UMSRA Researcher Portal"

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Share, ShareAdmin)