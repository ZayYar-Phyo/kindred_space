# KindredSpace - Community Sharing Platform

## Overview
KindredSpace is a Django-based web application designed as a Japanese community sharing platform. Its core purpose is to facilitate the giving and requesting of items or skills among users. The platform incorporates location-based functionalities using Japanese postal codes and geocoding, aiming to foster local community engagement and resource sharing. It includes robust user profiles with dynamic reputation scores, peer-to-peer rating systems, and a focus on intuitive Japanese-language UI.

## User Preferences
I prefer iterative development with clear, concise explanations for each step. Please ensure that all new features and modifications are well-documented. I value clean code and maintainable solutions. Before making any major architectural changes or introducing new external dependencies, please ask for my approval. Ensure all user-facing text is in Japanese where appropriate. I prefer detailed explanations for complex features.

## System Architecture

### UI/UX Decisions
The platform features an eco-friendly green color scheme (#4CAF50) as the primary brand color, used for buttons, forms, and accents, while the header is a clean off-white (bg-gray-50) for a professional look. The header implements a unified green button aesthetic with clear visual hierarchy: the "検索" (Search) button features green background with white text and full rounded corners (rounded-lg), "Create Post" is styled as a primary CTA button with green background and white text, and "Home" is a secondary green text link with bold font-weight. All navigation elements use proper spacing with gap-6 utilities for consistent layout. The search bar includes an inset shadow input field with the search button perfectly aligned vertically using flexbox centering. It includes responsive design for all components, an auto-hiding header on scroll, and dynamic hero background carousels with pagination using Swiper.js. User profiles are professionally redesigned with enlarged photos, prominent names, enhanced statistics, and gradient trust metric bars.

### Technical Implementations
- **Backend**: Django 5.2.6 (Python 3.12)
- **Frontend**: HTML templates with Tailwind CSS
- **Database**: SQLite (development)
- **Image Handling**: Pillow for image uploads.
- **Authentication**: Custom authentication system with Japanese-language login/signup pages, secure logout, and `next` parameter handling for redirects.
- **User Profiles**: Comprehensive `UserProfile` model with fields for profile picture, bio, dynamic `reputation_score`, `total_contributions`, `success_rate`, `location_display`, `is_verified`, and `followers_count`. Includes a bulletproof profile safety system using context processors and template filters to prevent `RelatedObjectDoesNotExist` errors.
- **Peer-to-Peer Rating**: `Review` model for 1-5 star ratings and comments, automatically calculating user reputation scores.
- **Follow System**: `Follow` model implementing follower/following relationships with dynamic count calculation and a toggle follow/unfollow view.
- **Posts**: Users can create GIVE (offering) or REQUEST (seeking) posts with image uploads, location data (Japanese postal codes), and a tag/category system. Posts display visual badges for type and link to user profiles.
- **Search**: Functionality to search by title, body, artist, and tags.

### Feature Specifications
- User authentication with Japanese UI.
- User profiles with community metrics, trust scores, and activity tabs.
- Peer-to-peer rating system with dynamic reputation scores.
- Post creation with image uploads, location, and privacy options.
- Search functionality.
- Follow/unfollow system for users.
- Custom authentication pages (`/login/`, `/signup/`, `/logout/`).

### System Design Choices
- Configured for Replit compatibility with `0.0.0.0:5000` for the development server and `ALLOWED_HOSTS = ['*']`.
- Deployment configured for Autoscale with Gunicorn.
- Uses `LOGIN_URL` and `LOGIN_REDIRECT_URL` for custom authentication flow.
- Context processors and template filters ensure safe access to user profiles and post owners, preventing errors.

## External Dependencies
- **ZipCloud API**: Used for Japanese postal code lookup.
- **Nominatim/OpenStreetMap**: Used for geocoding services.
- **Swiper.js**: Integrated for hero background carousels.
- **Alpine.js**: Used for dynamic UI behaviors like the auto-hiding header.
- **Python Packages**:
    - Django 5.2.6
    - Pillow 11.1.0
    - beautifulsoup4 4.12.3
    - requests 2.32.3
    - gunicorn 23.0.0