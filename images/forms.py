from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {'url': forms.HiddenInput, }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()

        if extension not in valid_extensions:
            raise forms.ValidationError('This given URL does not match given image extensions.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        # new image instance by calling save() method with commit=False
        image = super().save(commit=False)
        # get the URL from cleaned_data
        image_url = self.cleaned_data['url']
        # generate image name by using the title with the file extension (image_title.jpg)
        name = slugify(image.title)  # using the slug to remove the spaces between words
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        """ModelForm provides a save() method to save the current model instance to the database and return the object. 
            This method receives a Boolean commit parameter, which allows you to specify whether the object has to be 
            persisted to the database"""

        # download image from the given URL
        response = request.urlopen(image_url)  # using urllib to download the image
        image.image.save(image_name, ContentFile(response.read()), save=False)
        # you pass ContentFile object to the save() method and instantiate it with the downloaded file content.
        # In this way, you save the file to the media directory of your project.
        # You pass the save=False parameter to avoid saving the object to the database yet.
        # to maintain the same behavior as the save() method you override,
        # you save the form to the database only when the commit=True (i the views section)
        if commit:
            image.save()

        return image

# to retrieve images from URLs served through HTTPS: pip install --upgrade certifi
