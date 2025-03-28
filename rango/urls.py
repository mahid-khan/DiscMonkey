from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('all_albums/', views.all_albums, name='all_albums'),
    path('album/<slug:album_name_slug>/', views.album, name='album'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('add_review/<int:album_id>/', views.add_review, name='add_review'),
    path('vote/', views.vote_album, name='vote_album'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('add_album/', views.add_album, name='add_album'),
]

