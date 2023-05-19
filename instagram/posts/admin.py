from django.contrib import admin

from .models import Comment, HashTag, Post


admin.site.register(Comment)
admin.site.register(HashTag)


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('author', 'name', 'pub_date', 'edit_date')
    readonly_fields = ('pub_date', 'edit_date')
    inlines = [CommentInline, ]
    list_display = ['name', 'author', 'pub_date']
    list_filter = ['author']
    search_fields = ['author__username',]