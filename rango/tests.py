from django.test import TestCase, override_settings
from django.urls import reverse
from rango.models import Album, User, UserProfile1, Review, Genre, FavoriteAlbum, FavoriteGenre, Vote
from django.core.files import File
from django.db import IntegrityError
import os
import datetime
import shutil

TEST_DIR = 'test_media'

def add_album(name, artist, year, score, genre_name):
    genre = Genre.objects.get(genreName=genre_name)
    album, created = Album.objects.get_or_create(albumName=name, artist=artist, releaseDate=year, score=score, genre=genre)
    return album

def add_user(username, password, bio, email, profile_pic_path):
    user = User.objects.create_user(username=username, email=email, password=password)
    user_profile, created = UserProfile1.objects.get_or_create(user=user, defaults={'bio': bio})
    
    with open(profile_pic_path, 'rb') as f:
        profile_pic = File(f)
        user_profile.profilePicture.save(os.path.basename(profile_pic_path), profile_pic, save=True)
    return user_profile

def add_review(username, album_name, text):
    user = User.objects.get(username=username)
    user_profile = UserProfile1.objects.get(user=user)
    album = Album.objects.get(albumName = album_name)
    review = Review.objects.get_or_create(userID=user_profile, albumID=album, reviewText=text)
    return review

def add_genre(name, description):
    genre = Genre.objects.get_or_create(genreName=name, genreDescription=description)
    return genre

def add_fav_album(username, album_name):
    user = User.objects.get(username=username)
    user_profile = UserProfile1.objects.get(user=user)
    album = Album.objects.get(albumName = album_name)
    fav_album = FavoriteAlbum.objects.get_or_create(userID=user_profile, albumID=album, defaults={'dateAdded': datetime.datetime.now()})
    return fav_album

def add_fav_genre(username, genre_name):
    user = User.objects.get(username=username)
    user_profile = UserProfile1.objects.get(user=user)
    genre = Genre.objects.get(genreName=genre_name)
    fav_genre = FavoriteGenre.objects.get_or_create(userID=user_profile, genreID=genre, defaults={'dateAdded': datetime.datetime.now()})
    return fav_genre

def populate_albums():
    add_album("AM", "Arctic Monkeys", "2013", 20, 'Indie rock')
    add_album("Demon Days", "Gorillaz", "2005", -20, 'Alternative rock')

def populate_users():
    add_user('Dr bob', 'drBobsSecretPassword', 'hey im dr bob a profesional doctor man', 'doctorBob@Medical.com', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'profilePicsForPopulating', 'drBob.jpg'))
    add_user('Paddy Mcguinness', 'wolfeTones1954', 'Paddy Mcguinness acomplished cow tipper', 'paddymcguinnes@country.com', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'profilePicsForPopulating', 'paddyMcG.jpg'))

def populate_reviews():
    add_review('Dr bob', 'AM', "this is so bad turn it off!!! turn it offff!!!")
    add_review('Paddy Mcguinness', 'Demon Days', "this is so good turn it up bai")

def populate_genres():
    add_genre('Indie rock', 'Rock that is indie')
    add_genre('Alternative rock', 'Rock that is alternative')

def populate_fav_albums():
    add_fav_album('Dr bob', 'AM')
    add_fav_album('Paddy Mcguinness', 'Demon Days')

def populate_fav_genres():
    add_fav_genre('Dr bob', 'Indie rock')
    add_fav_genre('Paddy Mcguinness', 'Alternative rock')


class ModelTests(TestCase):
    @override_settings(MEDIA_ROOT=(TEST_DIR))
    def setUp(self):
        populate_genres()
        populate_albums()
        populate_users()
        populate_reviews()

        user = User.objects.get(username='Dr bob')
        self.user_profile = UserProfile1.objects.get(user=user)
        self.album = Album.objects.get(albumName='AM')
        self.genre = Genre.objects.get(genreName='Indie rock')

    def test_review_uniqueness(self):
        """
        Checks that an IntegrityError is raised if the uniqueness constraints of the Review model are violated
        """
        
        self.assertRaises(IntegrityError, Review.objects.create, userID=self.user_profile, albumID=self.album, reviewText='I should not be able to add a second review')

    def test_fav_album_uniqueness(self):
        """
        Checks that an IntegrityError is raised if the uniqueness constraints of the FavoriteAlbum model are violated
        """

        populate_fav_albums()
        self.assertRaises(IntegrityError, FavoriteAlbum.objects.create, userID=self.user_profile, albumID=self.album)

    def test_fav_genre_uniqueness(self):
        """
        Checks that an IntegrityError is raised if the uniqueness constraints of the FavoriteGenre model are violated
        """

        populate_fav_genres()
        self.assertRaises(IntegrityError, FavoriteGenre.objects.create, userID=self.user_profile, genreID=self.genre)

    def test_vote_uniqueness(self):
        """
        Checks that an IntegrityError is raised if the uniqueness constraints of the Vote model are violated
        """

        Vote.objects.create(voteType='up', userID=self.user_profile, albumID=self.album)
        self.assertRaises(IntegrityError, Vote.objects.create, voteType='up', userID=self.user_profile, albumID=self.album)

    def test_username_uniqueness(self):
        """
        Checks that an IntegrityError is raised if the uniqueness constraints of the Vote model are violated
        """

        self.assertRaises(IntegrityError, User.objects.create_user, username='Dr bob', email='drBobsSecondEmail@email.com', password='drBobsNewPassword')

    def test_album_slug_uniqueness(self):
        """
        Checks that an IntegrityError is raised if the uniqueness constraints of the Album model are violated
        """

        self.assertRaises(IntegrityError, Album.objects.create, albumName='AM', artist="Arctic Monkeys", releaseDate="2013")

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

class IndexPageTests(TestCase):
    def test_index_view_no_albums(self):
        """
        Checks if correct message displays when database contains no albums
        """

        response = self.client.get(reverse('rango:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no albums present.')
        self.assertQuerysetEqual(response.context['albums'], [])

    def test_index_view_with_albums(self):
        """
        Checks if albums are displayed when present in database
        """
        
        populate_genres()
        populate_albums()

        response = self.client.get(reverse('rango:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AM')
        self.assertContains(response, 'Arctic Monkeys')
        self.assertContains(response, 'Demon Days')
        self.assertContains(response, 'Gorillaz')

        num_albums = len(response.context['albums'])
        self.assertEqual(num_albums, 2)



class AboutPageTest(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('rango:about'))
    
    def test_about_page_loads(self):
        """
        Checks if the status code of the returned HttpResponse is 200
        """

        self.assertEqual(self.response.status_code, 200)

class NewReviewsPageEmptyTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('rango:reviews'))
    
    def test_new_reviews_page_loads(self):
        """
        Checks if the status code of the returned HttpResponse is 200
        """

        self.assertEqual(self.response.status_code, 200)
        
    def test_new_reviews_view_shows_empty_message(self):
        """
        Checks if correct message displays when database contains no reviews
        """

        self.assertContains(self.response, 'There are no album reviews yet.')
        self.assertQuerysetEqual(self.response.context['reviews'], [])

class NewReviewsPagePopulatedTests(TestCase):
    @override_settings(MEDIA_ROOT=(TEST_DIR))
    def setUp(self):
        populate_genres()
        populate_albums()
        populate_users()
        populate_reviews()

        self.response = self.client.get(reverse('rango:reviews'))

    def test_new_reviews_page_loads(self):
        """
        Checks if the status code of the returned HttpResponse is 200
        """

        self.assertEqual(self.response.status_code, 200)


    def test_new_reviews_view_shows_review_texts(self):
        """
        Checks if review texts are displayed when present in database
        """

        self.assertContains(self.response, 'this is so bad turn it off!!! turn it offff!!!')
        self.assertContains(self.response, 'this is so good turn it up bai')

    def test_new_reviews_view_shows_usernames(self):
        """
        Checks if review authors' usernames are displayed when present in database
        """

        self.assertContains(self.response, 'Dr bob')
        self.assertContains(self.response, 'Paddy Mcguinness')

    def test_new_reviews_view_shows_album_names(self):
        """
        Checks if reviewed album names are displayed when present in database
        """

        self.assertContains(self.response, 'AM')
        self.assertContains(self.response, 'Demon Days')

    def test_new_reviews_view_context_dict_has_all_reviews(self):
        """
        Checks if all the reviews from the database are passed in the context dictionary
        """

        num_reviews = len(self.response.context['reviews'])
        self.assertEqual(num_reviews, 2)

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

class AllAlbumsPageEmptyTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('rango:all_albums'))
    
    def test_all_albums_view_loads(self):
        """
        Checks if the status code of the returned HttpResponse is 200
        """

        self.assertEqual(self.response.status_code, 200)

    def test_all_albums_view_shows_empty_message(self):
        """
        Checks if correct message displays when database contains no albums
        """

        self.assertContains(self.response, 'There are no albums available yet.')     

    def test_all_albums_view_context_dict_is_empty(self):
        """
        Checks if the context dictionary returned by the view is contains no albums
        """

        self.assertQuerysetEqual(self.response.context['albums'], [])

class AllAlbumsPagePopulatedTests(TestCase):
    @override_settings(MEDIA_ROOT=(TEST_DIR))
    def setUp(self):
        populate_genres()
        populate_albums()

        self.response = self.client.get(reverse('rango:all_albums'))

    def test_all_albums_view_shows_album_names(self):
        """
        Checks if album names are displayed correctly when present in database
        """

        self.assertContains(self.response, 'AM')
        self.assertContains(self.response, 'Demon Days')

    def test_all_albums_view_shows_authors(self):
        """
        Checks if album authors are displayed correctly when present in database
        """

        self.assertContains(self.response, 'Arctic Monkeys')
        self.assertContains(self.response, 'Gorillaz')

    def test_all_albums_view_shows_genres(self):
        """
        Checks if album genres are displayed correctly when present in database
        """

        self.assertContains(self.response, 'Indie rock')
        self.assertContains(self.response, 'Alternative rock')

    def test_all_albums_view_shows_votes(self):
        """
        Checks if album votes are displayed correctly when present in database
        """

        self.assertContains(self.response, '20')
        self.assertContains(self.response, '-20')

    def test_all_albums_view_context_dict_contains_all_albums(self):
        """
        Checks if the context dictionary returned by the view contains all albums
        """

        num_albums = len(self.response.context['albums'])
        self.assertEqual(num_albums, 2)

class UserProfilePageEmptyTests(TestCase):
    @override_settings(MEDIA_ROOT=(TEST_DIR))
    def setUp(self):
        populate_users()

        user = User.objects.get(username="Dr bob")
        user_profile = UserProfile1.objects.get(user=user)
        self.client.login(username=user.username, password=user.password)
        
        self.response = self.client.get(reverse('rango:user_profile', args=[user_profile.pk]))
    
    def test_user_profile_page_loads(self):
        """
        Checks if the status code of the returned HttpResponse is 200
        """

        self.assertEqual(self.response.status_code, 200)
        
    def test_user_profile_shows_no_fav_album_message(self):
        """
        Checks if no favourite album message is displayed
        """

        self.assertContains(self.response, 'No favourite albums yet')    

    def test_user_profile_shows_no_fav_genre_message(self):
        """
        Checks if no favourite genre message is displayed
        """

        self.assertContains(self.response, 'No favourite genres yet')   

    def test_user_profile_shows_no_reviews_message(self):
        """
        Checks if no review added message is displayed
        """

        self.assertContains(self.response, "No reviews yet")            
    
    def test_user_profile_context_dict_has_no_reviews(self):
        """
        Checks if the context dictionary returned by the view contains no reviews
        """

        review_num = len(self.response.context['reviews'])
        self.assertEqual(review_num, 0)        
 
    def tearDown(self):
        shutil.rmtree(TEST_DIR)

class UserProfilePagePopulatedTests(TestCase):
    @override_settings(MEDIA_ROOT=(TEST_DIR))
    def setUp(self):
        populate_genres()
        populate_users()
        populate_albums()
        populate_reviews()
        populate_fav_genres()
        populate_fav_albums()

        user = User.objects.get(username="Dr bob")
        user_profile = UserProfile1.objects.get(user=user)
        self.client.login(username=user.username, password=user.password)
        
        self.response = self.client.get(reverse('rango:user_profile', args=[user_profile.pk]))

    def test_user_profile_view_loads(self):
        """
        Checks if the status code of the returned HttpResponse is 200
        """

        self.assertEqual(self.response.status_code, 200)

    def test_user_profile_shows_username(self):
        """
        Checks if username is displayed
        """

        self.assertContains(self.response, 'Dr bob')

    def test_user_profile_shows_fav_album_name(self):
        """
        Checks if favourite album name is displayed
        """

        self.assertContains(self.response, 'AM')

    def test_user_profile_shows_fav_album_author(self):
        """
        Checks if favourite album author is displayed
        """

        self.assertContains(self.response, 'Arctic Monkeys')    

    def test_user_profile_shows_fav_genre(self):
        """
        Checks if favourite genre is displayed
        """

        self.assertContains(self.response, 'Indie rock')          
    
    def test_user_profile_context_dict_has_all_reviews(self):
        """
        Checks if all user's reviews are in the context dictionary
        """

        review_num = len(self.response.context['reviews'])
        self.assertEqual(review_num, 1)        
    
    def test_user_profile_shows_review_texts(self):
        """
        Checks if review texts are displayed
        """

        self.assertContains(self.response, "this is so bad turn it off!!! turn it offff!!!")     

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

class AlbumPagePopulatedTests(TestCase):
    @override_settings(MEDIA_ROOT=(TEST_DIR))
    def setUp(self):
        populate_genres()
        populate_albums()
        populate_users()
        populate_reviews()

        album = Album.objects.get(albumName='AM')
        
        self.response = self.client.get(reverse('rango:album', args=[album.slug]))


    def test_album_view_loads(self):
        """
        Checks if the status code of the returned HttpResponse is 200
        """

        self.assertEqual(self.response.status_code, 200)

    def test_album_view_shows_album_name(self):
        """
        Checks if album name is displayed
        """

        self.assertContains(self.response, "AM")

    def test_album_view_shows_artist(self):
        """
        Checks if artist is displayed
        """

        self.assertContains(self.response, "Arctic Monkeys")

    def test_album_view_shows_genre(self):
        """
        Checks if genre is displayed
        """

        self.assertContains(self.response, "Indie rock")

    def test_album_view_shows_votes(self):
        """
        Checks if number of votes is displayed
        """

        self.assertContains(self.response, "20")

    def test_album_view_shows_review_author_username(self):
        """
        Checks if usernames of users who added reviews are displayed
        """

        self.assertContains(self.response, "Dr bob")

    def test_album_view_shows_review_author_username(self):
        """
        Checks if review texts are displayed
        """

        self.assertContains(self.response, "this is so bad turn it off!!! turn it offff!!!")

    def test_album_view_context_dict_has_all_reviews(self):
        """
        Checks if all reviews of a given album are in the context dictionary
        """

        review_num = len(self.response.context['reviews'])
        self.assertEqual(review_num, 1) 

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

    

    
    





