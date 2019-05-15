from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.urls import reverse
# we do the work related to databases here
class book_table(models.Model):
	
	book_id = models.IntegerField()
	books_count = models.IntegerField()
	publication_year = models.IntegerField()
	
	authors = models.TextField()
	title = models.TextField()
	
	average_rating = models.FloatField()
	
	image_url = models.URLField()

	def __str__(self):
		return '<id: {},book_id: {},books_count: {},publication_year: {},authors: {},title: {},average_rating: {},image_url: {}>'.format(self.id,self.book_id,self.books_count,self.publication_year,self.authors,self.title,self.average_rating,self.image_url)



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
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
	title = models.CharField(max_length=200)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	seller = models.ForeignKey(User, on_delete = models.CASCADE)
	picture = models.ImageField(default = 'default.jpg', upload_to='post_pics')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail',kwargs={'pk':self.pk})

