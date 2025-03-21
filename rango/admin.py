from django.contrib import admin
from rango.models import Category, Page, UserProfile, UserProfile1, Album, Review, Vote, Genre, FavoriteGenre, FavoriteAlbum, GenreAlbum

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(UserProfile1)
admin.site.register(Album)
admin.site.register(Review)
admin.site.register(Vote)
admin.site.register(Genre)
admin.site.register(FavoriteGenre)
admin.site.register(FavoriteAlbum)
admin.site.register(GenreAlbum)