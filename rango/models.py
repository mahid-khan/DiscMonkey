from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name
    
class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    

# database for new project disc monkey
# 
# .





class UserProfile1(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.CharField(max_length=255)

    #maybe consider password hashing

    #profile picture
    
    profilePicture = models.ImageField(upload_to='profilePicture/', default='default_pro_pic.jpg')

    def __str__(self):
        return self.user.username

    




class Album(models.Model):
    
    slug = models.SlugField(unique=True,blank=True)
    albumName = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    releaseDate = models.CharField(max_length=255)
    albumCover = models.ImageField(upload_to='albumCover/', default='default_cover.jpg')

    def __str__(self):
        return self.albumName

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.albumName)
            super(Album, self).save(*args, **kwargs)



class Review(models.Model):
    #just one review using composite key  UserID/AlbumID
    TEXT_MAX_LENGTH = 255
    userID = models.ForeignKey(UserProfile1, on_delete=models.CASCADE)
    albumID = models.ForeignKey(Album, on_delete=models.CASCADE)
    reviewText = models.CharField(max_length=TEXT_MAX_LENGTH)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['userID', 'albumID'], name='uniqueVoteID') ]

    def __str__(self):
        return self.userID.user.username + ", " + self.albumID.albumName





class Vote(models.Model):
    #composite primary key (UserID/AlbumID)
    #make uniqe key constraint instead of composite primary key



    voteType = models.CharField(max_length=255)
    userID = models.ForeignKey(UserProfile1, on_delete=models.CASCADE)
    albumID = models.ForeignKey(Album, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['userID', 'albumID'], name='uniqueVoteID') ]

    def __str__(self):
        return self.userID.user.username + ", " + self.albumID.albumName



class Genre(models.Model):
    genreName = models.CharField(max_length=255)
    genreDescription = models.CharField(max_length=255)

    def __str__(self):
        return self.genreName



class FavoriteAlbum(models.Model):


    dateAdded = models.DateField(max_length=255)
    userID = models.ForeignKey(UserProfile1, on_delete=models.CASCADE)
    albumID = models.ForeignKey(Album, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['userID', 'albumID'], name='uniqueFavAlbumID') ]

    def __str__(self):
        return self.userID.user.username



class GenreAlbum(models.Model):

    
    albumname = models.CharField(max_length=255)
    genreID = models.ForeignKey(Genre, on_delete=models.CASCADE)
    albumID  = models.ForeignKey(Album, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['genreID', 'albumID'], name='uniqueGenreAlbum') ]

    def __str__(self):
        return self.albumname




class FavoriteGenre(models.Model):
    
    
    dateAdded = models.DateField(max_length=255)

    
    genreID = models.ForeignKey(Genre, on_delete=models.CASCADE)
    userID  = models.ForeignKey(UserProfile1, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['userID', 'genreID'], name='uniqueFavoriteGenre') ]

    def __str__(self):
        return self.userID.user.username


    



