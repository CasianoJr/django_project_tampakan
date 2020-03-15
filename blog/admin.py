from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title',
                    'slug', 'timestamp']
    list_filter = ['title']
    list_editable = ['slug']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
