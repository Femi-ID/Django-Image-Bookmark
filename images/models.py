from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked',
                                        blank=True)
    # many-to-many relationship because a user might like multiple images and each image can be liked by multiple users.
    # The ManyToManyField can be defined in either of the two related models.
    # many-to-many relationships at: https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_many/.

    # Database indexes improve query performance. Use db_index=True for fields that you frequently query using
    # filter(), exclude(), or order_by(). ForeignKey fields or fields with unique=True imply the creation of an index.
    # You can also use Meta.index_together or Meta.indexes to create indexes for multiple fields.
    # Database indexes at https://docs.djangoproject.com/en/3.0/ref/models/options/#django.db.models.Options.indexes.

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:  # if slug field is not provided
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
# You override the save method to automatically generate a slug field based on the value of title field


