from django.contrib import admin
from rango.models import UserProfile1, Album, Review, Vote, Genre, FavoriteGenre, FavoriteAlbum, GenreAlbum

admin.site.register(UserProfile1)
admin.site.register(Album)
admin.site.register(Review)
admin.site.register(Vote)
admin.site.register(Genre)
admin.site.register(FavoriteGenre)
admin.site.register(FavoriteAlbum)
admin.site.register(GenreAlbum)