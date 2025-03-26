import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
import datetime
from django.core.files import File
from pathlib import Path

django.setup()
from django.contrib.auth.models import User
from rango.models import Category, Page, UserProfile1, Album, Review, Vote, Genre, FavoriteAlbum

def populate():
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url':'http://docs.python.org/3/tutorial/',
         'views': 884,},
        {'title':'How to Think like a Computer Scientist',
         'url':'http://www.greenteapress.com/thinkpython/',
         'views': 356},
        {'title':'Learn Python in 10 Minutes',
         'url':'http://www.korokithakis.net/tutorials/python/',
         'views': 458} ]
    
    django_pages = [
        {'title':'Official Django Tutorial',
         'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
         'views': 21},
        {'title':'Django Rocks',
         'url':'http://www.djangorocks.com/',
         'views': 3247},
        {'title':'How to Tango with Django',
         'url':'http://www.tangowithdjango.com/',
         'views': 6943} ]
    
    other_pages = [
        {'title':'Bottle',
         'url':'http://bottlepy.org/docs/dev/',
         'views': 54},
        {'title':'Flask',
         'url':'http://flask.pocoo.org',
         'views': 57} ]
    
    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16} }

    users = [
        ['Dr bob', 'drBobsSecretPassword', 'hey im dr bob a profesional doctor man', 
         'doctorBob@Medical.com', os.path.join('profilePicsForPopulating', 'drBob.jpg')],
        ['Paddy Mcguinness', 'wolfeTones1954', 'Paddy Mcguinness acomplished cow tipper', 
         'paddymcguinnes@country.com', os.path.join('profilePicsForPopulating', 'paddyMcG.jpg')]
    ]
 
    albums = [
        ["Parklife", "Blur", "1994", os.path.join('albumCoversForPopulating', 'BlurParklife.jpg')],
        [" Straight From The Heart", "Ann Peebles", "1972", os.path.join('albumCoversForPopulating', 'mrBeanAlbum.jpg')]
    ]

    albums = [
    ["Parklife", "Blur", "1994", os.path.join('albumCoversForPopulating', 'BlurParklife.jpg'), 30],  # Positive score
    ["Straight From The Heart", "Ann Peebles", "1972", os.path.join('albumCoversForPopulating', 'mrBeanAlbum.jpg'), -23]  # Negative score
]

    #reveiws contain UserID, AlbumID, reviewText

    reviews = [["1","1", "this is so bad turn it off!!! turn it offff!!!"],["1","2", "this is so good turn it up bai"]]

    #votes contain UserID AlbumID and votetype(either 1 for yes or 0 for no)

    votes = [["1","1","0"], ["1","2","1"]]

    #genre contains name and description

    genre = [["Irish traditional","Irish folk music often using traditional instruments"],["Soul","idk how to explain"]]

    #favoriteAlbum contains date added UserID and AlbumID but date added is made automaticaly 

    favoriteAlbums = [["1","2"]]
    
    
    
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], views=p['views'])
    
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

    for u in users:
        u = add_user(*u)

    
    # Create albums
    for a in albums:
        add_album(*a)  # This will now pass all parameters including score
       

    for r in reviews:
        r = add_review(r[0],r[1],r[2])

    for v in votes:
        v = add_vote(v[0], v[1], v[2])

    for g in genre:
        g = add_genre(g[0],g[1])

    for fa in favoriteAlbums:
        fa = add_favoriteAlbum(fa[0], fa[1])

    # Create users and store their IDs
    users_ids = []
    for u in users:
        user_profile = add_user(*u)
        if user_profile:
            users_ids.append(user_profile.id)

    # # First album - lots of upvotes (positive score)
    # for i in range(35):  # 35 upvotes
    #     if users_ids:
    #         add_vote(random.choice(users_ids), 1, 'up')
        
    # for i in range(5):  # 5 downvotes
    #     if users_ids:
    #         add_vote(random.choice(users_ids), 1, 'down')
        
    # # Second album - lots of downvotes (negative score)
    # for i in range(8):  # 8 upvotes
    #     if users_ids:
    #         add_vote(random.choice(users_ids), 2, 'up')
        
    # for i in range(31):  # 31 downvotes
    #     if users_ids:
    #         add_vote(random.choice(users_ids), 2, 'down')

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

def add_user(username, password, bio, email, profilePicPath=None):
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        # Get existing user
        user = User.objects.get(username=username)
        
        # Check if profile exists
        try:
            user_profile = UserProfile1.objects.get(user=user)
        except UserProfile1.DoesNotExist:
            # Create profile if it doesn't exist
            user_profile = UserProfile1.objects.create(
                user=user,
                bio=bio
            )
        
        return user_profile
    
    # Create new user if doesn't exist
    try:
        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create UserProfile1
        user_profile = UserProfile1.objects.create(
            user=user,
            bio=bio
        )
        
        # Add profile picture if path provided
        if profilePicPath:
            try:
                with open(profilePicPath, 'rb') as f:
                    django_file = File(f)
                    user_profile.profilePicture.save(
                        os.path.basename(profilePicPath), 
                        django_file, 
                        save=True
                    )
            except FileNotFoundError:
                print(f"Warning: Profile picture file not found at {profilePicPath}")
                
        return user_profile
    
    except Exception as e:
        print(f"Error creating user {username}: {e}")
        return None

# def add_album(albumName, artist, releaseYear, albumCoverPath):
#     try:
#         with open(albumCoverPath, 'rb') as f:
#             djangoFile = File(f)
            
#             album, created = Album.objects.get_or_create(
#                 albumName=albumName,
#                 defaults={'artist': artist, 'releaseDate': releaseYear}
#             )
                
#             album.albumCover.save(os.path.basename(albumCoverPath), djangoFile, save=True)
#         return album
#     except FileNotFoundError:
#         print(f"Warning: Album cover file not found at {albumCoverPath}. Creating album without image.")
#         album, created = Album.objects.get_or_create(
#             albumName=albumName,
#             defaults={'artist': artist, 'releaseDate': releaseYear}
#         )
#         return album

def add_album(albumName, artist, releaseYear, albumCoverPath, score=0):
    try:
        # First, check if album already exists
        album, created = Album.objects.get_or_create(
            albumName=albumName,
            defaults={
                'artist': artist,
                'releaseDate': releaseYear,
                'score': score  # Use the score parameter
            }
        )
        
        # If album already exists, update its fields
        if not created:
            album.artist = artist
            album.releaseDate = releaseYear
            album.score = score  # Update the score
            album.save()
        
        # Try to add the cover image if a path is provided
        if os.path.exists(albumCoverPath):
            with open(albumCoverPath, 'rb') as f:
                django_file = File(f)
                album.albumCover.save(
                    os.path.basename(albumCoverPath),
                    django_file,
                    save=True
                )
        else:
            print(f"Warning: Album cover file not found at {albumCoverPath}")
            
        return album
    except Exception as e:
        print(f"Error creating album {albumName}: {e}")
        return None

def add_review(userID, albumID, reviewText):

    user = UserProfile1.objects.get(pk=userID)
    album = Album.objects.get(pk=albumID)



    review, created = Review.objects.get_or_create(
        userID=user,
        albumID=album,
        
        defaults={'reviewText': reviewText}
    )

    return review

def add_vote(userID, albumID, voteType):

    user = UserProfile1.objects.get(pk=userID)
    album = Album.objects.get(pk=albumID)



    review, created = Vote.objects.get_or_create(
        userID=user,
        albumID=album,
        
        defaults={'voteType': voteType}
    )

    return review

def add_genre(genreName , genreDescription):

    



    genre, created = Genre.objects.get_or_create(
        genreName=genreName,
        genreDescription=genreDescription,
        
        
    )

    return genre

def add_vote(user_id, album_id, vote_type):
    user = UserProfile1.objects.get(pk=user_id)
    album = Album.objects.get(pk=album_id)
    
    vote, created = Vote.objects.get_or_create(
        userID=user,
        albumID=album,
        defaults={'voteType': vote_type}
    )
    
    return vote

def add_favoriteAlbum(userID , albumID):

    user = UserProfile1.objects.get(pk=userID)
    album = Album.objects.get(pk=albumID)




    genre, created = FavoriteAlbum.objects.get_or_create(
        userID=user,
        albumID=album,

        defaults={'dateAdded': datetime.datetime.now()}
        
        
    )

    return genre

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()