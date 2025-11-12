#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_core.settings')
django.setup()

from django.contrib.auth.models import User
from a_posts.models import UserProfile

username = 'demo_user'

if not User.objects.filter(username=username).exists():
    user = User.objects.create_user(
        username=username,
        email='demo@kindredspace.com',
        password='demo123',
        first_name='田中',
        last_name='花子'
    )
    
    profile = user.profile
    profile.bio = '大阪で子育て中です。使わなくなったものを必要な方に譲りたいと思っています。'
    profile.reputation_score = 4.8
    profile.total_contributions = 165
    profile.success_rate = 95.5
    profile.location_display = '大阪府 大阪市 北区'
    profile.is_verified = True
    profile.followers_count = 42
    profile.save()
    
    print(f"Demo user '{username}' created successfully!")
    print(f"Username: {username}")
    print(f"Password: demo123")
    print(f"Profile URL: /users/{username}/")
else:
    print(f"User '{username}' already exists.")
