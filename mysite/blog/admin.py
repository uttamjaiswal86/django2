from django.contrib import admin
from .models import Post, Comment

# Register your models here.
#admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    #Je ham dikhaye(cloumn header)
    list_display = (
        'title', 'author','slug', 'publish', 'status'
    )
    #right side filteration 
    list_filter = ('status','created','publish','author')
    #on search from serach-bar
    search_fields = ('title','body')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    #navigation bar on date of publish
    date_hierarchy = 'publish'
    ordering = ('status','publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('name', 'email', 'post', 'created', 'active')
    list_filter=('active', 'created', 'updated')
    search_fields=('name','email','body')
    