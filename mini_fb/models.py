from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of an Article by some author.'''
    # data attributes of a Article:
    FirstName = models.TextField(blank=False)
    LastName = models.TextField(blank=False)
    City = models.TextField(blank=False)
    Email = models.TextField(blank=False)
    ProfileImage = models.TextField(blank=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    def get_message(self):
        message = StatusMessage.objects.filter(Profile = self).order_by('-TimeStamp')
        return message
    def get_absolute_url(self):
        """
        Returns the URL to view this profile's detail page.
        """
        return reverse('profile_detail', kwargs={'pk': self.pk})
    def get_friends(self):
        """
        Returns a list of Profiles that are friends with this Profile.
        """
        # Find all Friend instances where this Profile is either profile1 or profile2
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)

        # Collect all friend profiles
        friends = [friend.profile2 for friend in friends_as_profile1] + \
                  [friend.profile1 for friend in friends_as_profile2]

        return list(set(friends))
    def add_friend(self, other):
        if self == other:
            raise ValueError("A profile cannot be friends with itself.")

        # Check if a Friend relationship already exists (either direction)
        friend_exists = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
        ).exists()

        # If no existing friendship, create a new Friend instance
        if not friend_exists:
            Friend.objects.create(profile1=self, profile2=other)
    def get_friend_suggestions(self):
        """
        Returns a list of Profiles that are not friends with this Profile and do not include this Profile.
        """
        # Get profiles that are friends with this profile
        friends = self.get_friends()

        # Build a query to exclude this profile and existing friends
        suggestions = Profile.objects.exclude(
            Q(id=self.id) | Q(id__in=[friend.id for friend in friends])
        )

        return suggestions
    def get_news_feed(self):
        """
        Returns a queryset of all StatusMessages for the profile itself and all friends, ordered by timestamp (most recent first).
        """
        # Get friends' profiles
        friends = self.get_friends()

        # Collect StatusMessages from this profile and friends
        status_messages = StatusMessage.objects.filter(
            Q(Profile=self) | Q(Profile__in=friends)
        ).order_by('-TimeStamp')

        return status_messages

class StatusMessage(models.Model):
    TimeStamp = models.DateTimeField(auto_now_add=True)
    Message = models.TextField(blank = False)
    Profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        return f'(self.TimeStamp) by (self.Message)'

    def get_images(self):
        return self.images.all()
    
class Image(models.Model):
    """
    Represents an image file associated with a StatusMessage.
    """
    # Image file stored in the Django media directory
    image_file = models.ImageField(blank=False)
    # Timestamp of when the image was uploaded
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # ForeignKey to associate the image with a StatusMessage
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image {self.id} for StatusMessage {self.status_message.id} uploaded at {self.uploaded_at}"


class Friend(models.Model):
    profile1 = models.ForeignKey("Profile", on_delete= models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete= models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1} & {self.profile2}"