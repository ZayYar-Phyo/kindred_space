from django.db import models
import uuid

class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('GIVE', 'I want to GIVE'),
        ('REQUEST', 'I need to REQUEST'),
    ]
    
    title = models.CharField(max_length=500, blank=True, null=True)
    artist = models.CharField(max_length=500, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='posts/')
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='GIVE')
    reason = models.TextField(blank=True, help_text='Why are you giving this away? or Why do you need this item/skill?')
    latitude = models.FloatField(default=0.0)  # required, default for existing rows
    longitude = models.FloatField(default=0.0)  # required, default for existing rows
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