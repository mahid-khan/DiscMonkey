from django import forms
from rango.models import UserProfile1, Review, Album, Genre
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile1
        fields = ('bio', 'profilePicture')

class ReviewForm(forms.ModelForm):
    reviewText = forms.CharField(
        max_length=Review.TEXT_MAX_LENGTH,
        help_text="Enter your review of the album",
        widget=forms.Textarea(attrs={'rows':5, 'cols': 40}),
        label=None
    )

    class Meta:
        model = Review
        fields = ('reviewText',)

class EditProfileForm(forms.ModelForm):
    profilePicture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile1
        fields = ('profilePicture',)

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('albumName', 'artist', 'releaseDate', 'albumCover')

class GenreFilterForm(forms.Form):
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), required=False, label="Genre")
