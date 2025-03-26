from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

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


# class Album(models.Model):
    
#     slug = models.SlugField(unique=True,blank=True)
#     albumName = models.CharField(max_length=255)
#     artist = models.CharField(max_length=255)
#     releaseDate = models.CharField(max_length=255)
#     albumCover = models.ImageField(upload_to='albumCover/', default='default_cover.jpg')

#     def __str__(self):
#         return self.albumName

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.albumName)
#             super(Album, self).save(*args, **kwargs)

class Album(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    albumName = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    releaseDate = models.CharField(max_length=255)
    albumCover = models.ImageField(upload_to='albumCover/', default='default_cover.jpg')
    score = models.IntegerField(default=0)  # Add this field to track the total score

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


# class Vote(models.Model):
#     #composite primary key (UserID/AlbumID)
#     #make uniqe key constraint instead of composite primary key



#     voteType = models.CharField(max_length=255)
#     userID = models.ForeignKey(UserProfile1, on_delete=models.CASCADE)
#     albumID = models.ForeignKey(Album, on_delete=models.CASCADE)

#     class Meta:
#         constraints = [models.UniqueConstraint(fields=['userID', 'albumID'], name='uniqueVoteID') ]

#     def __str__(self):
#         return self.userID.user.username + ", " + self.albumID.albumName

class Vote(models.Model):
    VOTE_TYPES = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )
    
    voteType = models.CharField(max_length=4, choices=VOTE_TYPES)
    userID = models.ForeignKey(UserProfile1, on_delete=models.CASCADE)
    albumID = models.ForeignKey(Album, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['userID', 'albumID'], name='uniqueVoteID')]

    def __str__(self):
        return f"{self.userID.user.username}, {self.albumID.albumName}, {self.voteType}"
    
    def save(self, *args, **kwargs):
        # Check if this is a new vote
        is_new = self.pk is None
        
        # Get old vote if updating
        old_vote = None
        if not is_new:
            old_vote = Vote.objects.get(pk=self.pk)
            
        # Save the vote
        super(Vote, self).save(*args, **kwargs)
        
        # Update album score
        album = self.albumID
        
        if is_new:  # New vote
            if self.voteType == 'up':
                album.score += 1
            else:
                album.score -= 1
        else:  # Changed vote
            if old_vote and old_vote.voteType != self.voteType:
                if self.voteType == 'up':
                    album.score += 2  # -1 to +1 = change of 2
                else:
                    album.score -= 2  # +1 to -1 = change of 2
                    
        album.save()

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
