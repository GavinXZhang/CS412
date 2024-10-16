from django.db import models
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of an Article by some author.'''
    # data attributes of a Article:
    FirstName = models.TextField(blank=False)
    LastName = models.TextField(blank=False)
    City = models.TextField(blank=False)
    Email = models.TextField(blank=False)
    ProfileImage = models.TextField(blank=False)
    def get_message(self):
        message = StatusMessage.objects.filter(Profile = self).order_by('-TimeStamp')
        return message
    def get_absolute_url(self):
        """
        Returns the URL to view this profile's detail page.
        """
        return reverse('profile_detail', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
    TimeStamp = models.DateTimeField(auto_now_add=True)
    Message = models.TextField(blank = False)
    Profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        return f'(self.TimeStamp) by (self.Message)'
