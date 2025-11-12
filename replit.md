# KindredSpace - Community Sharing Platform

## Overview
This is a Django-based web application for a Japanese community sharing platform called "KindredSpace". The platform allows users to post items or skills they want to GIVE away or REQUEST from others. The app includes location-based features using Japanese postal codes with geocoding integration.

## Project Architecture

### Tech Stack
- **Backend**: Django 5.2.6 (Python 3.12)
- **Frontend**: HTML templates with Tailwind CSS
- **Database**: SQLite (development) - db.sqlite3
- **Image Handling**: Pillow for image uploads
- **External APIs**: 
  - ZipCloud API (Japanese postal code lookup)
  - Nominatim/OpenStreetMap (geocoding)

### Project Structure
```
.
├── a_core/              # Django project settings
│   ├── settings.py      # Main configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI application
├── a_posts/             # Main app for posts
│   ├── models.py        # Post and Tag models
│   ├── views.py         # View functions
│   ├── forms.py         # Post creation/editing forms
│   └── migrations/      # Database migrations
├── templates/           # HTML templates
│   ├── a_posts/         # Post-specific templates
│   ├── includes/        # Reusable components
│   └── layouts/         # Base layouts
├── media/               # User uploaded images
└── manage.py            # Django management script
```

### Key Features
- Post creation with image uploads
- Location-based posts using Japanese postal codes
- Search functionality (by title, body, artist, tags)
- Post types: GIVE (offering items/skills) or REQUEST (seeking items/skills)
- Tag/category system
- Privacy options (show general area only or exact location)

## Development

### Running Locally
The Django development server is configured to run on `0.0.0.0:5000` for Replit compatibility.

### Database
Currently using SQLite for development. The database is already migrated and includes existing posts with images.

### Configuration Notes
- `ALLOWED_HOSTS = ['*']` - Allows all hosts for development
- `CSRF_TRUSTED_ORIGINS` - Configured for Replit domains
- `X_FRAME_OPTIONS = 'SAMEORIGIN'` - Allows iframe embedding in Replit
- XFrame middleware removed for Replit iframe compatibility

## Deployment
The project is configured for deployment using:
- **Deployment Type**: Autoscale
- **Production Server**: Gunicorn
- **Command**: `gunicorn --bind=0.0.0.0:5000 --reuse-port a_core.wsgi:application`

## Dependencies
See `requirements.txt` for all Python dependencies:
- Django 5.2.6
- Pillow 11.1.0
- beautifulsoup4 4.12.3
- requests 2.32.3
- gunicorn 23.0.0

## User Profiles
The platform now includes comprehensive user profiles with community metrics:

### UserProfile Model Fields
- **profile_picture**: User's profile image
- **bio**: Self-introduction (max 500 characters)
- **reputation_score**: Average rating from transactions (default 5.0)
- **total_contributions**: Count of successful contributions
- **success_rate**: Percentage of completed transactions (default 100%)
- **location_display**: General area for sharing activities
- **is_verified**: ID verification status
- **followers_count**: Number of followers/neighbors

### Profile Features
- Trust metrics display (reputation score with star ratings)
- Community badges (achievements based on contributions)
- Contribution summary (stats showing impact)
- Activity tabs: 提供中 (Giving), 依頼中 (Requesting), 履歴 (History)
- Profile URL: `/users/{username}/`

## Recent Changes
- **2025-11-12**: User Profile Feature Implementation
  - Created UserProfile model with community metrics
  - Added user field to Post model for ownership tracking
  - Created profile view and comprehensive profile template
  - Implemented trust metrics and contribution statistics
  - Added automatic profile creation on user registration
  - Created demo user creation script

- **2025-11-11**: Initial Replit setup
  - Created requirements.txt
  - Configured Django settings for Replit environment
  - Added .gitignore for Python/Django project
  - Set up workflow for development server on port 5000
  - Configured deployment with Gunicorn
  - Added replit.md documentation
  - Fixed map display and zoom controls overflow issues
