from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .prefectures import PREFECTURE_CHOICES

class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('GIVE', 'I want to GIVE'),
        ('REQUEST', 'I need to REQUEST'),
    ]
    
    URGENCY_CHOICES = [
        ('asap', 'できるだけ早く'),
        ('week', '1週間以内'),
        ('no_rush', '急ぎではない'),
        ('custom', '日付を指定'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    artist = models.CharField(max_length=500, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='GIVE')
    reason = models.TextField(blank=True, help_text='Why are you giving this away? or Why do you need this item/skill?')
    prefecture = models.CharField(max_length=50, blank=True, default='', choices=PREFECTURE_CHOICES, help_text='Prefecture/都道府県')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    show_general_area_only = models.BooleanField(default=False)
    display_area = models.CharField(max_length=255, blank=True, default='')
    body = models.TextField()
    tags = models.ManyToManyField('Tag')
    acceptable_condition = models.CharField(max_length=100, blank=True, default='', help_text='Acceptable condition for REQUEST posts (any, good, like_new)')
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, blank=True, default='', help_text='Urgency level for REQUEST posts')
    deadline_date = models.DateField(null=True, blank=True, help_text='Specific deadline date for REQUEST posts')
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True,  primary_key=True, editable=False)

    def __str__(self):
        return str(self.title or 'Untitled')
    
    class Meta:
        ordering = ['-created_at']  # Orders posts by creation date in descending order latest first
        
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/')
    order = models.PositiveIntegerField(default=0, help_text='Display order (0 = first)')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.order + 1} for {self.post.title}"

    class Meta:
        ordering = ['order', 'created_at']


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

    def update_reputation_score(self):
        reviews = Review.objects.filter(reviewee=self.user)
        if reviews.exists():
            average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.reputation_score = round(average_rating, 1)
            self.save()


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given',
                                help_text='User who wrote the review')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received',
                                help_text='User being reviewed')
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                                help_text='Rating from 1 to 5 stars')
    comment = models.TextField(blank=True, default='',
                              help_text='Optional written feedback')
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True,
                           related_name='reviews',
                           help_text='Related post/transaction (optional)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reviewer.username} → {self.reviewee.username}: {self.rating}★"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        unique_together = [['reviewer', 'reviewee', 'post']]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        profile, created = UserProfile.objects.get_or_create(user=self.reviewee)
        profile.update_reputation_score()


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following',
                                help_text='User who is following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers',
                                 help_text='User being followed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        ordering = ['-created_at']
        unique_together = [['follower', 'following']]


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('follow', 'New Follower'),
        ('review', 'New Review'),
        ('post', 'New Post'),
        ('message', 'New Message'),
        ('system', 'System Message'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_received',
                                 help_text='User who receives the notification')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent',
                              null=True, blank=True,
                              help_text='User who triggered the notification (null for system messages)')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system')
    message = models.TextField(help_text='Notification message content')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=500, blank=True, default='',
                           help_text='URL to redirect when notification is clicked')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sender_name = self.sender.username if self.sender else 'System'
        return f"{sender_name} → {self.recipient.username}: {self.message[:50]}"

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = '通知一覧'
        ordering = ['-created_at']


class ChatRoom(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='chat_rooms',
                            help_text='The post this conversation is about')
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms_as_p1',
                                    help_text='Post owner')
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms_as_p2',
                                    help_text='User who initiated the chat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat: {self.participant1.username} & {self.participant2.username} about {self.post.title}"

    class Meta:
        verbose_name = 'チャットルーム'
        verbose_name_plural = 'チャットルーム一覧'
        ordering = ['-updated_at']
        unique_together = ['post', 'participant1', 'participant2']

    def get_other_participant(self, user):
        if user == self.participant1:
            return self.participant2
        return self.participant1


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"

    class Meta:
        verbose_name = 'メッセージ'
        verbose_name_plural = 'メッセージ一覧'
        ordering = ['created_at']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


# Signal to create notification when someone follows
@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.following,
            sender=instance.follower,
            notification_type='follow',
            message=f'{instance.follower.username}さんがあなたをフォローしました',
            link=f'/users/{instance.follower.username}/'
        )


# Signal to create notification when someone leaves a review
@receiver(post_save, sender=Review)
def create_review_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.reviewee,
            sender=instance.reviewer,
            notification_type='review',
            message=f'{instance.reviewer.username}さんがあなたを{instance.rating}つ星で評価しました',
            link=f'/users/{instance.reviewer.username}/'
        )


# Signal to create notification when someone sends a message
@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        chat_room = instance.chat_room
        recipient = chat_room.get_other_participant(instance.sender)
        if recipient is None:
            return
        title = chat_room.post.title or chat_room.post.display_area or '投稿'
        post_title = title[:20]
        if len(title) > 20:
            post_title += '...'
        Notification.objects.create(
            recipient=recipient,
            sender=instance.sender,
            notification_type='message',
            message=f'{instance.sender.username}さんから「{post_title}」についてメッセージが届きました',
            link=f'/chat/room/{chat_room.id}/'
        )