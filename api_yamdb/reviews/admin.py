from django.contrib import admin

from .models import User, Title, Comment, Category, Genre, Review
admin.site.register(User)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
