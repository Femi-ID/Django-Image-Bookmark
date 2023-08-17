from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.


class Action(models.Model):
    user = models.ForeignKey('auth.User', related_name='actions',
                             db_index=True, on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType, blank=True,
                                  null=True, related_name='target_obj',
                                  on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True,
                                            db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    # • verb: Describing the action the user performed
    # • created: to automatically set the current datetime when the object is saved for the first time in the database.
    # • target_ct: A ForeignKey field that points to the ContentType model
    # • target_id: A PositiveIntegerField for storing the primary key of the related object
    # • target: A GenericForeignKey field to the related object based on the combination of the two previous fields

    class Meta:
        ordering = ('-created',)


"""
The contenttypes application contains a ContentType model. Instances of this
model represent the actual models of your application, nd new instances of
ContentType are automatically created when new models are installed in your
project.
In the shell command:

from django.contrib.contenttypes.models import ContentType
>>> image_type = ContentType.objects.get(app_label='images',
model='image')
>>> image_type
<ContentType: images | image>

You can also retrieve the model class from a ContentType object by calling its
model_class() method:
>>> image_type.model_class()
<class 'images.models.Image'>

It's also common to get the ContentType object for a particular model class,
as follows:
>>> from images.models import Image
>>> ContentType.objects.get_for_model(Image)
<ContentType: images | image>

find the official documentation about the contenttypes
framework at https://docs.djangoproject.com/en/3.0/ref/contrib/
contenttypes/
"""