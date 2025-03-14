from django.test import TestCase
from django.urls import reverse
from rango.models import Album
from rango.models import UserProfile1
from rango.models import Review

# Create your tests here.

def add_album(name, artist, year):
    album = Album.objects.get_or_create(albumName=name, artist=artist, releaseDate=year)[0]
    return album

def add_user(username, password, bio, email):
    user = UserProfile1.objects.get_or_create(username=username, password=password, bio=bio, email=email)
    return user

def add_review(username, album_name, text):
    user = UserProfile1.objects.get(username=username)
    album = Album.objects.get(albumName = album_name)
    review = Review.objects.get_or_create(userID=user, albumID=album, reviewText=text)
    return review



class IndexTests(TestCase):
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
        Checks if albums are displayed correctly when present in database
        """
        
        add_album("AM", "Arctic Monkeys", "2013")
        add_album("Demon Days", "Gorillaz", "2005")

        response = self.client.get(reverse('rango:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AM')
        self.assertContains(response, 'Arctic Monkeys')
        self.assertContains(response, 'Demon Days')
        self.assertContains(response, 'Gorillaz')

        num_albums = len(response.context['albums'])
        self.assertEqual(num_albums, 2)


class NewReviewsTests(TestCase):
    def test_new_reviews_view_no_reviews(self):
        """
        Checks if correct message displays when database contains no reviews
        """
        response = self.client.get(reverse('rango:reviews'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no albums present.')
        self.assertQuerysetEqual(response.context['reviews'], [])

    def test_new_reviews_view_with_reviews(self):
        """
        Checks if reviews are displayed correctly when present in database
        """
        
        add_album('AM', 'Arctic Monkeys', '2013')
        add_album('Demon Days', "Gorillaz", '2005')
        add_user('Dr  bob', 'drBobsSecretPassword', 'hey im dr bob a profesional doctor man', 'doctorBob@Medical.com')
        add_user('Paddy Mcguinness', 'wolfeTones1954', 'Paddy Mcguinness acomplished cow tipper', 'paddymcguinnes@country.com')
        add_review('Dr  bob', 'AM', "this is so bad turn it off!!! turn it offff!!!")
        add_review('Paddy Mcguinness', 'Demon Days', "this is so good turn it up bai")

        response = self.client.get(reverse('rango:reviews'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AM')
        self.assertContains(response, 'Dr  bob')
        self.assertContains(response, 'Demon Days')
        self.assertContains(response, 'this is so bad turn it off!!! turn it offff!!!')
        self.assertContains(response, 'this is so good turn it up bai')

        num_reviews = len(response.context['reviews'])
        self.assertEqual(num_reviews, 2)


