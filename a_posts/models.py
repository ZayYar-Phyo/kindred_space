from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('GIVE', 'I want to GIVE'),
        ('REQUEST', 'I need to REQUEST'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    artist = models.CharField(max_length=500, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='posts/')
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='GIVE')
    reason = models.TextField(blank=True, help_text='Why are you giving this away? or Why do you need this item/skill?')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    show_general_area_only = models.BooleanField(default=False)
    display_area = models.CharField(max_length=255, blank=True, default='')
    body = models.TextField()
    tags = models.ManyToManyField('Tag')
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True,  primary_key=True, editable=False)

    def __str__(self):
        return str(self.title or 'Untitled')
    
    class Meta:
        ordering = ['-created_at']  # Orders posts by creation date in descending order latest first
        
class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return str(self.name)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, 
                                       help_text='Profile picture')
    bio = models.TextField(max_length=500, blank=True, default='', 
                          help_text='User self-introduction')
    reputation_score = models.FloatField(default=5.0, 
                                        help_text='Average rating from transactions (e.g., 4.9)')
    total_contributions = models.IntegerField(default=0, 
                                             help_text='Count of successfully completed Give posts and Skill Offers')
    success_rate = models.FloatField(default=100.0, 
                                    help_text='Percentage of follow-through on transactions')
    location_display = models.CharField(max_length=255, blank=True, default='', 
                                       help_text='General area where user shares (e.g., Osaka-shi, Kita-ku)')
    is_verified = models.BooleanField(default=False, 
                                     help_text='ID verification status')
    followers_count = models.IntegerField(default=0, 
                                         help_text='Number of followers/neighbors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    @property
    def display_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def reputation_stars(self):
        return int(self.reputation_score)

    @property
    def default_avatar_url(self):
        return 'https://img.icons8.com/small/96/A9A9A9/happy.png'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()