from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _
from news.models import Category, Post


# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )


def delete_post(modeladmin, request, queryset):
    # queryset.delete(id=request.id)
    # delete_post.short_description = 'Удаление публикации'
    pass


class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Post._meta.get_fields()]
    list_filter = ('title', 'category', 'type_post', 'author', 'rating')
    search_fields = ('title', 'category__name', 'type_post', 'author__full_name')
    actions = [delete_post]


# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Category)
admin.site.register(Post)
