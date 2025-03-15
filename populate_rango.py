import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
import datetime
from django.core.files import File
from pathlib import Path

django.setup()
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
    
    #users contain (username, password, bio, email)
    #      !!!!!!!!! BAD EXAMPLE OF WRITING PATHS - NOT COMPATIBLE WITH ALL OS'S !!!!!!!!! :
    # users = [['Dr  bob', 'drBobsSecretPassword', 'hey im dr bob a profesional doctor man', 'doctorBob@Medical.com', r'profilePicsForPopulating\drBob.jpg'], ['Paddy Mcguinness', 'wolfeTones1954',
    #  'Paddy Mcguinness acomplished cow tipper', 'paddymcguinnes@country.com', r'profilePicsForPopulating\paddyMcG.jpg']]
    
    # how it should be done: !

    users = [
        ['Dr  bob', 'drBobsSecretPassword', 'hey im dr bob a profesional doctor man', 
         'doctorBob@Medical.com', os.path.join('profilePicsForPopulating', 'drBob.jpg')],
        ['Paddy Mcguinness', 'wolfeTones1954', 'Paddy Mcguinness acomplished cow tipper', 
         'paddymcguinnes@country.com', os.path.join('profilePicsForPopulating', 'paddyMcG.jpg')]
    ]
    

   
    #      !!!!!!!!! BAD EXAMPLE OF WRITING PATHS - NOT COMPATIBLE WITH ALL OS'S !!!!!!!!! :
    # albums contain name, artist and relsease date
    # albums = [["Parklife", "Blur", "1994", r"albumCoversForPopulating\BlurParklife.jpg" ],[" Straight From The Heart", "Ann Peebles", "1972", r"albumCoversForPopulating/mrBeanAlbum.jpg"]]


    # how it should be done: 
    albums = [
        ["Parklife", "Blur", "1994", os.path.join('albumCoversForPopulating', 'BlurParklife.jpg')],
        [" Straight From The Heart", "Ann Peebles", "1972", os.path.join('albumCoversForPopulating', 'mrBeanAlbum.jpg')]
    ]

    #       
    #filelocation parklife = "C:\Users\Finn McInroy\Downloads\BlurParklife.jpg".   -  no, use ospathjoin
    #filelocation Straight from the heart = "C:\Users\Finn McInroy\Downloads\mrBeanAlbum2.jpg".  - no, use ospathjoin
 


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

    
    for a in albums:
        print("codeRan")
        a = add_album(*a)
       
        
        

    

    """

    for i, image_file in enumerate(image_files):
        # Full path to the image file
        image_path = os.path.join(image_dir, image_file)

        # Open the image file
        with open(image_path, 'rb') as f:
            # Create a Django File object
            django_file = File(f)

            # Create a model instance
            album = Album(
                title=f'Album {i + 1}',
                artist=f'Artist {i + 1}',
            )

            # Assign the image to the ImageField
            album.cover_image.save(image_file, django_file, save=True)

            print(f'Created {album.title} with image {image_file}')


    """

    for r in reviews:
        r = add_reveiw(r[0],r[1],r[2])

    for v in votes:
        v = add_vote(v[0], v[1], v[2])

    for g in genre:
        g = add_genre(g[0],g[1])

    for fa in favoriteAlbums:
        fa = add_favoriteAlbum(fa[0], fa[1])

    #

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

def add_user(username, password, bio, email, profilePicPath):
    try:
        with open(profilePicPath, 'rb') as f:
            djangoFile = File(f)
            
            user1, created = UserProfile1.objects.get_or_create(
                username=username,
                defaults={'email': email, 'bio': bio, 'password': password}
            )
            
            user1.profilePicture.save(os.path.basename(profilePicPath), djangoFile, save=True)
        return user1
    except FileNotFoundError:
        print(f"Warning: Profile picture file not found at {profilePicPath}. Creating user without image.")
        user1, created = UserProfile1.objects.get_or_create(
            username=username,
            defaults={'email': email, 'bio': bio, 'password': password}
        )
        return user1

def add_album(albumName, artist, releaseYear, albumCoverPath):
    try:
        with open(albumCoverPath, 'rb') as f:
            djangoFile = File(f)
            
            album, created = Album.objects.get_or_create(
                albumName=albumName,
                defaults={'artist': artist, 'releaseDate': releaseYear}
            )
                
            album.albumCover.save(os.path.basename(albumCoverPath), djangoFile, save=True)
        return album
    except FileNotFoundError:
        print(f"Warning: Album cover file not found at {albumCoverPath}. Creating album without image.")
        album, created = Album.objects.get_or_create(
            albumName=albumName,
            defaults={'artist': artist, 'releaseDate': releaseYear}
        )
        return album

def add_reveiw(userID, albumID, reveiwText):

    user = UserProfile1.objects.get(pk=userID)
    album = Album.objects.get(pk=albumID)



    review, created = Review.objects.get_or_create(
        userID=user,
        albumID=album,
        
        defaults={'reviewText': reveiwText}
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