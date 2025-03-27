import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
import datetime
from django.core.files import File
from pathlib import Path

django.setup()
from django.contrib.auth.models import User
from rango.models import UserProfile1, Album, Review, Vote, Genre, FavoriteAlbum

def populate():

    users = [
        ['Dr bob', 'drBobsSecretPassword', 'hey im dr bob a profesional doctor man', 
         'doctorBob@Medical.com', os.path.join('profilePicsForPopulating', 'drBob.jpg')],
        ['Paddy Mcguinness', 'wolfeTones1954', 'Paddy Mcguinness acomplished cow tipper', 
         'paddymcguinnes@country.com', os.path.join('profilePicsForPopulating', 'paddyMcG.jpg')]
    ]

    albums = [
        ["Parklife", "Blur", "1994", os.path.join('albumCoversForPopulating', 'BlurParklife.jpg'), 30, "Rock"],
        ["Straight From The Heart", "Ann Peebles", "1972", os.path.join('albumCoversForPopulating', 'StraightFromTheHeart.jpg'), -23, "Blues"],
        ["Brothers In Arms", "Dire Straits", "1985", os.path.join('albumCoversForPopulating', 'BrothersInArms.jpg'), 20, "Pop"],
        ["Ege Bamyasi", "CAN", "1972", os.path.join('albumCoversForPopulating', 'EgeBamyasi.jpg'), 3, "Rock"],
        ["I Can Hear The Heart Beating As One", "Yo La Tengo", "1997", os.path.join('albumCoversForPopulating', 'ICanHearTheHeartBeatingAsOne.jpg'), 43, "Indie Rock"],
        ["If You're Feeling Sinister", "Belle and Sebastian", "1996", os.path.join('albumCoversForPopulating', 'IfYoureFeelingSinister.jpg'), 62, "Indie Pop"],
        ["The Freewheelin' Bob Dylan", "Bob Dylan", "1963", os.path.join('albumCoversForPopulating', 'TheFreeWheelinBobDylan.jpg'), 100, "Folk"],
        ["Parallel Lines", "Blondie", "1979", os.path.join('albumCoversForPopulating', 'ParallelLines.jpg'), -4, "Rock"],
        ["Foxbase Alpha", "Saint Etienne", "1991", os.path.join('albumCoversForPopulating', 'FoxbaseAlpha.jpg'), 10, "Alternative Dance"],
        ["Beaucoup Fish", "Underworld", "1999", os.path.join('albumCoversForPopulating', 'BeaucoupFish.jpg'), 6, "Techno"],
        ["Debut", "Björk", "1993", os.path.join('albumCoversForPopulating', 'Debut.jpg'), 50, "Alternative Dance"]
    ]


    reviews = [
        ["1","1", "this is so bad turn it off!!! turn it offff!!!"],
        ["1","2", "this is so good turn it up bai"]
    ]

    #votes contain UserID AlbumID and votetype(either 1 for yes or 0 for no)

    votes = [
    ["1","1","0"],
    ["1","2","1"]
    ]

    #genre contains name and description

    genre = [
        ["Irish Traditional", "Irish folk music often using traditional instruments"],
        ["Jazz", "distinctively American style of music"],
        ["Pop", "Popular music with appealing melodies and catchy hooks"],
        ["Rap", "Rhythmic and rhyming speech set to music"],
        ["Hip-Hop", "Music genre that evolved from rap with urban influences"],
        ["Blues", "Music that is blue in colour"],
        ["Country", "American roots music telling heartfelt stories"],
        ["Metal", "Heavy and aggressive style of rock music"],
        ["Rock", "Broad genre featuring electric guitars and strong rhythms"],
        ["Dance", "Music designed to facilitate dancing"],
        ["Alternative Dance", "Alternative music with danceable beats"],
        ["EDM", "Electronic Dance Music with energetic beats"],
        ["Heavy Metal", "Intense and amplified style of rock"],
        ["International", "Diverse musical styles from around the world"],
        ["Techno", "Electronic dance music with repetitive beats"],
        ["Indie Pop", "A genre of alternative rock music with pop sensibilities"],
        ["Indie Rock", "A genre of alternative rock music with independent sensibilities"],
        ["Folk", "Traditional music passed down through generations"],
    ]

    favoriteAlbums = [["1","2"]] #favoriteAlbum contains date added UserID and AlbumID but date added is made automaticaly 

    for u in users:
        u = add_user(*u)

    for g in genre:
        g = add_genre(g[0],g[1])

    for a in albums:
        add_album(*a)
       
    for r in reviews:
        r = add_review(r[0],r[1],r[2])

    for v in votes:
        v = add_vote(v[0], v[1], v[2])

    for fa in favoriteAlbums:
        fa = add_favoriteAlbum(fa[0], fa[1])

    # Create users and store their IDs
    users_ids = []
    for u in users:
        user_profile = add_user(*u)
        if user_profile:
            users_ids.append(user_profile.id)


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




def add_album(albumName, artist, releaseYear, albumCoverPath, score=0, genreName=None):
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
        
        # Link album to genre if provided
        if genreName:
            try:
                genre = Genre.objects.get(genreName__iexact=genreName)
                album.genre = genre
                album.save()
            except Genre.DoesNotExist:
                print(f"Warning: Genre '{genreName}' not found for album {albumName}")
            
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

# def add_album(albumName, artist, releaseYear, albumCoverPath, score=0):
#     try:
#         # First, check if album already exists
#         album, created = Album.objects.get_or_create(
#             albumName=albumName,
#             defaults={
#                 'artist': artist,
#                 'releaseDate': releaseYear,
#                 'score': score  # Use the score parameter
#             }
#         )
        
#         # If album already exists, update its fields
#         if not created:
#             album.artist = artist
#             album.releaseDate = releaseYear
#             album.score = score  # Update the score
#             album.save()
        
#         # Try to add the cover image if a path is provided
#         if os.path.exists(albumCoverPath):
#             with open(albumCoverPath, 'rb') as f:
#                 django_file = File(f)
#                 album.albumCover.save(
#                     os.path.basename(albumCoverPath),
#                     django_file,
#                     save=True
#                 )
#         else:
#             print(f"Warning: Album cover file not found at {albumCoverPath}")
            
#         return album
#     except Exception as e:
#         print(f"Error creating album {albumName}: {e}")
#         return None

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()