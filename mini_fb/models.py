from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of an Article by some author.'''
    # data attributes of a Article:
    FirstName = models.TextField(blank=False)
    LastName = models.TextField(blank=False)
    City = models.TextField(blank=False)
    Email = models.TextField(blank=False)
    ProfileImage = models.TextField(blank=False)
    