from django.contrib import admin

# Register your models here.

from .models import book_table
from .models import Profile
from .models import post

admin.site.register(Profile)
admin.site.register(book_table)
admin.site.register(post)