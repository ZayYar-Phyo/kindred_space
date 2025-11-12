from django import template
from a_posts.models import UserProfile

register = template.Library()


@register.filter
def get_profile(user):
    """Safely get or create a user's profile"""
    if not user or not user.is_authenticated:
        return None
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile
