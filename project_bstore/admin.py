from django.contrib import admin

# Register your models here.

from .models import Book
from .models import Profile
from .models import post

admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(post)
