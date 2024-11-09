from django.contrib import admin
from .models import Post, Category
from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('text',)

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category)