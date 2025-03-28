from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rango.models import Album, Review, UserProfile1, FavoriteAlbum, FavoriteGenre, Vote, Genre
from rango.forms import UserForm, UserProfileForm, ReviewForm, AlbumForm, EditProfileForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
from os.path import join
from django.conf import settings
from django.db import IntegrityError

def index(request):
    top_albums = Album.objects.all().order_by('-score')[:4]
    lowest_rated_albums = Album.objects.all().order_by('score')[:4]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['albums'] = top_albums
    context_dict['bottom_albums'] = lowest_rated_albums

    visitor_cookie_handler(request)

    return render(request, 'rango/index.html', context=context_dict)

def add_category(request):
    pass

# def all_albums(request):
#     context_dict = {}
#     album_list = Album.objects.order_by('albumName')
#     context_dict['albums'] = album_list
#     return render(request, 'rango/all_albums.html', context=context_dict)

def all_albums(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    genre_filter = request.GET.get('genre', '')

    albums = Album.objects.all()
    
    if query:
        # Filter albums by name or artist (case-insensitive)
        albums = albums.filter(albumName__icontains=query) | Album.objects.filter(artist__icontains=query)

    if genre_filter:
        albums = albums.filter(genre_id=genre_filter)

    genres = Genre.objects.all()

    context_dict = {
        'albums': albums,
        'query': query,
        'genres': genres,
        'genre_filter': genre_filter
    }
    
    return render(request, 'rango/all_albums.html', context=context_dict)

def album(request, album_name_slug):
    context_dict = {}
    album = get_object_or_404(Album, slug=album_name_slug)
    reviews = Review.objects.filter(albumID=album)
    context_dict['album'] = album
    context_dict['reviews'] = reviews
    return render(request, 'rango/album.html', context=context_dict)

def about(request):
    context_dict = {}
    return render(request, 'rango/about.html', context=context_dict)

def reviews(request):
    review_list = Review.objects.order_by("userID")
    context_dict = {}
    context_dict['reviews'] = review_list

    return render(request, 'rango/reviews.html', context=context_dict)

def user_profile(request, user_id):
    context_dict = {}

    try:
        profile_owner = UserProfile1.objects.get(pk=user_id)

    except UserProfile1.DoesNotExist:
        context_dict['profile_owner'] = None
        context_dict['reviews'] = None
        context_dict['fav_album'] = None
        context_dict['fav_genre'] = None
    else:
        try:
            reviews = Review.objects.filter(userID=user_id)
        except Review.DoesNotExist:
            reviews = None

        try:
            fav_albums = FavoriteAlbum.objects.filter(userID=user_id).order_by('-dateAdded')
        except FavoriteAlbum.DoesNotExist:
            fav_albums = None

        try:
            fav_genres = FavoriteGenre.objects.filter(userID=user_id).order_by('-dateAdded')
        except FavoriteGenre.DoesNotExist:
            fav_genres = None

        context_dict['profile_owner'] = profile_owner
        context_dict['reviews'] = reviews
        context_dict['fav_albums'] = fav_albums
        context_dict['fav_genres'] = fav_genres

    return render(request, 'rango/user_profile.html', context=context_dict)

@login_required
def edit_profile(request):
    context_dict = {}
    context_dict['form'] = EditProfileForm()
    context_dict['albums'] = Album.objects.all()
    context_dict['genres'] = Genre.objects.all()

    if request.method == 'POST':
        user = request.user
        user_profile = UserProfile1.objects.get(user=user)

        form = EditProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            new_bio = request.POST.get('bio')
            new_fav_album_id = request.POST.get('fav_album')
            new_fav_genre_id = request.POST.get('fav_genre')

            if 'profilePicture' in request.FILES:
                try:
                    old_path = os.path.join(settings.MEDIA_ROOT, "profilePicture", str(user_profile.profilePicture))
                    os.remove(old_path)
                except Exception as e:
                    print(e)
                user_profile.profilePicture = request.FILES['profilePicture']
                user_profile.save()

            if new_bio:
                user_profile.bio = new_bio
                user_profile.save()

            if new_fav_album_id:
                album = Album.objects.get(pk=new_fav_album_id)
                FavoriteAlbum.objects.get_or_create(userID=user_profile, albumID=album, dateAdded = datetime.now()) 

            if new_fav_genre_id:
                genre = Genre.objects.get(pk=new_fav_genre_id)
                FavoriteGenre.objects.get_or_create(userID=user_profile, genreID=genre, dateAdded = datetime.now())
                    
            return redirect(reverse('rango:user_profile', args=[user_profile.pk]))
        
    return render(request, 'rango/edit_profile.html', context=context_dict)

@login_required
def add_review(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    user_profile = get_object_or_404(UserProfile1, user=request.user)
    form = ReviewForm()

    if Review.objects.filter(albumID=album, userID=user_profile).exists():
        messages.info(request, "You have already written a review for this album.")
        return redirect('rango:album', album_name_slug=album.slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.userID = user_profile
            review.albumID = album 
            review.save()

            return redirect('rango:album', album_name_slug=album.slug)
        else:
            print(form.errors)

    return render(request, 'rango/add_review.html', {'form':form, 'album': album})

@login_required
def add_album(request):
    context_dict = {}
    context_dict['form'] = AlbumForm()
    context_dict['genres'] = Genre.objects.all()

    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                album = form.save(commit=False)

                if request.POST['genre']:
                    genre_id = request.POST['genre']
                    genre = Genre.objects.get(pk=genre_id)
                    album.genre = genre
                
                album.save()
            except IntegrityError:
                context_dict['album_exists'] = True
                return render(request, 'rango/add_album.html', context=context_dict)
            
            return redirect('rango:all_albums')
        
    return render(request, 'rango/add_album.html', context=context_dict)


@login_required
def vote_album(request):
    if request.method == 'POST':
        album_id = request.POST.get('album_id')
        vote_type = request.POST.get('vote_type')
        
        album = get_object_or_404(Album, id=album_id)
        user_profile = request.user.userprofile1
        
        if vote_type not in ['up', 'down']:
            return JsonResponse({'status': 'error', 'message': 'Invalid vote type'})
            
        # Check if user already voted
        try:
            vote = Vote.objects.get(userID=user_profile, albumID=album)
            
            # If same vote type, remove the vote (toggle)
            if vote.voteType == vote_type:
                if vote_type == 'up':
                    album.score -= 1
                else:
                    album.score += 1
                vote.delete()
                album.save()
                return JsonResponse({'status': 'success', 'action': 'removed', 'new_score': album.score})
                
            # Otherwise, change the vote
            old_vote = vote.voteType
            vote.voteType = vote_type
            vote.save()  # The score will be updated in the save method
            
            return JsonResponse({'status': 'success', 'action': 'changed', 'new_score': album.score})
            
        except Vote.DoesNotExist:
            # New vote
            vote = Vote.objects.create(
                userID=user_profile,
                albumID=album,
                voteType=vote_type
            )
            
            return JsonResponse({'status': 'success', 'action': 'added', 'new_score': album.score})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.profilePicture = request.FILES['picture']

            profile.save()

            registered = True
        else:

            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})

def user_login(request):
    context_dict = {}

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            context_dict['login_status'] = "Invalid login details provided"
            return render(request, 'rango/login.html', context=context_dict)
    else:
        return render(request, 'rango/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
    'last_visit',
    str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
    '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1

        request.session['last_visit'] = str(datetime.now())
    else:

        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits
