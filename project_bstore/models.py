from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.urls import reverse
# we do the work related to databases here
class Book(models.Model):

    title            = models.TextField()
    isbn10           = models.CharField(max_length=10)
    author           = models.TextField()
    rating           = models.FloatField()
    read_url         = models.URLField()
    image_url        = models.URLField()
    publication_year = models.IntegerField()

    def __str__(self):
        return "isbn: {}, title: {}".format(self.isbn10, self.title)


class Profile(models.Model):

	user  = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	
	def __str__(self):
 		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
 		super(Profile, self).save(*args, **kwargs)

 		img = Image.open(self.image.path)

 		if img.height > 300 or img.width > 300:
 			output_size = (300,300)
 			img.thumbnail(output_size)
 			img.save(self.image.path)


class post(models.Model):
    title       = models.CharField(max_length=200)
    seller      = models.ForeignKey(User, on_delete = models.CASCADE)	
    content     = models.TextField()
    picture     = models.ImageField(default = 'default.jpg', upload_to='post_pics')
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
