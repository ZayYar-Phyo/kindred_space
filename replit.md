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
- User authentication with Japanese-language login/signup pages
- User profiles with community metrics (reputation, contributions, success rate)
- **Peer-to-peer rating system** - Users can review each other with 1-5 star ratings and comments
- **Dynamic reputation scores** - Automatically calculated from real user reviews
- Post creation with image uploads (requires login)
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
- `LOGIN_URL = '/login/'` - Custom login page instead of Django admin
- `LOGIN_REDIRECT_URL = '/'` - Redirects to home after login

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

## Authentication System
The platform uses a custom authentication system with Japanese-language UI:

### Available Pages
- **Login**: `/login/` - User-friendly login page with Japanese UI
- **Signup**: `/signup/` - Registration page for new users
- **Logout**: `/logout/` - POST-only logout with CSRF protection

### Features
- Automatic redirect to originally requested page after login (`next` parameter)
- Security validation on redirect URLs to prevent open redirect vulnerabilities
- Success messages in Japanese for login/signup/logout
- Auto-creates UserProfile for new signups
- Protected routes require login (post creation, editing, deletion)

### Demo Account
- Username: `demo_user`
- Password: `demo123`
- You can now login at `/login/` instead of Django admin!

## Recent Changes
- **2025-11-12**: Professional Profile Page Redesign
  - Enlarged profile photo from 80px to 120px with enhanced shadow and border
  - Increased name typography from text-2xl to text-3xl for better prominence
  - Added "プロフィールを編集" (Edit Profile) button visible only to profile owner
  - Enhanced statistics display with text-4xl numbers and hover effects
  - Upgraded trust metrics bar with gradient background (yellow-50 to orange-50)
  - Implemented responsive grid layout (stacks on mobile, 3 columns on desktop)
  - Improved spacing throughout (p-8, gap-6) for cleaner visual hierarchy
  - All data correctly mapped to backend fields (display_name, bio, reputation_score, etc.)
  - Architect-approved and production-ready

- **2025-11-12**: Peer-to-Peer Rating System
  - Created Review model with rating (1-5 stars), comment, reviewer/reviewee relationships
  - Implemented automatic reputation score calculation based on average of all user reviews
  - Added review submission form with star selector and optional comment field on profile pages
  - Created reviews display section showing recent reviews with avatars, ratings, and timestamps
  - Review count now displays alongside reputation score (accurate total, displays 10 most recent)
  - Validation prevents self-reviews and enforces required rating
  - URL endpoint: `/users/<username>/review/` for review submission
  - Database migration applied successfully (Review table created)
  - Users can now give authentic peer feedback instead of static reputation scores
  - Architect-approved and production-ready

- **2025-11-12**: Bulletproof Profile Safety System
  - Created context processor (`a_posts/context_processors.py`) for safe logged-in user profile access
  - Created template filter (`get_profile`) for safe post author profile access
  - Eliminates all RelatedObjectDoesNotExist exceptions across the platform
  - All profile access now uses safe helpers with `get_or_create` pattern
  - Post displays now show real usernames from `post.user.username` (migrated from deprecated `artist` field)
  - Added visual post type badges (提供 for GIVE, 依頼 for REQUEST)
  - Profile pictures display with auto-generated avatar fallbacks
  - Edit/Delete buttons only visible to post owners for security
  - Clickable username links to user profiles
  - Anonymous user fallback for legacy posts without users
  - Production-ready and architect-approved

- **2025-11-12**: User Authentication System Implementation
  - Created custom login page with Japanese UI at `/login/`
  - Created signup/registration page at `/signup/`
  - Implemented secure logout with POST-only and CSRF protection
  - Added proper `next` parameter handling for redirect after login
  - Updated navigation to use new authentication pages
  - Added success messages in Japanese
  - All authentication follows Django best practices
  
- **2025-11-12**: Navigation Bar and Authentication Improvements
  - Updated navigation bar with dynamic user profile integration
  - "My Profile" link now correctly uses `/users/{{ user.username }}/`
  - Replaced hardcoded user display with actual logged-in user's username
  - Added dynamic profile picture display (uploaded image or generated avatar)
  - Implemented authentication checks (show login/logout based on user state)
  - Added @login_required decorators to post create/edit/delete views
  - Configured LOGIN_URL and LOGIN_REDIRECT_URL in settings
  
- **2025-11-12**: User Profile Feature Implementation
  - Created UserProfile model with community metrics
  - Added user field to Post model for ownership tracking
  - Created profile view and comprehensive profile template
  - Implemented trust metrics and contribution statistics
  - Added automatic profile creation on user registration
  - Created demo user creation script
  - Data migration to backfill profiles for existing users

- **2025-11-11**: Initial Replit setup
  - Created requirements.txt
  - Configured Django settings for Replit environment
  - Added .gitignore for Python/Django project
  - Set up workflow for development server on port 5000
  - Configured deployment with Gunicorn
  - Added replit.md documentation
  - Fixed map display and zoom controls overflow issues
