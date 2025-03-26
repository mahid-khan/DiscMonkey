from django import forms
from rango.models import Page, Category, UserProfile1, Review, Album
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re

class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=Category.NAME_MAX_LENGTH,
        help_text="Enter the album name:"
    )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)


    class Meta:

        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(
        max_length=Page.TITLE_MAX_LENGTH,
        help_text="Please enter the title of the page."
    )
    url = forms.URLField(
        max_length=Page.URL_MAX_LENGTH,
        help_text="Please enter the URL of the page.",
        validators=[URLValidator(schemes=['http', 'https'])]
    )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:

        model = Page

        exclude = ('category',)

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url:
            # 如果URL不以http://或https://开头，添加http://
            if not re.match(r'https?://', url):
                url = f'http://{url}'
            try:
                # 使用更宽松的URL验证
                URLValidator(schemes=['http', 'https'])(url)
            except ValidationError:
                raise ValidationError('Please enter a valid URL.')
        return url

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile1
        fields = ('bio', 'profilePicture',)

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
